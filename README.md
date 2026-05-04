# ⚡ PJME Energy Demand Forecasting

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://energy-forecast-app-d3bt5b3gvqnapp4fzufybpw.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-CC0-green)

End-to-end time series forecasting and anomaly detection on 145,392 hourly energy observations (2002–2018) from the PJM East Interconnection grid. LSTM achieved **MAPE = 1.23%** (outstanding benchmark) — 89.3% better than SARIMA baseline.

🔗 **Live app:** [energy-forecast-app-d3bt5b3gvqnapp4fzufybpw.streamlit.app](https://energy-forecast-app-d3bt5b3gvqnapp4fzufybpw.streamlit.app)

---

## 📊 Model Results

| Model | MAE (MW) | RMSE (MW) | MAPE | Rating |
|---|---|---|---|---|
| SARIMA(1,0,1)(1,1,1,7) | 3,552 | 4,365 | 11.47% | Poor |
| Prophet (yearly + weekly + US holidays) | 2,568 | 3,361 | 8.13% | Acceptable |
| **LSTM (64+32 units, 24h lookback)** | **379** | **493** | **1.23%** | **Outstanding ✅** |

LSTM outperforms SARIMA by **89.3%** and Prophet by **84.9%**.

---

## 🚨 Anomaly Detection

Three methods applied across 16.6 years of data:

| Method | Anomalies | Period |
|---|---|---|
| Z-Score (3σ threshold) | 42 days | 2002–2018 |
| Isolation Forest (2% contamination) | 122 days | 2002–2018 |
| LSTM Prediction Error (3σ) | 182 hours | 2017–2018 |

**Key events detected:**
- 🔥 August 2006 Northeast heatwave — 52,230 MW (z=4.22)
- 🔥 July 2011 North American heat wave — 51,987 MW (z=4.14)
- 🥶 January 2018 bomb cyclone — polar vortex demand surge
- 🕐 March 2017 DST spring-forward — 3,520 MW prediction error

---

## 📋 Dataset

| Parameter | Value |
|---|---|
| Source | PJM Interconnection LLC via Kaggle |
| License | CC0 — Public Domain |
| Period | January 2002 — August 2018 |
| Observations | 145,392 hourly records |
| Features | Datetime, PJME_MW |
| Mean demand | 32,080 MW |
| Peak demand | 62,009 MW |

---

## 🔬 Methodology

```
Phase 1 → EDA
          3 seasonality layers confirmed:
          Daily (43% swing) · Weekly (13%) · Yearly (36%)

Phase 2 → Preprocessing
          DST duplicate removal · Missing hour interpolation
          ADF stationarity test (p≈0) · ACF/PACF analysis
          Train/test split: 93% / 7% (Jan 2002–Dec 2016 / Jan 2017–Aug 2018)

Phase 3 → Forecasting (3 models)
          SARIMA(1,0,1)(1,1,1,7) · Prophet · LSTM

Phase 4 → Anomaly Detection
          Z-Score · Isolation Forest · LSTM prediction error

Phase 5 → Model comparison
          MAE · RMSE · MAPE · benchmark classification

Phase 6 → Streamlit deployment
          6 interactive pages · live on Streamlit Cloud
```

---

## 🖥️ Streamlit App — 6 Pages

| Page | Description |
|---|---|
| Overview | Project summary and model results table |
| EDA | 16-year time series, day-of-week, monthly seasonality |
| Forecast | Interactive SARIMA vs Prophet vs LSTM comparison |
| Anomaly Detection | Z-score and LSTM error methods with toggle |
| Model Comparison | MAE, RMSE, MAPE bar charts + benchmark table |
| Predict | Interactive 30-day Prophet forecast with confidence intervals |

---

## 🛠️ Tech Stack

```
Python · Streamlit · Plotly · Prophet · LSTM (TensorFlow/Keras)
SARIMA (statsmodels) · Isolation Forest (scikit-learn)
Pandas · NumPy · Joblib
```

---

## 💡 Methodology Note

> This forecasting pipeline is directly transferable to **telecom network traffic forecasting**, retail demand planning, and IoT sensor monitoring — any domain with temporal patterns and seasonality.

---

## 📁 Repository Structure

```
energy-forecast-app/
├── app.py                    ← Streamlit main page
├── requirements.txt
├── models/                   ← Pre-computed forecasts + models
│   ├── df_daily.csv
│   ├── sarima_forecast.csv
│   ├── prophet_forecast.csv
│   ├── lstm_forecast.csv
│   ├── zscore_anomalies.csv
│   ├── lstm_anomalies.csv
│   └── model_results.csv
└── pages/
    ├── 1_EDA.py
    ├── 2_Forecast.py
    ├── 3_Anomaly_Detection.py
    ├── 4_Model_Comparison.py
    └── 5_Predict.py
```

---

## 📖 Citation

```
PJM Interconnection LLC. PJME Hourly Energy Consumption.
Kaggle, 2018. License: CC0 Public Domain.
kaggle.com/datasets/robikscube/hourly-energy-consumption
```

---

## 👤 Author

**Jean Fred A. Williama**
Senior RF Engineer → Data Scientist | Panama

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/jean-fred-a-williama-36905315/)
[![GitHub](https://img.shields.io/badge/GitHub-JeanAndre376-black)](https://github.com/JeanAndre376/)
