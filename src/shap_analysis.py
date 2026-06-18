import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

# Load model
model = joblib.load("pickle/revenue_model.pkl")

# Load engineered dataset
df = pd.read_csv("output/master_featured.csv")

# Keep numeric columns only
X = df.select_dtypes(include=["number"]).copy()

# Remove target if present
for col in ["revenue", "roas"]:
    if col in X.columns:
        X = X.drop(columns=[col])

# Sample to make SHAP faster
X = X.sample(min(500, len(X)), random_state=42)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

plt.figure(figsize=(10,6))
shap.summary_plot(
    shap_values,
    X,
    show=False
)

plt.savefig(
    "output/shap_summary.png",
    bbox_inches="tight"
)

print("SHAP chart saved to output/shap_summary.png")