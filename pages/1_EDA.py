import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")
st.title("📊 Exploratory Data Analysis")

df = pd.read_csv('models/df_daily.csv',
                 index_col=0, parse_dates=True)
df.columns = ['PJME_MW']

st.markdown(f"**Dataset:** {len(df):,} daily observations · "
            f"{df.index.min().year} to {df.index.max().year}")
st.markdown("---")

# Full time series
fig1 = px.line(df, y='PJME_MW',
               title='PJME Daily Energy Demand — Full 16-year period',
               color_discrete_sequence=['#1D9E75'])
fig1.update_layout(yaxis_title='Energy (MW)')
st.plotly_chart(fig1, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # Weekly pattern instead of hourly
    # (daily data has no hour info)
    df['dayofweek'] = df.index.dayofweek
    daily = df.groupby('dayofweek')['PJME_MW'].mean().reset_index()
    days  = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    daily['day_name'] = daily['dayofweek'].apply(lambda x: days[x])
    fig2 = px.bar(daily, x='day_name', y='PJME_MW',
                  title='Average demand by day of week',
                  color_discrete_sequence=['#D85A30'])
    fig2.update_layout(yaxis_title='Avg Energy (MW)')
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    # Monthly pattern
    df['month'] = df.index.month
    monthly = df.groupby('month')['PJME_MW'].mean().reset_index()
    months  = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']
    monthly['month_name'] = monthly['month'].apply(
        lambda x: months[x-1])
    fig3 = px.bar(monthly, x='month_name', y='PJME_MW',
                  title='Average demand by month',
                  color='PJME_MW',
                  color_continuous_scale=['#1D9E75','#D85A30'])
    fig3.update_layout(yaxis_title='Avg Energy (MW)')
    st.plotly_chart(fig3, use_container_width=True)

# Key stats
st.markdown("---")
st.subheader("Key Statistics")
col3, col4, col5, col6 = st.columns(4)
col3.metric("Mean demand",  f"{df['PJME_MW'].mean():,.0f} MW")
col4.metric("Peak demand",  f"{df['PJME_MW'].max():,.0f} MW")
col5.metric("Min demand",   f"{df['PJME_MW'].min():,.0f} MW")
col6.metric("Std deviation",f"{df['PJME_MW'].std():,.0f} MW")