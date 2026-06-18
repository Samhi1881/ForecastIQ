import pandas as pd
from pathlib import Path

DATA_PATH = Path("datasets/AIgnition_dataset")

google = pd.read_csv(DATA_PATH / "google_ads_campaign_stats.csv")
meta = pd.read_csv(DATA_PATH / "meta_ads_campaign_stats.csv")
bing = pd.read_csv(DATA_PATH / "bing_campaign_stats.csv")

# ----------------------
# GOOGLE
# ----------------------

google_df = pd.DataFrame({
    "date": google["segments_date"],
    "channel": "Google",
    "campaign_name": google["campaign_name"],
    "campaign_type": google["campaign_advertising_channel_type"],
    "spend": google["metrics_cost_micros"] / 1000000,
    "revenue": google["metrics_conversions_value"],
    "clicks": google["metrics_clicks"],
    "impressions": google["metrics_impressions"],
    "conversions": google["metrics_conversions"],
    "budget": google["campaign_budget_amount"]
})

# ----------------------
# META
# ----------------------

meta_df = pd.DataFrame({
    "date": meta["date_start"],
    "channel": "Meta",
    "campaign_name": meta["campaign_name"],
    "campaign_type": "Meta Campaign",
    "spend": meta["spend"],
    "revenue": meta["conversion"],
    "clicks": meta["clicks"],
    "impressions": meta["impressions"],
    "conversions": meta["conversion"],
    "budget": meta["daily_budget"]
})

# ----------------------
# BING
# ----------------------

bing_df = pd.DataFrame({
    "date": bing["TimePeriod"],
    "channel": "Bing",
    "campaign_name": bing["CampaignName"],
    "campaign_type": bing["CampaignType"],
    "spend": bing["Spend"],
    "revenue": bing["Revenue"],
    "clicks": bing["Clicks"],
    "impressions": bing["Impressions"],
    "conversions": bing["Conversions"],
    "budget": bing["DailyBudget"]
})

master_df = pd.concat(
    [google_df, meta_df, bing_df],
    ignore_index=True
)

master_df["date"] = pd.to_datetime(master_df["date"])

master_df.to_csv(
    "data/master_dataset.csv",
    index=False
)

print("=" * 50)
print("MASTER DATASET CREATED")
print("=" * 50)

print(master_df.head())

print("\nShape:", master_df.shape)

print("\nChannels:")
print(master_df["channel"].value_counts())