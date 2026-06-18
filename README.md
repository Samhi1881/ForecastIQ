# ForecastIQ

## AI-Powered Revenue & ROAS Intelligence Platform

ForecastIQ is a marketing forecasting and decision intelligence platform and helps organizations forecast revenue, predict Return on Ad Spend (ROAS), evaluate budget allocation strategies, quantify forecast uncertainty, identify campaign risks, and generate actionable recommendations for marketing decision-making.

---

## Executive Summary

Marketing teams frequently make strategic budget decisions based on historical reports and manual analysis. While these approaches provide visibility into past performance, they offer limited insight into future outcomes.

ForecastIQ addresses this challenge by combining machine learning, probabilistic forecasting, optimization techniques, and business intelligence into a unified decision-support system.

The platform enables users to:

* Forecast future revenue
* Predict future ROAS
* Analyze campaign performance
* Simulate budget allocation scenarios
* Quantify uncertainty using probabilistic forecasting
* Detect campaign risks and anomalies
* Optimize marketing spend allocation
* Generate business-oriented recommendations

---

## Problem Statement

Marketing leaders are often required to answer questions such as:

* What revenue can be expected in the next planning cycle?
* Which campaigns are likely to generate the highest returns?
* How will revenue change if budgets are reallocated?
* Which channels present the highest risk?
* How confident should stakeholders be in forecast outcomes?

Traditional dashboards focus on historical reporting.

ForecastIQ focuses on future decision-making.

---

## Solution Overview

ForecastIQ provides four core capabilities:

### Forecast

Predict future Revenue and ROAS using machine learning models.

### Simulate

Evaluate the impact of different budget allocation strategies.

### Detect

Identify campaign risks and performance anomalies.

### Optimize

Recommend budget allocations designed to maximize forecasted business outcomes.

---

## System Architecture

```text
Marketing Data Sources
(Google Ads | Meta Ads | Microsoft Ads)
                     │
                     ▼
             Data Standardization
                     │
                     ▼
            Feature Engineering
                     │
                     ▼
          Revenue Forecast Model
                (XGBoost)
                     │
                     ├─────────────┐
                     ▼             ▼
           ROAS Forecast      Monte Carlo
               Model          Simulation
                     │             │
                     └──────┬──────┘
                            ▼
                  Budget Optimization
                            ▼
                  Insight Generation
                            ▼
                  Streamlit Dashboard
```

---

## Key Features

### Revenue Forecasting

Forecast future campaign and channel revenue using machine learning.

### ROAS Forecasting

Predict future Return on Ad Spend (ROAS).

### Campaign-Level Intelligence

Analyze forecast performance across individual campaigns.

### Campaign-Type Analysis

Evaluate forecast performance by campaign category.

### Budget Scenario Simulation

Simulate budget allocation changes and evaluate projected business impact.

Example:

```text
Google +20%
Meta -10%
Bing +15%
```

### Probabilistic Forecasting

Generate:

* P10 Revenue
* P50 Revenue
* P90 Revenue

to quantify uncertainty and support risk-aware planning.

### Risk Intelligence Center

Identify:

* Revenue anomalies
* Spend spikes
* ROAS volatility
* Campaign performance risks

### Budget Optimization

Recommend allocation strategies designed to maximize forecasted revenue.

### AI-Assisted Recommendations

Convert forecast outputs into actionable business insights.

---

## Model Performance

### Revenue Forecast Model

| Metric   | Value             |
| -------- | ----------------- |
| Model    | XGBoost Regressor |
| R² Score | 0.9356            |
| MAE      | 44.68             |

### ROAS Forecast Model

| Metric   | Value             |
| -------- | ----------------- |
| Model    | XGBoost Regressor |
| R² Score | 0.7922            |
| MAE      | 1.70              |

---
## Project Structure

```text
ForecastIQ/
│
├── app/
│   └── dashboard.py
│
├── src/
│   ├── generate_features.py
│   ├── feature_engineering.py
│   ├── predict.py
│   ├── train.py
│   ├── train_roas.py
│   ├── monte_carlo.py
│   ├── optimizer.py
│   ├── shap_analysis.py
│   └── preprocess.py
│
├── pickle/
│   ├── model.pkl
│   ├── revenue_model.pkl
│   ├── roas_model.pkl
│   ├── channel_encoder.pkl
│   └── campaign_encoder.pkl
│
├── data/                 # Input datasets
│
├── output/
│   └── predictions.csv
│
├── requirements.txt
├── run.sh
└── README.md
```

---

## How to Run ForecastIQ

### 1. Clone Repository

```bash
git clone https://github.com/Samhi1881/ForecastIQ.git
cd ForecastIQ
```

### 2. Create Virtual Environment

#### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Forecasting Pipeline

```bash
./run.sh ./data ./pickle/model.pkl ./output/predictions.csv
```

This command:

* Generates features from the input data
* Loads the trained forecasting model
* Generates revenue predictions
* Saves results to:

```text
output/predictions.csv
```

### 5. Launch Dashboard

```bash
streamlit run app/dashboard.py
```

Open:

```text
http://localhost:8501
```

---

## Hackathon Evaluation Command

The command expected for automated evaluation is:

```bash
./run.sh ./data ./pickle/model.pkl ./output/predictions.csv
```

Expected output:

```text
output/predictions.csv
```

This command is the primary entry point used for automated evaluation.

---

## Environment

* Python 3.11
* No internet access required during inference
* Trained models are included in the repository under `pickle/`
* Predictions are generated automatically from a single command

---

## Business Impact

ForecastIQ enables organizations to:

* Forecast Revenue
* Forecast ROAS
* Simulate Budget Scenarios
* Quantify Forecast Uncertainty
* Detect Campaign Risks
* Optimize Marketing Spend
* Improve Decision-Making Speed
* Increase Marketing ROI

---

## Author

**Gorantla Samhitha**