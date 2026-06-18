import pandas as pd
import numpy as np

df = pd.read_csv("data/master_dataset.csv")

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

# Fill missing

df.fillna(0, inplace=True)

# Save

df.to_csv(
    "data/features_dataset.csv",
    index=False
)

print("=" * 50)
print("FEATURE ENGINEERING COMPLETE")
print("=" * 50)

print(df.head())

print("\nShape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())