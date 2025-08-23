import numpy as np
import pandas as pd
import streamlit as st
from fastdtw import *
import plotly.express as px
from sklearn.metrics import r2_score
from scipy.spatial.distance import *
# Dynamic Time Warping synchronization function
def synchronize(df, datetime_col, reference, target):
    x = np.array(df[reference].fillna(0))
    y = np.array(df[target].fillna(0))
    distance, path = fastdtw(x, y)
    
    result = [
        [df[datetime_col].iloc[path[i][0]], df[reference].iloc[path[i][0]], df[target].iloc[path[i][1]]]
        for i in range(len(path))
    ]
    
    df_synchronized = pd.DataFrame(result, columns=[datetime_col, reference, target])
    df_synchronized = df_synchronized.drop_duplicates(subset=[datetime_col])
    
    return df_synchronized
# Plotly time-series visualization function
def timeseries_chart(df, datetime_col):
    df_columns = list(df)
    df[datetime_col] = pd.to_datetime(df[datetime_col],format='%d-%m-%y %H:%M')
    df = df.sort_values(by=datetime_col)
    fig = px.line(df, x=datetime_col, y=df_columns,
                  hover_data={datetime_col: '|%d-%m-%Y %H:%M'})
    st.write(fig)
if __name__ == '__main__':
    st.sidebar.title('Time-series Synchronization')
    uploaded_file = st.sidebar.file_uploader('Upload a time-series dataset')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file).dropna(subset=['datetime'])
        df_synchronized = synchronize(df, 'datetime', 'power', 'voltage')
        timeseries_chart(df, 'datetime')
        st.subheader(f'Correlation: {round(r2_score(df["power"], df["voltage"]), 3)}')
        timeseries_chart(df_synchronized, 'datetime')
        st.subheader(f'Correlation: {round(r2_score(df_synchronized["power"], df_synchronized["voltage"]), 3)}')
        st.download_button(
            label='Download synchronized data',
      data=df_synchronized.to_csv(index=False).encode('utf-8'),
            file_name='synchronized_data.csv',
            mime='text/csv')
