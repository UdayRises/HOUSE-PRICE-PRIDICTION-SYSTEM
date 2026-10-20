// ============================================================================
// BILINGUAL TRANSLATION DICTIONARY (ENGLISH & HINDI)
// ============================================================================
const TRANSLATIONS = {
  en: {
    tag: "EN",
    language_label: "LANGUAGE / भाषा",
    eyebrow: "DRAWING NO. HP‑001 • AMES REGRESSION ENGINE",
    app_title: "Appraised",
    subhead: "A structural estimate of market value, drafted in real time from your architectural specifications.",
    stat_model: "MODEL",
    stat_model_val: "Random Forest",
    stat_r2: "R² ON HOLDOUT",
    stat_mae: "MAE CONFIDENCE",
    schematic_title: "FIG. 1 — FLOOR SCHEMATIC (LIVE DRAFT)",
    live_cad_sync: "LIVE CAD SYNC",
    scale_text: "SCALE — NTS (SCHEMATIC)",
    estimate_label: "APPRAISED VALUATION",
    estimate_placeholder: "Configure specifications and click STAMP ESTIMATE",
    confidence_badge: "CONFIDENCE INTERVAL ACTIVE",
    spec_title: "FIG. 2 — ARCHITECTURAL SPECIFICATIONS",
    presets_label: "LOAD PRESET:",
    preset_starter: "Compact Starter",
    preset_suburban: "Suburban Family",
    preset_estate: "Executive Estate",
    label_grlivarea: "Living Area (sq ft)",
    label_lotarea: "Lot Area (sq ft)",
    label_totalbsmtsf: "Basement Area (sq ft)",
    label_overallqual: "Build Quality (1–10)",
    label_overallcond: "Condition (1–10)",
    label_yearbuilt: "Year Built",
    label_bedroomabvgr: "Bedrooms",
    label_fullbath: "Full Baths",
    label_halfbath: "Half Baths",
    label_garagecars: "Garage (Cars)",
    label_fireplaces: "Fireplaces",
    label_neighborhood: "Neighborhood",
    label_housestyle: "House Style",
    label_centralair: "Central Air",
    opt_yes: "Yes",
    opt_no: "No",
    submit_btn: "STAMP ESTIMATE",
    submitting_btn: "APPRAISING...",
    range_prefix: "Range: ",
    confidence_prefix: "CONFIDENCE INTERVAL ",
    dim_area_suffix: "sq ft living area",
    dim_bed_single: "BEDROOM",
    dim_bed_plural: "BEDROOMS",
    dim_bath_single: "BATH",
    dim_bath_plural: "BATHS",
    dim_garage_no: "NO GARAGE",
    dim_garage_single: "GARAGE — 1 CAR",
    dim_garage_plural: "GARAGE — {n} CARS",
    val_failed: "VALUATION FAILED",
  },
  hi: {
    tag: "HI",
    language_label: "भाषा / LANGUAGE",
    eyebrow: "ड्राइंग सं. HP‑001 • एम्स रिग्रेशन इंजन",
    app_title: "मूल्यांकित (Appraised)",
    subhead: "आपके वास्तुशिल्प विनिर्देशों से वास्तविक समय में तैयार किया गया बाज़ार मूल्य का संरचनात्मक अनुमान।",
    stat_model: "मॉडल",
    stat_model_val: "रैंडम फ़ॉरेस्ट",
    stat_r2: "होल्डआउट पर R²",
    stat_mae: "MAE विश्वास सीमा",
    schematic_title: "चित्र 1 — फ़्लोर योजना (लाइव ड्राफ़्ट)",
    live_cad_sync: "लाइव CAD सिंक",
    scale_text: "पैमाना — सांकेतिक (SCHEMATIC)",
    estimate_label: "अनुमानित मूल्यांकन (VALUATION)",
    estimate_placeholder: "विनिर्देश सेट करें और 'अनुमानित मूल्य निकालें' पर क्लिक करें",
    confidence_badge: "सक्रिय विश्वास अंतराल (CONFIDENCE ACTIVE)",
    spec_title: "चित्र 2 — वास्तुशिल्प विनिर्देश",
    presets_label: "प्रीसेट चुनें:",
    preset_starter: "कॉम्पैक्ट स्टार्टर",
    preset_suburban: "उपनगरीय परिवार",
    preset_estate: "आलीशान एस्टेट",
    label_grlivarea: "रहने का क्षेत्र (वर्ग फीट)",
    label_lotarea: "प्लॉट का क्षेत्रफल (वर्ग फीट)",
    label_totalbsmtsf: "बेसमेंट क्षेत्र (वर्ग फीट)",
    label_overallqual: "निर्माण गुणवत्ता (1–10)",
    label_overallcond: "मकान की स्थिति (1–10)",
    label_yearbuilt: "निर्माण वर्ष",
    label_bedroomabvgr: "शयनकक्ष (Bedrooms)",
    label_fullbath: "पूरे स्नानघर (Full Baths)",
    label_halfbath: "आधे स्नानघर (Half Baths)",
    label_garagecars: "गैराज (गाड़ियों की संख्या)",
    label_fireplaces: "अंगीठी (Fireplaces)",
    label_neighborhood: "इलाका / कॉलोनी (Neighborhood)",
    label_housestyle: "मकान की शैली (House Style)",
    label_centralair: "सेंट्रल एसी (Central Air)",
    opt_yes: "हाँ (Yes)",
    opt_no: "नहीं (No)",
    submit_btn: "अनुमानित मूल्य निकालें (STAMP ESTIMATE)",
    submitting_btn: "मूल्यांकन जारी है...",
    range_prefix: "अनुमानित दायरा: ",
    confidence_prefix: "विश्वास अंतराल ",
    dim_area_suffix: "वर्ग फीट रहने का क्षेत्र",
    dim_bed_single: "शयनकक्ष (BEDROOM)",
    dim_bed_plural: "शयनकक्ष (BEDROOMS)",
    dim_bath_single: "स्नानघर (BATH)",
    dim_bath_plural: "स्नानघर (BATHS)",
    dim_garage_no: "गैराज नहीं है",
    dim_garage_single: "गैराज — 1 गाड़ी",
    dim_garage_plural: "गैराज — {n} गाड़ियाँ",
    val_failed: "मूल्यांकन विफल रहा",
  }
};

// ============================================================================
// STATE & DOM ELEMENTS
// ============================================================================
let currentLang = localStorage.getItem("appraised_lang") || "en";
let latestPredictionData = null;

// DOM Elements
const form = document.getElementById("predict-form");
const submitButton = document.getElementById("submit-btn");
const formNote = document.getElementById("form-note");
const estimateBox = document.getElementById("estimate-box");
const estimateLabel = document.getElementById("estimate-label");
const estimateValue = document.getElementById("estimate-value");
const estimateRange = document.getElementById("estimate-range");
const estimateSummary = document.getElementById("estimate-summary");
const estimateLangTag = document.getElementById("estimate-lang-tag");
const confidenceBadge = document.getElementById("confidence-badge");

const btnLangEn = document.getElementById("btn-lang-en");
const btnLangHi = document.getElementById("btn-lang-hi");

// SVG Blueprint Elements
const dimArea = document.getElementById("dim-area");
const dimBed = document.getElementById("dim-bed");
const dimBath = document.getElementById("dim-bath");
const dimGarage = document.getElementById("dim-garage");
const scaleText = document.getElementById("scale-text");
const garageGroup = document.getElementById("garage-group");
const garageRect = document.getElementById("garage-rect");
const chimneyGroup = document.getElementById("chimney-group");
const secondStoryDecor = document.getElementById("second-story-decor");

// Preset Archetypes
const PRESETS = {
  starter: {
    GrLivArea: 1150,
    LotArea: 6500,
    TotalBsmtSF: 600,
    OverallQual: 5,
    OverallCond: 5,
    YearBuilt: 1982,
    BedroomAbvGr: 2,
    FullBath: 1,
    HalfBath: 0,
    GarageCars: 1,
    Fireplaces: 0,
    Neighborhood: "Edwards",
    HouseStyle: "1Story",
    CentralAir: "Y",
  },
  suburban: {
    GrLivArea: 1850,
    LotArea: 9500,
    TotalBsmtSF: 950,
    OverallQual: 7,
    OverallCond: 6,
    YearBuilt: 2005,
    BedroomAbvGr: 3,
    FullBath: 2,
    HalfBath: 1,
    GarageCars: 2,
    Fireplaces: 1,
    Neighborhood: "CollgCr",
    HouseStyle: "2Story",
    CentralAir: "Y",
  },
  estate: {
    GrLivArea: 3200,
    LotArea: 16000,
    TotalBsmtSF: 1600,
    OverallQual: 9,
    OverallCond: 8,
    YearBuilt: 2018,
    BedroomAbvGr: 4,
    FullBath: 3,
    HalfBath: 1,
    GarageCars: 3,
    Fireplaces: 2,
    Neighborhood: "NridgHt",
    HouseStyle: "2Story",
    CentralAir: "Y",
  },
};

// ============================================================================
// LANGUAGE SWITCHING LOGIC
// ============================================================================
function setLanguage(lang) {
  if (!TRANSLATIONS[lang]) return;
  currentLang = lang;
  localStorage.setItem("appraised_lang", lang);

  // Update active button state
  if (btnLangEn && btnLangHi) {
    if (lang === "en") {
      btnLangEn.classList.add("active");
      btnLangHi.classList.remove("active");
    } else {
      btnLangHi.classList.add("active");
      btnLangEn.classList.remove("active");
    }
  }

  const t = TRANSLATIONS[lang];

  // Update language tag on estimate box
  if (estimateLangTag) {
    estimateLangTag.textContent = t.tag;
  }

  // Update all elements with data-i18n
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (t[key] !== undefined) {
      el.textContent = t[key];
    }
  });

  // Update SVG scale text
  if (scaleText && t.scale_text) {
    scaleText.textContent = t.scale_text;
  }

  // Re-render schematic callouts in selected language
  updateSchematic();

  // If we already have prediction data, re-run appraisal with the newly selected language
  performAppraisal();
}

/**
 * Updates the SVG blueprint in real time based on current form inputs and active language.
 */
function updateSchematic() {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
  const formData = new FormData(form);
  const livArea = parseFloat(formData.get("GrLivArea")) || 0;
  const bedrooms = parseInt(formData.get("BedroomAbvGr"), 10) || 0;
  const fullBaths = parseInt(formData.get("FullBath"), 10) || 0;
  const halfBaths = parseInt(formData.get("HalfBath"), 10) || 0;
  const garageCars = parseInt(formData.get("GarageCars"), 10) || 0;
  const fireplaces = parseInt(formData.get("Fireplaces"), 10) || 0;
  const houseStyle = formData.get("HouseStyle") || "1Story";

  // 1. Living Area Dimension
  if (dimArea) {
    dimArea.textContent = `${livArea.toLocaleString()} ${t.dim_area_suffix}`;
  }

  // 2. Bedrooms Callout
  if (dimBed) {
    const label = bedrooms === 1 ? t.dim_bed_single : t.dim_bed_plural;
    dimBed.textContent = `${bedrooms} ${label}`;
  }

  // 3. Bathrooms Callout
  if (dimBath) {
    const totalBaths = fullBaths + halfBaths * 0.5;
    const label = totalBaths === 1 ? t.dim_bath_single : t.dim_bath_plural;
    dimBath.textContent = `${totalBaths} ${label}`;
  }

  // 4. Garage Callout and Geometry
  if (dimGarage) {
    if (garageCars <= 0) {
      dimGarage.textContent = t.dim_garage_no;
      if (garageGroup) garageGroup.style.opacity = "0.2";
    } else {
      const label = garageCars === 1 ? t.dim_garage_single : t.dim_garage_plural.replace("{n}", garageCars);
      dimGarage.textContent = label;
      if (garageGroup) garageGroup.style.opacity = "1";
      if (garageRect) {
        const widths = { 1: 50, 2: 75, 3: 95, 4: 105 };
        const w = widths[garageCars] || 75;
        garageRect.setAttribute("width", w.toString());
      }
    }
  }

  // 5. Fireplace Chimney
  if (chimneyGroup) {
    chimneyGroup.style.opacity = fireplaces > 0 ? "1" : "0.08";
  }

  // 6. House Style Decor
  if (secondStoryDecor) {
    const isMultiStory = houseStyle.includes("2") || houseStyle.includes("1.5");
    secondStoryDecor.style.opacity = isMultiStory ? "1" : "0.2";
  }
}

/**
 * Smoothly animates a number counting up to the target value.
 */
function animateValue(element, start, end, duration = 600) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const easeProgress = 1 - Math.pow(1 - progress, 3); // cubic ease out
    const current = Math.floor(easeProgress * (end - start) + start);
    element.textContent = `$${current.toLocaleString()}`;
    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      element.textContent = `$${end.toLocaleString()}`;
    }
  };
  window.requestAnimationFrame(step);
}

/**
 * Performs appraisal calculation via the backend API with language selection.
 */
async function performAppraisal() {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
  const rawEntries = Object.fromEntries(new FormData(form).entries());
  
  // Attach current selected language choice to the request payload
  const payload = {
    ...rawEntries,
    language: currentLang,
  };

  submitButton.disabled = true;
  submitButton.textContent = t.submitting_btn;
  formNote.textContent = "";

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const text = await response.text();
    let data = {};
    if (text) {
      try {
        data = JSON.parse(text);
      } catch (err) {
        throw new Error(`Invalid server response (${response.status})`);
      }
    }

    if (!response.ok) {
      throw new Error(data.error || `Request failed with status ${response.status}`);
    }

    latestPredictionData = data;

    const predictedPrice = Math.round(Number(data.predicted_price));
    const lowEst = Math.round(Number(data.low_estimate));
    const highEst = Math.round(Number(data.high_estimate));
    const mae = Math.round(Number(data.mae || 0));

    // Remove error state and trigger visual update flash
    estimateBox.classList.remove("error");
    estimateBox.classList.add("updated");
    setTimeout(() => estimateBox.classList.remove("updated"), 600);

    // Update label and language tag
    if (estimateLabel) {
      estimateLabel.textContent = data.output_title || t.estimate_label;
    }
    if (estimateLangTag) {
      estimateLangTag.textContent = t.tag;
    }

    // Animate valuation number
    const currentNum = parseInt(estimateValue.textContent.replace(/\D/g, ""), 10) || predictedPrice;
    animateValue(estimateValue, currentNum, predictedPrice, 500);

    // Update range and confidence using localized strings
    estimateRange.textContent = `${t.range_prefix}$${lowEst.toLocaleString()} – $${highEst.toLocaleString()}`;
    
    if (confidenceBadge) {
      confidenceBadge.textContent = `${t.confidence_prefix}±$${mae.toLocaleString()} MAE`;
    }

    // Display rich natural language summary if provided by API
    if (estimateSummary && data.summary) {
      estimateSummary.textContent = data.summary;
      estimateSummary.classList.add("active");
    }

  } catch (error) {
    console.error("Appraisal error:", error);
    estimateBox.classList.add("error");
    estimateValue.textContent = t.val_failed;
    estimateRange.textContent = error.message;
    formNote.textContent = error.message;
    if (estimateSummary) {
      estimateSummary.classList.remove("active");
    }
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = t.submit_btn;
  }
}

// ============================================================================
// EVENT LISTENERS
// ============================================================================

// Language Switcher Buttons
if (btnLangEn) {
  btnLangEn.addEventListener("click", () => setLanguage("en"));
}
if (btnLangHi) {
  btnLangHi.addEventListener("click", () => setLanguage("hi"));
}

// Preset button handlers
document.querySelectorAll(".preset-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const presetKey = button.getAttribute("data-preset");
    const presetData = PRESETS[presetKey];
    if (!presetData) return;

    Object.entries(presetData).forEach(([field, value]) => {
      const input = form.elements[field];
      if (input) {
        input.value = value;
      }
    });

    updateSchematic();
    performAppraisal();
  });
});

// Event Listeners for live schematic updates
form.addEventListener("input", updateSchematic);
form.addEventListener("change", updateSchematic);

// Form submit handler
form.addEventListener("submit", (event) => {
  event.preventDefault();
  performAppraisal();
});

// Initial boot
document.addEventListener("DOMContentLoaded", () => {
  // Apply saved or default language
  setLanguage(currentLang);
});