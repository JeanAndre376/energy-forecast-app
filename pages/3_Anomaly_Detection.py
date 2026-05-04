import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Anomaly Detection",
                   page_icon="🚨", layout="wide")
st.title("🚨 Anomaly Detection")

df      = pd.read_csv('models/df_daily.csv',
                      index_col=0, parse_dates=True)
df.columns = ['PJME_MW']
zscore  = pd.read_csv('models/zscore_anomalies.csv',
                      index_col=0, parse_dates=True)
errors  = pd.read_csv('models/lstm_errors.csv',
                      index_col=0, parse_dates=True)
lstm_an = pd.read_csv('models/lstm_anomalies.csv',
                      index_col=0, parse_dates=True)

method = st.sidebar.radio("Detection method",
    ["Z-Score", "LSTM Prediction Error"])

st.markdown("---")

if method == "Z-Score":
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['PJME_MW'],
        name='Daily demand',
        line=dict(color='#1D9E75', width=0.8),
        opacity=0.8))
    fig.add_trace(go.Scatter(
        x=zscore.index,
        y=df.loc[zscore.index, 'PJME_MW'],
        mode='markers',
        name=f'Anomalies ({len(zscore)})',
        marker=dict(color='#D85A30', size=8)))
    fig.update_layout(
        title='Z-Score Anomaly Detection — 16 years',
        yaxis_title='Energy (MW)', height=450)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top anomaly events")
    st.dataframe(zscore.sort_values(
        by=zscore.columns[0], ascending=False).head(10))

else:
    threshold = errors.iloc[:,0].mean() + \
                3 * errors.iloc[:,0].std()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=errors.index, y=errors.iloc[:,0],
        name='Prediction error',
        line=dict(color='#888780', width=0.8)))
    fig.add_hline(y=threshold,
                  line_dash='dash', line_color='#D85A30',
                  annotation_text='3σ threshold')
    fig.add_trace(go.Scatter(
        x=lstm_an.index, y=lstm_an.iloc[:,0],
        mode='markers',
        name=f'Anomalies ({len(lstm_an)})',
        marker=dict(color='#D85A30', size=8)))
    fig.update_layout(
        title='LSTM Prediction Error Anomalies',
        yaxis_title='Absolute Error (MW)', height=450)
    st.plotly_chart(fig, use_container_width=True)

# Key events
st.markdown("---")
st.subheader("Known anomaly events")
events = {
    'Event': ['August 2006 heatwave', 'July 2011 heat wave',
              'Jan 2018 bomb cyclone', 'March 2017 DST',
              'Feb 2015 polar vortex'],
    'Date':  ['2006-08-02', '2011-07-22',
              '2018-01-04', '2017-03-12', '2015-02-20'],
    'MW':    [52230, 51987, 44198, 40600, 44694],
    'Type':  ['Heatwave', 'Heatwave', 'Cold snap',
              'DST disruption', 'Polar vortex']
}
st.dataframe(pd.DataFrame(events), use_container_width=True)