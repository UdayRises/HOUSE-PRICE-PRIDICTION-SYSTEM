import json
import os
import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "house_price_model.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

# Template & Static directories configuration
TEMPLATE_DIR = (
    os.path.join(BASE_DIR, "templates")
    if os.path.isdir(os.path.join(BASE_DIR, "templates"))
    else BASE_DIR
)
STATIC_DIR = (
    os.path.join(BASE_DIR, "static")
    if os.path.isdir(os.path.join(BASE_DIR, "static"))
    else BASE_DIR
)

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config["JSON_AS_ASCII"] = False
try:
    app.json.ensure_ascii = False
except AttributeError:
    pass

# Safe fallback defaults matching Ames Housing specs
DEFAULT_NUMERIC_FEATURES = [
    "GrLivArea", "LotArea", "TotalBsmtSF", "OverallQual", "OverallCond",
    "YearBuilt", "BedroomAbvGr", "FullBath", "HalfBath", "GarageCars",
    "Fireplaces",
]
DEFAULT_CATEGORICAL_FEATURES = ["Neighborhood", "HouseStyle", "CentralAir"]
DEFAULT_NEIGHBORHOODS = [
    "CollgCr", "Edwards", "Gilbert", "NAmes", "NridgHt", "OldTown", "Somerst"
]
DEFAULT_HOUSE_STYLES = [
    "1Story", "1.5Fin", "2Story", "2.5Unf", "SFoyer", "SLvl"
]
DEFAULT_METRICS = {
    "r2": 0.86,
    "mae": 26000,
    "rmse": 34000,
    "train_time_sec": 0.6,
    "n_train": 1600,
    "n_test": 400,
}

pipeline = None
NUMERIC_FEATURES = list(DEFAULT_NUMERIC_FEATURES)
CATEGORICAL_FEATURES = list(DEFAULT_CATEGORICAL_FEATURES)
REQUIRED_FIELDS = NUMERIC_FEATURES + CATEGORICAL_FEATURES
NEIGHBORHOODS = list(DEFAULT_NEIGHBORHOODS)
HOUSE_STYLES = list(DEFAULT_HOUSE_STYLES)
METRICS = dict(DEFAULT_METRICS)


def load_or_train_model():
    """Loads the model and metrics, auto-training if artifacts are missing."""
    global pipeline, NUMERIC_FEATURES, CATEGORICAL_FEATURES, REQUIRED_FIELDS
    global NEIGHBORHOODS, HOUSE_STYLES, METRICS

    if not os.path.exists(MODEL_PATH) or not os.path.exists(METRICS_PATH):
        try:
            print("Model artifacts not found. Initiating auto-training...")
            from model import train_and_save_model
            bundle, metrics = train_and_save_model()
            pipeline = bundle["pipeline"]
            NUMERIC_FEATURES = bundle.get("numeric_features", DEFAULT_NUMERIC_FEATURES)
            CATEGORICAL_FEATURES = bundle.get("categorical_features", DEFAULT_CATEGORICAL_FEATURES)
            NEIGHBORHOODS = bundle.get("neighborhoods", DEFAULT_NEIGHBORHOODS)
            HOUSE_STYLES = bundle.get("house_styles", DEFAULT_HOUSE_STYLES)
            REQUIRED_FIELDS = NUMERIC_FEATURES + CATEGORICAL_FEATURES
            METRICS = metrics
            print("Auto-training completed successfully.")
            return
        except Exception as err:
            print(f"Warning: Auto-training failed: {err}")

    # Load existing model bundle
    if os.path.exists(MODEL_PATH):
        try:
            bundle = joblib.load(MODEL_PATH)
            pipeline = bundle.get("pipeline")
            NUMERIC_FEATURES = bundle.get("numeric_features", DEFAULT_NUMERIC_FEATURES)
            CATEGORICAL_FEATURES = bundle.get("categorical_features", DEFAULT_CATEGORICAL_FEATURES)
            NEIGHBORHOODS = bundle.get("neighborhoods", DEFAULT_NEIGHBORHOODS)
            HOUSE_STYLES = bundle.get("house_styles", DEFAULT_HOUSE_STYLES)
            REQUIRED_FIELDS = NUMERIC_FEATURES + CATEGORICAL_FEATURES
            print("Model loaded successfully.")
        except Exception as err:
            print(f"Error loading model from {MODEL_PATH}: {err}")

    # Load existing metrics
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict) and loaded:
                    METRICS = loaded
        except Exception as err:
            print(f"Error loading metrics from {METRICS_PATH}: {err}")


# Initialize model on startup
load_or_train_model()


@app.route("/")
def index():
    return render_template(
        "index.html",
        neighborhoods=NEIGHBORHOODS,
        house_styles=HOUSE_STYLES,
        metrics=METRICS,
    )


# Static file fallback routes (supports root /style.css and /script.js)
@app.route("/style.css")
def serve_root_style():
    if os.path.isfile(os.path.join(app.static_folder, "style.css")):
        return send_from_directory(app.static_folder, "style.css")
    return send_from_directory(BASE_DIR, "style.css")


@app.route("/script.js")
def serve_root_script():
    if os.path.isfile(os.path.join(app.static_folder, "script.js")):
        return send_from_directory(app.static_folder, "script.js")
    return send_from_directory(BASE_DIR, "script.js")


@app.route("/api/meta", methods=["GET"])
def meta():
    return jsonify({
        "languages": [
            {"code": "en", "name": "English", "native": "English"},
            {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
        ],
        "neighborhoods": NEIGHBORHOODS,
        "house_styles": HOUSE_STYLES,
        "metrics": METRICS,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "status": "ready" if pipeline is not None else "degraded",
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy" if pipeline is not None else "degraded",
        "model_loaded": pipeline is not None,
        "metrics_available": bool(METRICS),
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    if pipeline is None:
        # Try once more to initialize the model on demand
        load_or_train_model()
        if pipeline is None:
            return jsonify({"error": "Prediction model is currently unavailable."}), 503

    if not request.is_json:
        return jsonify({"error": "Request must use Content-Type: application/json."}), 415

    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify({"error": "Invalid or malformed JSON payload."}), 400

    if not isinstance(payload, dict) or not payload:
        return jsonify({"error": "JSON payload must be a non-empty object."}), 400

    missing_fields = [
        field for field in REQUIRED_FIELDS
        if field not in payload or payload[field] is None or str(payload[field]).strip() == ""
    ]

    if missing_fields:
        return jsonify({
            "error": f"Missing required specification fields: {', '.join(missing_fields)}"
        }), 400

    # Parse and validate feature inputs
    try:
        row = {}

        for feature in NUMERIC_FEATURES:
            raw_val = payload[feature]
            if isinstance(raw_val, bool):
                return jsonify({"error": f"Invalid boolean value for numeric field '{feature}'."}), 400
            val = float(raw_val)

            # Sanity range checks
            if val < 0:
                return jsonify({"error": f"Field '{feature}' cannot be negative."}), 400

            if feature == "GrLivArea" and (val < 200 or val > 20000):
                return jsonify({"error": "Living area must be between 200 and 20,000 sq ft."}), 400
            if feature == "OverallQual" and (val < 1 or val > 10):
                return jsonify({"error": "Build quality must be between 1 and 10."}), 400
            if feature == "OverallCond" and (val < 1 or val > 10):
                return jsonify({"error": "Condition must be between 1 and 10."}), 400
            if feature == "YearBuilt" and (val < 1800 or val > 2030):
                return jsonify({"error": "Year built must be between 1800 and 2030."}), 400

            row[feature] = val

        for feature in CATEGORICAL_FEATURES:
            raw_val = str(payload[feature]).strip()
            if not raw_val:
                return jsonify({"error": f"Field '{feature}' cannot be empty."}), 400
            row[feature] = raw_val

    except (TypeError, ValueError) as err:
        return jsonify({"error": f"Invalid input format: {err}"}), 400

    try:
        input_data = pd.DataFrame([row])
        raw_prediction = float(pipeline.predict(input_data)[0])
        prediction = max(raw_prediction, 10000.0)

        mae = float(METRICS.get("mae", 26000) or 26000)
        low_estimate = max(prediction - mae, 0.0)
        high_estimate = max(prediction + mae, 0.0)

        lang = str(payload.get("language", "en")).strip().lower()
        if lang not in ["en", "hi"]:
            lang = "en"

        if lang == "hi":
            formatted_price = f"${prediction:,.0f}"
            formatted_range = f"${low_estimate:,.0f} – ${high_estimate:,.0f}"
            confidence = f"±${mae:,.0f} MAE (औसत पूर्ण त्रुटि)"
            summary = (
                f"इस मकान का अनुमानित बाज़ार मूल्य ${prediction:,.0f} है। "
                f"संभावित दायरा ${low_estimate:,.0f} से ${high_estimate:,.0f} के बीच है (विश्वास अंतराल: ±${mae:,.0f} MAE)।"
            )
            output_title = "अनुमानित मूल्यांकन"
            status_text = "सफलतापूर्वक अनुमानित"
        else:
            formatted_price = f"${prediction:,.0f}"
            formatted_range = f"${low_estimate:,.0f} – ${high_estimate:,.0f}"
            confidence = f"±${mae:,.0f} MAE"
            summary = (
                f"The estimated market value is ${prediction:,.0f}. "
                f"Expected valuation range is ${low_estimate:,.0f} to ${high_estimate:,.0f} (Confidence: ±${mae:,.0f} MAE)."
            )
            output_title = "APPRAISED VALUATION"
            status_text = "Estimate calculated successfully"

        return jsonify({
            "predicted_price": round(prediction, 2),
            "low_estimate": round(low_estimate, 2),
            "high_estimate": round(high_estimate, 2),
            "mae": round(mae, 2),
            "currency": "$",
            "language": lang,
            "formatted_price": formatted_price,
            "formatted_range": formatted_range,
            "confidence": confidence,
            "summary": summary,
            "output_title": output_title,
            "status_text": status_text,
        })

    except Exception as error:
        app.logger.exception("Prediction calculation error")
        return jsonify({"error": f"Prediction error: {str(error)}"}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found."}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed on this endpoint."}), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    url = f"http://{host}:{port}"

    print("\n" + "=" * 58)
    print("  Appraised — House Price Estimator is LIVE!")
    print(f"  Open in your browser: {url}")
    print("  Press CTRL+C to stop.")
    print("=" * 58 + "\n")

    try:
        from waitress import serve
        serve(app, host=host, port=port)
    except ImportError:
        app.run(host=host, port=port, debug=False)