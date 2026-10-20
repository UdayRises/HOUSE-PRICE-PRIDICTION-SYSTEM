"""
Generates a synthetic housing dataset modeled on the structure and feature
relationships of the well-known Ames Housing dataset (the dataset behind the
Kaggle "House Prices - Advanced Regression Techniques" competition).

We generate synthetically rather than downloading because this environment
has no live internet access. The feature set, ranges, and price-driving
relationships mirror real Ames housing data closely enough for this to be a
realistic training target, while being fully reproducible (fixed seed).
"""
import os
import numpy as np
import pandas as pd

SEED = 42
N_SAMPLES = 2000

# Fix 1a: Align neighborhood keys with what app.py expects in /api/meta
NEIGHBORHOODS = {
    "NridgHt":     1.35,
    "Somerst":     1.18,
    "CollgCr":     1.05,
    "OldTown":     0.85,
    "Edwards":     0.80,
    "Gilbert":     0.95,
    "NAmes":       0.78,
}

def generate(n=N_SAMPLES, seed=SEED):
    rng = np.random.default_rng(seed)

    overall_qual = rng.integers(1, 11, n)                     # 1-10 quality rating
    overall_cond = rng.integers(1, 11, n)                     # 1-10 condition rating
    year_built = rng.integers(1900, 2023, n)
    year_sold = rng.integers(2006, 2011, n)
    age = np.clip(year_sold - year_built, 0, None)

    gr_liv_area = rng.normal(1500, 500, n).clip(400, 5000)    # above-ground living area (sqft)
    lot_area = rng.normal(10000, 4000, n).clip(1500, 50000)
    total_bsmt_sf = (gr_liv_area * rng.uniform(0.3, 0.9, n)).clip(0, 3000)

    bedrooms = rng.integers(1, 6, n)
    full_bath = rng.integers(1, 4, n)
    half_bath = rng.integers(0, 2, n)
    kitchen = rng.integers(1, 2, n) + 1 - 1  # almost always 1
    garage_cars = rng.integers(0, 4, n)
    fireplaces = rng.integers(0, 3, n)

    neighborhood = rng.choice(list(NEIGHBORHOODS.keys()), n)
    neighborhood_mult = np.array([NEIGHBORHOODS[nb] for nb in neighborhood])

    # Fix 1b: Align HouseStyle strings with what app.py /api/meta expects
    house_style = rng.choice(
        ["1Story", "2Story", "1.5Fin", "SLvl", "SFoyer", "2.5Unf"], 
        n, 
        p=[0.40, 0.30, 0.12, 0.08, 0.05, 0.05]
    )
    style_mult = pd.Series(house_style).map({
        "1Story": 1.0, 
        "2Story": 1.08, 
        "1.5Fin": 1.03, 
        "SLvl": 0.97,
        "SFoyer": 0.95,
        "2.5Unf": 0.90
    }).values

    central_air = rng.choice(["Y", "N"], n, p=[0.93, 0.07])
    air_mult = np.where(central_air == "Y", 1.05, 0.92)

    # --- Price model -----------------------------------------------------
    base = 20000
    price = (
        base
        + gr_liv_area * 85
        + total_bsmt_sf * 35
        + lot_area * 1.1
        + overall_qual * 9000
        + overall_cond * 1800
        + bedrooms * 3500
        + full_bath * 6000
        + half_bath * 2500
        + garage_cars * 5500
        + fireplaces * 3200
        - age * 220
    )
    price = price * neighborhood_mult * style_mult * air_mult
    price = price * rng.normal(1.0, 0.08, n)  # market noise
    price = price.clip(35000, 800000).round(-2)

    df = pd.DataFrame({
        "GrLivArea": gr_liv_area.round(0).astype(int),
        "LotArea": lot_area.round(0).astype(int),
        "TotalBsmtSF": total_bsmt_sf.round(0).astype(int),
        "OverallQual": overall_qual,
        "OverallCond": overall_cond,
        "YearBuilt": year_built,
        "YrSold": year_sold,
        "BedroomAbvGr": bedrooms,
        "FullBath": full_bath,
        "HalfBath": half_bath,
        "GarageCars": garage_cars,
        "Fireplaces": fireplaces,
        "Neighborhood": neighborhood,
        "HouseStyle": house_style,
        "CentralAir": central_air,
        "SalePrice": price.astype(int),
    })
    return df


DEFAULT_NEIGHBORHOODS = list(NEIGHBORHOODS.keys())
DEFAULT_HOUSE_STYLES = ["1Story", "2Story", "1.5Fin", "SLvl", "SFoyer", "2.5Unf"]


def generate_and_save(out_path=None, n=N_SAMPLES, seed=SEED):
    """Generates synthetic housing dataset and saves it to CSV."""
    if out_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        out_path = os.path.join(data_dir, "housing.csv")
    else:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

    data = generate(n=n, seed=seed)
    data.to_csv(out_path, index=False)
    return data, out_path


if __name__ == "__main__":
    df, out_path = generate_and_save()
    print(f"Wrote {len(df)} rows to {out_path}")
    print(df.head())