import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

from xgboost import XGBRegressor

# ---------------------------------------
# LOAD DATA
# ---------------------------------------

df = pd.read_csv("data/features_dataset.csv")

# ---------------------------------------
# CLEAN DATA
# ---------------------------------------

df = df.copy()

# Remove extreme ROAS outliers
df = df[df["roas"] < 50]

# ---------------------------------------
# ENCODE CATEGORICAL FEATURES
# ---------------------------------------

le_channel = LabelEncoder()
le_campaign = LabelEncoder()

df["channel_encoded"] = le_channel.fit_transform(
    df["channel"].astype(str)
)

df["campaign_type_encoded"] = le_campaign.fit_transform(
    df["campaign_type"].astype(str)
)

# ---------------------------------------
# FEATURES
# ---------------------------------------

FEATURES = [
    "spend",
    "clicks",
    "impressions",
    "conversions",
    "budget",

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

TARGET = "roas"

X = df[FEATURES]
y = df[TARGET]

# ---------------------------------------
# TRAIN TEST SPLIT
# ---------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ---------------------------------------
# MODEL
# ---------------------------------------

model = XGBRegressor(
    n_estimators=500,
    max_depth=8,
    learning_rate=0.03,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.5,
    reg_lambda=1.0,
    random_state=42
)

# ---------------------------------------
# TRAIN
# ---------------------------------------

model.fit(
    X_train,
    y_train
)

# ---------------------------------------
# PREDICT
# ---------------------------------------

preds = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    preds
)

r2 = r2_score(
    y_test,
    preds
)

print("=" * 50)
print("ROAS MODEL TRAINED")
print("=" * 50)

print(f"MAE: {mae:.4f}")
print(f"R2 Score: {r2:.4f}")

# ---------------------------------------
# SAVE
# ---------------------------------------

joblib.dump(
    model,
    "pickle/roas_model.pkl"
)

joblib.dump(
    le_channel,
    "pickle/roas_channel_encoder.pkl"
)

joblib.dump(
    le_campaign,
    "pickle/roas_campaign_encoder.pkl"
)

print("\nSaved:")

print("roas_model.pkl")
print("roas_channel_encoder.pkl")
print("roas_campaign_encoder.pkl")