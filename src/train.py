import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder

# Load data
df = pd.read_csv("data/features_dataset.csv")

# Encode categorical columns
le_channel = LabelEncoder()
le_campaign_type = LabelEncoder()

df["channel_encoded"] = le_channel.fit_transform(df["channel"].astype(str))
df["campaign_type_encoded"] = le_campaign_type.fit_transform(
    df["campaign_type"].astype(str)
)

# Features
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

TARGET = "revenue"

X = df[FEATURES]
y = df[TARGET]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = XGBRegressor(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)

print("="*50)
print("MODEL TRAINED")
print("="*50)

print(f"MAE: {mae:.2f}")
print(f"R2 Score: {r2:.4f}")

# Save model
joblib.dump(model, "pickle/revenue_model.pkl")

# Save encoders
joblib.dump(le_channel, "pickle/channel_encoder.pkl")
joblib.dump(le_campaign_type, "pickle/campaign_encoder.pkl")

print("\nSaved:")
print("revenue_model.pkl")
print("channel_encoder.pkl")
print("campaign_encoder.pkl")