import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Model Comparison",
                   page_icon="📈", layout="wide")
st.title("📈 Model Comparison")

results = pd.read_csv('models/model_results.csv')

col1, col2, col3 = st.columns(3)

# MAE chart
fig1 = px.bar(results, x='Model', y='MAE_MW',
              color='Model',
              color_discrete_map={'SARIMA':'#888780',
                                  'Prophet':'#534AB7',
                                  'LSTM':'#1D9E75'},
              title='MAE — lower is better',
              text='MAE_MW')
fig1.update_traces(texttemplate='%{text:,.0f}',
                   textposition='outside')
fig1.update_layout(showlegend=False)
col1.plotly_chart(fig1, use_container_width=True)

# RMSE chart
fig2 = px.bar(results, x='Model', y='RMSE_MW',
              color='Model',
              color_discrete_map={'SARIMA':'#888780',
                                  'Prophet':'#534AB7',
                                  'LSTM':'#1D9E75'},
              title='RMSE — lower is better',
              text='RMSE_MW')
fig2.update_traces(texttemplate='%{text:,.0f}',
                   textposition='outside')
fig2.update_layout(showlegend=False)
col2.plotly_chart(fig2, use_container_width=True)

# MAPE chart
fig3 = px.bar(results, x='Model', y='MAPE_pct',
              color='Model',
              color_discrete_map={'SARIMA':'#888780',
                                  'Prophet':'#534AB7',
                                  'LSTM':'#1D9E75'},
              title='MAPE % — lower is better',
              text='MAPE_pct')
fig3.update_traces(texttemplate='%{text:.2f}%',
                   textposition='outside')
fig3.update_layout(showlegend=False)
col3.plotly_chart(fig3, use_container_width=True)

# Summary table
st.markdown("---")
st.subheader("Complete results table")
def highlight_lstm(row):
    if row['Model'] == 'LSTM':
        return ['background-color: #1D9E75; color: white; font-weight: bold'] * len(row)
    return [''] * len(row)

st.dataframe(
    results.style.apply(highlight_lstm, axis=1),
    use_container_width=True)

# MAPE benchmark
st.markdown("---")
st.subheader("MAPE benchmark")
benchmarks = pd.DataFrame({
    'MAPE range': ['>10%', '5-10%', '3-5%',
                   '1-3%', '<1%'],
    'Rating':     ['Poor', 'Acceptable', 'Good',
                   'Excellent', 'Outstanding'],
    'Your models':['SARIMA (11.47%)', '', '',
                   'LSTM (1.23%)', '']
})
st.dataframe(benchmarks, use_container_width=True,
             hide_index=True)