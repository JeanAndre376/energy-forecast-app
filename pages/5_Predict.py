import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from prophet import Prophet

st.set_page_config(page_title="Predict",
                   page_icon="⚡", layout="wide")
st.title("⚡ Interactive Forecast — Next N Days")

st.markdown("Use Prophet to forecast energy demand "
            "for a selected number of days ahead.")

# Load historical data
df = pd.read_csv('models/df_daily.csv',
                 index_col=0, parse_dates=True)
df.columns = ['PJME_MW']

# Sidebar controls
st.sidebar.header("Forecast settings")
n_days = st.sidebar.slider("Forecast horizon (days)",
                             7, 90, 30)
show_history = st.sidebar.slider("Show history (days)",
                                  30, 365, 90)

if st.sidebar.button("Generate forecast", type="primary"):
    with st.spinner("Training Prophet model..."):
        # Prepare data
        df_prophet = df.reset_index()
        df_prophet.columns = ['ds', 'y']

        # Fit model
        m = Prophet(yearly_seasonality=True,
                    weekly_seasonality=True,
                    daily_seasonality=False)
        m.add_country_holidays(country_name='US')
        m.fit(df_prophet)

        # Forecast
        future = m.make_future_dataframe(
            periods=n_days, freq='D')
        forecast = m.predict(future)

        # Plot
        history_start = df.index[-show_history]
        hist = df[df.index >= history_start]
        future_fc = forecast[
            forecast['ds'] > df.index[-1]]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist['PJME_MW'],
            name='Historical', line=dict(
                color='#1D9E75', width=2)))
        fig.add_trace(go.Scatter(
            x=future_fc['ds'], y=future_fc['yhat'],
            name=f'Forecast ({n_days} days)',
            line=dict(color='#D85A30',
                      dash='dash', width=2)))
        fig.add_trace(go.Scatter(
            x=pd.concat([future_fc['ds'],
                         future_fc['ds'][::-1]]),
            y=pd.concat([future_fc['yhat_upper'],
                         future_fc['yhat_lower'][::-1]]),
            fill='toself', fillcolor='rgba(216,90,48,0.15)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% confidence interval'))

        fig.update_layout(
            title=f'Energy demand forecast — next {n_days} days',
            yaxis_title='Energy (MW)',
            height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Show forecast table
        st.subheader("Forecast values")
        fc_table = future_fc[['ds','yhat',
                               'yhat_lower',
                               'yhat_upper']].copy()
        fc_table.columns = ['Date', 'Forecast (MW)',
                             'Lower bound', 'Upper bound']
        fc_table = fc_table.round(0)
        st.dataframe(fc_table, use_container_width=True,
                     hide_index=True)
else:
    st.info("👈 Set parameters in the sidebar "
            "and click 'Generate forecast'")