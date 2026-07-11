import sys
from pathlib import Path

import pandas as pd
from lifetimes import BetaGeoFitter, GammaGammaFitter

# Path to the exported customer RFM file
FILE_PATH = Path("C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Customer_RFM_Final.csv")
OUTPUT_FILE = Path("Final_CLV_Data.csv"
                   )
def run_clv_model():
    try:
        print("📥 Loading data...")
        if not FILE_PATH.exists():
            raise FileNotFoundError(f"Input file not found: {FILE_PATH}")

        df = pd.read_csv(FILE_PATH, names=["CustomerID", "recency", "frequency", "monetary"])

        for col in ["recency", "frequency", "monetary"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["recency", "frequency", "monetary"])
        df = df[(df["monetary"] > 0) & (df["frequency"] > 0) & (df["recency"] >= 0)].copy()

        # lifetimes requires T to be greater than or equal to recency.
        df["T"] = df["recency"] + 30

        print(f"✅ Data cleaned. Processing {len(df)} customers.")

        print("🧠 Fitting BG/NBD Model...")
        bgf = BetaGeoFitter(penalizer_coef=0.01)
        bgf.fit(df["frequency"], df["recency"], df["T"])

        print("💰 Fitting Gamma-Gamma Model...")
        ggf = GammaGammaFitter(penalizer_coef=0.01)
        ggf.fit(df["frequency"], df["monetary"])

        print("🔮 Calculating CLV...")
        df["predicted_clv"] = ggf.conditional_expected_average_profit(df["frequency"], df["monetary"])

        output_file = "Final_CLV_Data.csv"
        df.to_csv(output_file, index=False)

        print("-" * 30)
        print(f"🎉 Success! Final data saved to: {output_file}")
        print(df[["CustomerID", "predicted_clv"]].head(10))
        print("-" * 30)

    except Exception as e:
        print(f"❌ Critical Error encountered: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_clv_model()