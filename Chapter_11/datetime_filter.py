import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.express as px
# Streamlit slider function used to truncate leading and trailing edges of dataset
def datetime_filter(datetime_col, df, format):
    lead, trail = st.sidebar.slider('Date-time filter', 0, len(df)-1, [0,len(df)-1], 1)
    df[datetime_col] = pd.to_datetime(df[datetime_col], format=format)
    sd = df.loc[lead][datetime_col].strftime('%d %b %Y, %I:%M%p')
    ed = df.loc[trail][datetime_col].strftime('%d %b %Y, %I:%M%p')
    st.sidebar.info(f'Start: **{sd}**')
    st.sidebar.info(f'End: **{ed}**')
    filtered_df = df.iloc[lead:trail+1][:]
    return filtered_df
# Plotly time-series visualization function
def timeseries_chart(df, datetime_col, value_col):
    df[datetime_col] = df[datetime_col].dt.strftime(' %H:%M on %B %-d, %Y')
    df = df.sort_values(by=datetime_col)
    fig = px.line(df, x=datetime_col, y=value_col,
                  hover_data={datetime_col: '|%d/%m/%Y %H:%M'})
    st.write(fig)
if __name__ == '__main__':
    st.sidebar.title('Date-time Filter')
    uploaded_file = st.sidebar.file_uploader('Upload a time-series dataset')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df_filtered = datetime_filter('datetime', df, '%d/%m/%Y %H:%M')
        st.header('Filtered Chart')
        timeseries_chart(df_filtered, 'datetime', 'value')
        st.download_button(
             label='Download filtered data',
             data=df_filtered.to_csv(index=False).encode('utf-8'),
             file_name='filtered_data.csv',
             mime='text/csv',
        )
