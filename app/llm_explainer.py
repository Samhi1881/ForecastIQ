"""
llm_explainer.py

Generates a natural-language business explanation of the current
forecast scenario by sending REAL computed statistics to the Claude
API. No fabricated claims -- every number in the prompt is computed
from the dashboard's own dataframes before the call is made.

If the API call fails for any reason (missing key, network error,
rate limit, timeout), `get_ai_explanation` returns a tuple of
(text, used_llm: bool) so the caller can fall back to a rule-based
summary and optionally show a small "AI unavailable" indicator.

Setup:
    pip install anthropic python-dotenv
    Create a .env file in your project root with:
        ANTHROPIC_API_KEY=sk-ant-...
"""

import os
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import anthropic
    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False

MODEL_NAME = "claude-sonnet-4-6"
TIMEOUT_SECONDS = 12


def build_stats_payload(scenario_df, df, top_channel, top_revenue,
                         channel_roas, channel_volatility, uplift):
    """
    Assemble only real, already-computed numbers into a plain dict.
    Nothing here is invented -- every field is passed in by the
    caller (dashboard.py) after it has already calculated them
    from the dataframes.

    Note: `top_channel` here is the channel with the highest total
    forecast REVENUE, which is not necessarily the same channel as
    the one with the best ROAS (efficiency). Both are included,
    labeled distinctly, so the explanation doesn't contradict the
    ROAS-based Budget Optimization Engine elsewhere in the dashboard.
    """
    best_roas_channel = max(channel_roas, key=channel_roas.get) if channel_roas else None

    return {
        "highest_revenue_channel": top_channel,
        "highest_revenue_channel_forecast_revenue": round(float(top_revenue), 2),
        "best_roas_channel": best_roas_channel,
        "total_actual_revenue": round(float(df["revenue"].sum()), 2),
        "total_forecast_revenue": round(float(scenario_df["forecast_revenue"].sum()), 2),
        "forecast_uplift_pct": round(float(uplift), 2),
        "channel_roas": {k: round(float(v), 3) for k, v in channel_roas.items()},
        "channel_roas_volatility": {k: round(float(v), 3) for k, v in channel_volatility.items()},
    }


def _rule_based_fallback(stats):
    """Plain-text summary with no LLM call, used when the API is unavailable."""
    revenue_leader = stats["highest_revenue_channel"]
    revenue_amount = stats["highest_revenue_channel_forecast_revenue"]
    roas_leader = stats.get("best_roas_channel")
    uplift = stats["forecast_uplift_pct"]

    most_volatile = max(
        stats["channel_roas_volatility"],
        key=stats["channel_roas_volatility"].get
    )

    lines = [
        f"{revenue_leader} is projected to generate the highest total forecast "
        f"revenue at ${revenue_amount:,.0f}, contributing to an overall forecast "
        f"uplift of {uplift:.2f}% versus actuals."
    ]

    if roas_leader and roas_leader != revenue_leader:
        lines.append(
            f"However, {roas_leader} has the best forecast ROAS (revenue per "
            f"dollar of spend), making it the most efficient channel even though "
            f"{revenue_leader} generates more total revenue."
        )
    elif roas_leader:
        lines.append(
            f"{roas_leader} also has the best forecast ROAS among channels, "
            f"making it the strongest performer on both revenue and efficiency."
        )

    lines.append(
        f"{most_volatile} shows the highest week-to-week ROAS volatility and "
        f"should be monitored most closely for stability."
    )

    return " ".join(lines)


def get_ai_explanation(stats, api_key=None):
    """
    Returns (explanation_text: str, used_llm: bool).

    `stats` should come from build_stats_payload() -- a dict of
    real, pre-computed numbers. This function does not compute
    anything itself; it only asks Claude to phrase what's already
    been calculated.
    """
    if not _ANTHROPIC_AVAILABLE:
        return _rule_based_fallback(stats), False

    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return _rule_based_fallback(stats), False

    prompt = f"""You are a marketing analytics assistant writing a short business
summary for a revenue forecasting dashboard. Use ONLY the data given below.
Do not invent any numbers, trends, or claims that are not present in this data.
Do not mention specific campaign names. Note that "highest_revenue_channel" and
"best_roas_channel" may be different channels -- if so, explain that distinction
clearly (one drives more total revenue, the other is more efficient per dollar
spent) rather than picking just one. Keep it to 3-4 sentences, plain language,
suitable for a non-technical marketing executive.

DATA:
{json.dumps(stats, indent=2)}

Write the summary now."""

    try:
        client = anthropic.Anthropic(api_key=key, timeout=TIMEOUT_SECONDS)
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        text_blocks = [b.text for b in response.content if b.type == "text"]
        explanation = "\n".join(text_blocks).strip()
        if not explanation:
            return _rule_based_fallback(stats), False
        return explanation, True
    except Exception:
        # Any failure (auth, network, rate limit, timeout) -> safe fallback.
        # Deliberately broad except: this runs live during a demo and must
        # never crash the dashboard.
        return _rule_based_fallback(stats), False