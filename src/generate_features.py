import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument(
"--data-dir",
required=True,
help="Input data directory"
)

parser.add_argument(
"--output",
required=True,
help="Output feature file"
)

args = parser.parse_args()

df = pd.read_csv(f"{args.data_dir}/master_dataset.csv")

# --------------------

# Basic Metrics

# --------------------

df["roas"] = np.where(
df["spend"] > 0,
df["revenue"] / df["spend"],
0
)

df["ctr"] = np.where(
df["impressions"] > 0,
df["clicks"] / df["impressions"],
0
)

df["cpc"] = np.where(
df["clicks"] > 0,
df["spend"] / df["clicks"],
0
)

df["conversion_rate"] = np.where(
df["clicks"] > 0,
df["conversions"] / df["clicks"],
0
)

# --------------------

# Date Features

# --------------------

df["date"] = pd.to_datetime(df["date"])

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["quarter"] = df["date"].dt.quarter
df["week"] = df["date"].dt.isocalendar().week.astype(int)
df["dayofweek"] = df["date"].dt.dayofweek

# --------------------

# Lag Features

# --------------------

df = df.sort_values("date")

df["spend_lag_7"] = df["spend"].rolling(7).mean()
df["spend_lag_30"] = df["spend"].rolling(30).mean()

df["revenue_lag_7"] = df["revenue"].rolling(7).mean()
df["revenue_lag_30"] = df["revenue"].rolling(30).mean()

df.fillna(0, inplace=True)

# Save both formats

df.to_csv("data/features_dataset.csv", index=False)

df.to_parquet(args.output, index=False)

print("=" * 50)
print("FEATURE ENGINEERING COMPLETE")
print("=" * 50)

print(f"Saved: {args.output}")
print(df.head())
