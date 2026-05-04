import streamlit as st

st.set_page_config(
    page_title="Energy Demand Forecaster",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ PJME Energy Demand Forecasting")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Dataset",        "PJME Hourly")
col2.metric("Period",         "2002 — 2018")
col3.metric("Best Model",     "LSTM")
col4.metric("LSTM MAPE",      "1.23%")

st.markdown("---")
st.markdown("""
### ⚡ Project Overview
This app presents an end-to-end time series forecasting
analysis of hourly energy demand from the PJM East
interconnection grid — 145,392 hourly observations
spanning 16.6 years.

**Navigate using the sidebar:**
- 📊 **EDA** — dataset exploration and seasonality analysis
- 🔮 **Forecast** — SARIMA vs Prophet vs LSTM predictions
- 🚨 **Anomaly Detection** — heatwaves, polar vortex, DST events
- 📈 **Model Comparison** — MAE, RMSE, MAPE comparison
- ⚡ **Predict** — forecast next 30 days interactively

---
### 🏆 Model Results
| Model | MAE (MW) | RMSE (MW) | MAPE |
|---|---|---|---|
| SARIMA | 3,552 | 4,365 | 11.47% |
| Prophet | 2,568 | 3,361 | 8.13% |
| **LSTM** | **379** | **493** | **1.23%** |

---
### 💡 Methodology Note
> The forecasting pipeline demonstrated here is directly
> transferable to telecom network traffic, retail demand
> planning, and IoT sensor monitoring — any domain with
> temporal patterns and seasonality.
""")

st.sidebar.success("Select a page above to get started.")