import pandas as pd
import joblib

# Load model
model = joblib.load("pickle/revenue_model.pkl")

# Load encoders
channel_encoder = joblib.load("pickle/channel_encoder.pkl")
campaign_encoder = joblib.load("pickle/campaign_encoder.pkl")

# Load dataset
df = pd.read_csv("data/features_dataset.csv")

# Encode
df["channel_encoded"] = channel_encoder.transform(
    df["channel"].astype(str)
)

df["campaign_type_encoded"] = campaign_encoder.transform(
    df["campaign_type"].astype(str)
)

FEATURES = [
    "spend",
    "clicks",
    "impressions",
    "conversions",
    "budget",
    "roas",
    "ctr",
    "cpc",
    "conversion_rate",
    "month",
    "quarter",
    "week",
    "dayofweek",
    "spend_lag_7",
    "spend_lag_30",
    "revenue_lag_7",
    "revenue_lag_30",
    "channel_encoded",
    "campaign_type_encoded"
]

df["forecast_revenue"] = model.predict(df[FEATURES])

df.to_csv(
    "output/predictions.csv",
    index=False
)

print("Predictions saved.")
print(df[[
    "campaign_name",
    "channel",
    "revenue",
    "forecast_revenue"
]].head())