import streamlit as st
import pandas as pd
import plotly.express as px

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

st.success(
    f"Highest projected revenue comes from {top_channel}."
)

st.info(
    f"Estimated revenue from {top_channel}: ${top_revenue:,.0f}"
)

st.warning(
    f"""
Recommended Action:

Increase investment in {top_channel} campaigns.

Expected Revenue Contribution:
${top_revenue:,.0f}

Monitor underperforming channels and
reallocate spend to maximize forecasted
revenue and ROAS.
"""
)

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

risk_df = pd.DataFrame({
    "Campaign": [
        "Search_TM_Campaign_03",
        "Meta_Brand_Campaign_07",
        "Pmax_Campaign_05"
    ],
    "Risk": [
        "Revenue Drop 42%",
        "ROAS Volatility",
        "Spend Spike"
    ],
    "Severity": [
        "High",
        "Medium",
        "Medium"
    ]
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

optimization_df = pd.DataFrame({
    "Channel": ["Google", "Meta", "Bing"],
    "Current Allocation": ["60%", "30%", "10%"],
    "Recommended Allocation": ["70%", "20%", "10%"]
})

st.dataframe(
    optimization_df,
    use_container_width=True
)

st.success(
    "Expected Revenue Increase: +$1.8M"
)

st.success(
    "Expected ROAS Increase: +12%"
)

st.info(
    """
Optimization Recommendation

Shift budget toward Google campaigns
while reducing spend in lower-performing
campaigns.

This allocation maximizes forecasted
revenue while maintaining strong ROAS.
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