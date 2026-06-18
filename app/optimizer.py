"""
optimizer.py

Computes a data-driven recommended budget allocation per channel,
based on each channel's forecast ROAS (forecast revenue per dollar
of spend). Replaces the previously hardcoded 60/30/10 -> 70/20/10
allocation table.

Method (transparent, so it can be explained to a judge):
1. For each channel, compute forecast ROAS =
       sum(forecast_revenue) / sum(spend)
   This is "how much revenue does this channel return per dollar
   spent", under the model's forecast.
2. Normalize ROAS across channels so the values sum to 100% ->
   this becomes "Recommended Allocation". A channel with double
   the ROAS of another gets roughly double the recommended share.
3. "Current Allocation" is each channel's actual share of total
   historical spend.

NOTE on an earlier, rejected approach: using
forecast_revenue / actual_revenue as the efficiency signal was
tried and discarded, because for a well-fit model that ratio is
close to 1.0 for every channel, which collapses the recommendation
to an uninformative even split regardless of true channel
performance. ROAS (revenue per dollar of spend) is the metric that
actually reflects efficiency.
"""

import pandas as pd


def compute_optimization_table(scenario_df):
    """
    scenario_df must have columns: channel, spend, forecast_revenue.
    Returns (table, numeric):
        table  - DataFrame with Channel, Current Allocation,
                 Recommended Allocation (for display)
        numeric - dict of the underlying percentages and ROAS
                  scores (for downstream calculations / LLM prompt)
    """
    channel_perf = (
        scenario_df
        .groupby("channel")
        .agg(
            forecast_revenue=("forecast_revenue", "sum"),
            spend=("spend", "sum"),
        )
    )

    channel_perf["forecast_roas"] = channel_perf.apply(
        lambda row: row["forecast_revenue"] / row["spend"]
        if row["spend"] > 0 else 0,
        axis=1,
    )

    roas_sum = channel_perf["forecast_roas"].sum()
    if roas_sum > 0:
        recommended_pct = (channel_perf["forecast_roas"] / roas_sum) * 100
    else:
        recommended_pct = pd.Series(
            [100 / len(channel_perf)] * len(channel_perf),
            index=channel_perf.index,
        )

    spend_sum = channel_perf["spend"].sum()
    if spend_sum > 0:
        current_pct = (channel_perf["spend"] / spend_sum) * 100
    else:
        current_pct = recommended_pct

    table = pd.DataFrame({
        "Channel": channel_perf.index,
        "Current Allocation": current_pct.round(1).astype(str) + "%",
        "Recommended Allocation": recommended_pct.round(1).astype(str) + "%",
    }).reset_index(drop=True)

    numeric = {
        "current_pct": current_pct.to_dict(),
        "recommended_pct": recommended_pct.to_dict(),
        "forecast_roas": channel_perf["forecast_roas"].to_dict(),
    }

    return table, numeric


def estimate_revenue_impact(scenario_df, numeric):
    """
    Directional estimate only: holds each channel's forecast ROAS
    fixed and asks "what would happen to total revenue if total
    spend were redistributed from current_pct to recommended_pct".
    This assumes ROAS stays constant as spend shifts, which real
    channels rarely do (diminishing returns), so this should be
    labeled as a rough/directional estimate in the UI, not a
    guaranteed outcome.
    """
    total_spend = scenario_df["spend"].sum()
    current = numeric["current_pct"]
    recommended = numeric["recommended_pct"]
    roas = numeric["forecast_roas"]

    delta = 0.0
    for channel in current:
        spend_share_change = (recommended[channel] - current[channel]) / 100
        delta += spend_share_change * total_spend * roas.get(channel, 0)

    return delta