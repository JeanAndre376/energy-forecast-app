import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Forecast",
                   page_icon="🔮", layout="wide")
st.title("🔮 Forecast — SARIMA vs Prophet vs LSTM")

# Load data
test    = pd.read_csv('models/test_daily.csv',
                      index_col=0, parse_dates=True)
sarima  = pd.read_csv('models/sarima_forecast.csv',
                      index_col=0, parse_dates=True)
prophet = pd.read_csv('models/prophet_forecast.csv',
                      index_col=0, parse_dates=True)
lstm_f  = pd.read_csv('models/lstm_forecast.csv',
                      index_col=0, parse_dates=True)

test.columns    = ['Actual']
sarima.columns  = ['SARIMA']
prophet.columns = ['Prophet']
lstm_f.columns  = ['LSTM']

# Resample lstm to daily
lstm_daily = lstm_f.resample('D').mean()

# Sidebar controls
st.sidebar.header("Display options")
show_sarima  = st.sidebar.checkbox("Show SARIMA",  True)
show_prophet = st.sidebar.checkbox("Show Prophet", True)
show_lstm    = st.sidebar.checkbox("Show LSTM",    True)
n_days = st.sidebar.slider("Days to show", 30, 365, 90)

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=test.index[:n_days], y=test['Actual'][:n_days],
    name='Actual', line=dict(color='#FF6B00', width=2.5)))

if show_sarima:
    fig.add_trace(go.Scatter(
        x=sarima.index[:n_days], y=sarima['SARIMA'][:n_days],
        name='SARIMA (MAPE=11.47%)',
        line=dict(color='#888780', dash='dash')))

if show_prophet:
    fig.add_trace(go.Scatter(
        x=prophet.index[:n_days], y=prophet['Prophet'][:n_days],
        name='Prophet (MAPE=8.13%)',
        line=dict(color='#A855F7', dash='dash', width=2)))

if show_lstm:
    fig.add_trace(go.Scatter(
        x=lstm_daily.index[:n_days], y=lstm_daily['LSTM'][:n_days],
        name='LSTM (MAPE=1.23%)',
        line=dict(color='#00FF88', dash='dash', width=2.5)))

fig.update_layout(
    title=f'Forecast comparison — first {n_days} days',
    yaxis_title='Energy (MW)',
    height=500,
    plot_bgcolor='rgba(0,0,0,0)',  # transparent background
    legend=dict(
        bgcolor='rgba(0,0,0,0.3)',
        bordercolor='white',
        borderwidth=1,
        font=dict(size=12)
    )
)
st.plotly_chart(fig, use_container_width=True)

# Metrics
st.markdown("---")
st.subheader("Model Performance")
col1, col2, col3 = st.columns(3)
col1.metric("SARIMA MAPE", "11.47%", delta="baseline")
col2.metric("Prophet MAPE", "8.13%",
            delta="-3.34pp vs SARIMA", delta_color="inverse")
col3.metric("LSTM MAPE", "1.23%",
            delta="-10.24pp vs SARIMA", delta_color="inverse")
