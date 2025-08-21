import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout='wide')
st.title('User Insights')
df = pd.read_excel('C:/Users/.../user_insights.xlsx')
column_selection = st.selectbox('Select column', df.columns[1:-2])
df = df[column_selection]
df = pd.to_datetime(df,format='%H:%M:%S %d/%m/%Y')
df_1h = df.copy()
df_1d = df.copy()
col1, col2 = st.columns(2)
with col1:
    st.subheader('Hourly chart')
    df_1h = df_1h.dt.strftime('%Y-%m-%d %I%p')
    df_1h = pd.DataFrame(df_1h.value_counts())
    df_1h.index = pd.DatetimeIndex(df_1h.index)
    df_1h = df_1h.sort_index()
    fig = px.bar(df_1h, x=df_1h.index, y=df_1h[column_selection])
    st.write(fig)
with col2:
    st.subheader('Daily chart')
    df_1d = df_1d.dt.strftime('%Y-%m-%d')
    df_1d = pd.DataFrame(df_1d.value_counts())
    df_1d.index = pd.DatetimeIndex(df_1d.index)
    df_1d = df_1d.sort_index()
    fig = px.line(df_1d, x=df_1d.index, y=df_1d[column_selection])
    st.write(fig)
