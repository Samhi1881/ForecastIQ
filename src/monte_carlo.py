import pandas as pd
import numpy as np

df = pd.read_csv("output/predictions.csv")

base_forecast = df["forecast_revenue"].sum()

simulations = []

for _ in range(1000):

    noise = np.random.normal(
        loc=1,
        scale=0.10
    )

    simulations.append(
        base_forecast * noise
    )

p10 = np.percentile(simulations,10)
p50 = np.percentile(simulations,50)
p90 = np.percentile(simulations,90)

print("="*50)
print("PROBABILISTIC FORECAST")
print("="*50)

print(f"P10 Revenue: ${p10:,.0f}")
print(f"P50 Revenue: ${p50:,.0f}")
print(f"P90 Revenue: ${p90:,.0f}")