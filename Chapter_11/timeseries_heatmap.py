import pandas as pd 
import streamlit as st 
from datetime import datetime 
import plotly.express as px 
# Month-hours dictionary generator 
def month_hours_dict(): 
    month_hours = {} 
    month_names = ['January','February','March','April','May', 
    'June','July','August','September','October','November','December'] 
    for month_name in month_names: 
        month = {month_name: {'12AM': None, '01AM': None, '02AM': None, 
                                       '03AM': None, '04AM': None, '05AM': None, 
                                       '06AM': None, '07AM': None, '08AM': None, 
                                       '09AM': None, '10AM': None, '11AM': None, 
                                       '12PM': None, '01PM': None, '02PM': None, 
                                       '03PM': None, '04PM': None, '05PM': None, 
                                       '06PM': None, '07PM': None, '08PM': None, 
                                       '09PM': None, '10PM': None, '11PM': None}} 
        month_hours.update(month) 
    return month_hours 
# Aggregating data into monthly-hourly averages 
def aggregate(df, datetime_col, format): 
    df[datetime_col] = pd.to_datetime(df[datetime_col], format='%d/%m/%Y %H:%M') 
    for i in range(0,len(df)): 
        df.loc[i,'Month'] = df.loc[i][datetime_col].strftime('%B') 
        df.loc[i,'Hour'] = df.loc[i][datetime_col].strftime('%I%p') 
    return df.groupby(['Month','Hour'],sort=False,as_index=False).mean().round(4) 
# Plotly heatmap visualization 
def heatmap(df, month_hours, value_col): 
    for i in range(len(df)): 
        month_hours[df.iloc[i][0]][df.iloc[i][1]] = df.loc[i][value_col] 
    data_rows = list(month_hours.values()) 
    data = [] 
    for i in range(0,len(data_rows)): 
        data.append(list(data_rows[i].values())) 
    fig = px.imshow(data, 
                    labels=dict(x='Hour', y='Month', color='Value'), 
                                x=['12AM','01AM','02AM','03AM','04AM','05AM','06AM','07AM', 
                                '08AM','09AM','10AM','11AM', 
                                '12PM','01PM','02PM','03PM','04PM','05PM','06PM','07PM', 
                                '08PM','09PM','10PM','11PM'], 
                                y=['January','February','March','April','May','June','July', 
                                'August','September','October','November','December'] 
                                ) 
    st.write(fig) 
if __name__ == '__main__': 
    st.sidebar.title('Time-series Heatmap') 
    uploaded_file = st.sidebar.file_uploader('Upload a time-series dataset') 
    if uploaded_file is not None: 
        month_hours = month_hours_dict() 
        df = pd.read_csv(uploaded_file) 
        df_aggregate = aggregate(df, 'datetime', '%d/%m/%Y %H:%M') 
        heatmap(df_aggregate, month_hours, 'value') 
