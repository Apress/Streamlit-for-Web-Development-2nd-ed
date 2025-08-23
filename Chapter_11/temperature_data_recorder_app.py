import serial
import time
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
# Plotly temperature gauge visualization function
def temperature_gauge(temperature, previous_temperature, gauge_placeholder):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = temperature,
        mode = 'gauge+number+delta',
        title = {'text': 'Temperature (C) '},
        delta = {'reference': previous_temperature},
        gauge = {'axis': {'range': [0, 40]}}))
    fig.update_layout(
        width=300,
    )
    gauge_placeholder.write(fig)
# Plotly time-series temperature visualization
def temperature_chart(df, chart_placeholder):
    fig = px.line(df, x='Time', y='Temperature (C)')
    chart_placeholder.write(fig)
if __name__ == '__main__':
    st.sidebar.title('Temperature Data Recorder')
    recording = False
    # End date and time form for temperature recording
    with st.sidebar.form('form_1'):
        col1, col2, = st.columns(2)
        with col1:
            end_date = st.date_input('Recording end date')
        with col2:
            end_time = st.time_input('Recording end time')
        if st.form_submit_button('Start recording'):
            recording = True
            arduino = serial.Serial(port='COM4', baudrate=9600)
    previous_temperature = 0
    temperature_record = pd.DataFrame(columns=['Time','Temperature (C)'])
    gauge_placeholder = st.sidebar.empty()
    chart_placeholder = st.empty()
    # Recording data while current date and time is less than specified end
    while recording and (datetime.now() < datetime.combine(end_date, end_time)):
        current_time = datetime.now().strftime('%H:%M:%S')
        temperature = round(float(arduino.readline().decode().strip('\r\n')),1)
        temperature_record.loc[len(temperature_record),
        ['Time','Temperature (C)']] = [current_time, temperature]
        temperature_gauge(temperature, previous_temperature, gauge_placeholder)
        temperature_chart(temperature_record, chart_placeholder)
        time.sleep(1)
        previous_temperature = temperature
    # Display and download temperature date if end date and time exceeded
    if recording and (datetime.now() > datetime.combine(end_date, end_time)):
        arduino.close()
        if len(temperature_record) > 0:
            st.write(temperature_record)
            st.download_button(
                label='Download data',
                data=temperature_record.to_csv(index=False).encode('utf-8'),
                file_name='temperature_record.csv',
                mime='text/csv',
            )
        else:
            st.warning('Please select a future end date and time')
