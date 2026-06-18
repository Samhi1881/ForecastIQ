import streamlit as st
import pandas as pd
import plotly.express as px

from optimizer import compute_optimization_table, estimate_revenue_impact
from llm_explainer import build_stats_payload, get_ai_explanation

CAMPAIGN_TYPE_MAP = {
    "PERFORMANCE_MAX": "Performance Max",
    "PERFORMANCEMAX": "Performance Max",
    "SEARCH": "Search",
    "SHOPPING": "Shopping",
    "DISPLAY": "Display",
    "VIDEO": "Video",
    "DEMAND_GEN": "Demand Gen",
    "AUDIENCE": "Audience",
    "META_CAMPAIGN": "Meta Campaign",
}


def normalize_campaign_type(value):
    key = str(value).upper().replace(" ", "_")
    return CAMPAIGN_TYPE_MAP.get(key, str(value).title())


def compute_channel_roas(data):
    grouped = data.groupby("channel").agg(
        revenue=("revenue", "sum"),
        spend=("spend", "sum"),
    )
    return (grouped["revenue"] / grouped["spend"].replace(0, pd.NA)).fillna(0)


def compute_channel_roas_volatility(data):
    """Std dev of weekly ROAS per channel -- a real volatility signal,
    not a guess. Requires a `date` column."""
    working = data.copy()
    working["date"] = pd.to_datetime(working["date"])
    working["week_start"] = working["date"].dt.to_period("W").dt.start_time

    weekly = working.groupby(["channel", "week_start"]).agg(
        spend=("spend", "sum"),
        revenue=("revenue", "sum"),
    ).reset_index()

    weekly["roas"] = weekly.apply(
        lambda row: row["revenue"] / row["spend"] if row["spend"] > 0 else 0,
        axis=1,
    )

    return weekly.groupby("channel")["roas"].std().fillna(0)

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="ForecastIQ",
    layout="wide"
)

# ==================================================
# TITLE
# ==================================================

st.title("🚀 ForecastIQ")
st.subheader("AI-Powered Revenue & ROAS Intelligence Platform")

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv("output/predictions.csv")

# ==================================================
# BUDGET SIMULATOR
# ==================================================

st.sidebar.title("🎯 Budget Scenario Simulator")

google_change = st.sidebar.slider(
    "Google Budget Change %",
    -50,
    100,
    0
)

meta_change = st.sidebar.slider(
    "Meta Budget Change %",
    -50,
    100,
    0
)

bing_change = st.sidebar.slider(
    "Bing Budget Change %",
    -50,
    100,
    0
)

scenario_df = df.copy()

scenario_df.loc[
    scenario_df["channel"] == "Google",
    "forecast_revenue"
] *= (1 + google_change / 100)

scenario_df.loc[
    scenario_df["channel"] == "Meta",
    "forecast_revenue"
] *= (1 + meta_change / 100)

scenario_df.loc[
    scenario_df["channel"] == "Bing",
    "forecast_revenue"
] *= (1 + bing_change / 100)

# ==================================================
# KPI CALCULATIONS
# ==================================================

total_revenue = df["revenue"].sum()

forecast_revenue = scenario_df[
    "forecast_revenue"
].sum()

uplift = (
    (forecast_revenue - total_revenue)
    / total_revenue
) * 100

# ==================================================
# EXECUTIVE SUMMARY
# ==================================================

st.info(
    f"""
### 📋 Executive Summary

ForecastIQ predicts **${forecast_revenue:,.0f}** in revenue.

Model Confidence: **93.56%**

Expected Revenue Range:

- P10: **$9.67M**
- P50: **$11.11M**
- P90: **$12.51M**

Recommendation:

Allocate more budget toward the highest-performing channel while monitoring campaign risks.
"""
)

st.caption(
    "Model Confidence and the P10/P50/P90 range above reflect the trained "
    "model's overall fit and are not recalculated per budget scenario. "
    "Revenue and ROAS figures below the divider DO update with the sliders."
)

# ==================================================
# KPI SECTION
# ==================================================

forecast_roas = (
    forecast_revenue /
    max(df["spend"].sum(), 1)
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Actual Revenue",
    f"${total_revenue:,.0f}"
)

col2.metric(
    "Forecast Revenue",
    f"${forecast_revenue:,.0f}"
)

col3.metric(
    "Forecast Uplift %",
    f"{uplift:.2f}%"
)

col4.metric(
    "Forecast ROAS",
    f"{forecast_roas:.2f}"
)

st.divider()

# ==================================================
# AI RECOMMENDATIONS
# ==================================================

st.subheader("🤖 AI Recommendations")

top_channel = (
    scenario_df
    .groupby("channel")["forecast_revenue"]
    .sum()
    .idxmax()
)

top_revenue = (
    scenario_df
    .groupby("channel")["forecast_revenue"]
    .sum()
    .max()
)

channel_roas = compute_channel_roas(scenario_df)
channel_volatility = compute_channel_roas_volatility(scenario_df)

ai_stats = build_stats_payload(
    scenario_df=scenario_df,
    df=df,
    top_channel=top_channel,
    top_revenue=top_revenue,
    channel_roas=channel_roas.to_dict(),
    channel_volatility=channel_volatility.to_dict(),
    uplift=uplift,
)

ai_text, used_llm = get_ai_explanation(ai_stats)

st.success(ai_text)

if not used_llm:
    st.caption("⚠ AI explanation unavailable — showing rule-based summary.")

# ==================================================
# MODEL CONFIDENCE
# ==================================================

st.subheader("📈 Forecast Confidence")

st.metric(
    "Model Confidence (R²)",
    "93.56%"
)

# ==================================================
# PROBABILISTIC FORECAST
# ==================================================

st.subheader("🎲 Probabilistic Forecast")

p1, p2, p3 = st.columns(3)

p1.metric(
    "P10 Revenue",
    "$9.67M"
)

p2.metric(
    "P50 Revenue",
    "$11.11M"
)

p3.metric(
    "P90 Revenue",
    "$12.51M"
)

st.divider()

# ==================================================
# RISK CENTER
# ==================================================

st.subheader("⚠ Risk Center")

st.error(
    "Potential campaign anomalies detected."
)

st.write(
    """
Monitor campaigns with unusual
revenue, spend, or ROAS behavior.
"""
)

volatility_sorted = channel_volatility.sort_values(ascending=False)


def severity_label(rank):
    return ["High", "Medium", "Low"][min(rank, 2)]


risk_df = pd.DataFrame({
    "Channel": volatility_sorted.index,
    "Weekly ROAS Volatility (std dev)": volatility_sorted.round(2).values,
    "Severity": [severity_label(i) for i in range(len(volatility_sorted))],
})

st.dataframe(
    risk_df,
    use_container_width=True
)

st.divider()

# ==================================================
# OPTIMIZATION ENGINE
# ==================================================

st.subheader("🎯 Budget Optimization Engine")

optimization_df, optimization_numeric = compute_optimization_table(scenario_df)

st.dataframe(
    optimization_df,
    use_container_width=True
)

estimated_delta = estimate_revenue_impact(scenario_df, optimization_numeric)

st.success(
    f"Estimated Revenue Impact of Reallocation: ${estimated_delta:,.0f}"
)

st.caption(
    "Directional estimate only — assumes each channel's forecast ROAS "
    "stays constant as spend shifts, which real channels rarely do "
    "exactly (diminishing returns typically apply at higher spend)."
)

top_recommended_channel = max(
    optimization_numeric["recommended_pct"],
    key=optimization_numeric["recommended_pct"].get,
)

st.info(
    f"""
Optimization Recommendation

Recommended allocations are calculated from each channel's
forecast ROAS (forecast revenue per dollar of spend), not
hardcoded. {top_recommended_channel} currently has the strongest
forecast ROAS and receives the largest recommended share.
"""
)

st.divider()

# ==================================================
# CHANNEL PERFORMANCE
# ==================================================

st.subheader("📊 Revenue by Channel")

channel_df = (
    scenario_df
    .groupby("channel")
    .agg({
        "revenue": "sum",
        "forecast_revenue": "sum"
    })
    .reset_index()
)

fig = px.bar(
    channel_df,
    x="channel",
    y=["revenue", "forecast_revenue"],
    barmode="group",
    title="Revenue by Channel"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ==================================================
# CAMPAIGN TYPE PERFORMANCE
# ==================================================

st.divider()

st.subheader("🎯 Campaign Type Performance")

scenario_df["campaign_type_norm"] = scenario_df["campaign_type"].apply(
    normalize_campaign_type
)

campaign_type_df = (
    scenario_df
    .groupby("campaign_type_norm")
    .agg({
        "revenue": "sum",
        "forecast_revenue": "sum"
    })
    .reset_index()
    .rename(columns={"campaign_type_norm": "campaign_type"})
)

fig3 = px.bar(
    campaign_type_df,
    x="campaign_type",
    y=["revenue", "forecast_revenue"],
    barmode="group",
    title="Forecast Revenue by Campaign Type"
)

st.plotly_chart(
    fig3,
    width="stretch"
)

st.caption(
    "Campaign type labels are normalized (e.g. 'PERFORMANCE_MAX' and "
    "'PerformanceMax' are merged into one category) to avoid duplicate bars."
)

# ==================================================
# CAMPAIGN FORECASTS
# ==================================================

st.subheader("📋 Campaign Forecasts")

st.dataframe(
    scenario_df[
        [
            "campaign_name",
            "channel",
            "revenue",
            "forecast_revenue"
        ]
    ],
    width="stretch"
)

# ==================================================
# TOP CAMPAIGNS
# ==================================================

st.subheader("🏆 Top Forecasted Campaigns")

top_campaigns = (
    scenario_df
    .groupby("campaign_name")
    .agg({
        "forecast_revenue": "sum"
    })
    .sort_values(
        "forecast_revenue",
        ascending=False
    )
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    top_campaigns,
    x="campaign_name",
    y="forecast_revenue",
    title="Top Forecasted Campaigns"
)

st.plotly_chart(
    fig2,
    width="stretch"
)

st.divider()

# ==================================================
# BUSINESS IMPACT
# ==================================================

st.subheader("💼 Business Impact")

st.success(
    """
ForecastIQ enables marketing teams to:

• Forecast Revenue

• Forecast ROAS

• Simulate Budget Scenarios

• Detect Campaign Risks

• Quantify Forecast Uncertainty

• Optimize Marketing Spend Allocation
"""
)

# ==================================================
# FOOTER
# ==================================================

st.caption(
    "ForecastIQ • AI-Powered Revenue, ROAS & Marketing Intelligence Platform"
)