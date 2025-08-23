import serial
import pygame as pg
import streamlit as st
import plotly.graph_objects as go
import time
# Plotly speed gauge visualization function
def speed_gauge(target_speed, placeholder):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = int(target_speed)-90,
        mode = 'gauge+number+delta',
        title = {'text': 'Speed'},
        delta = {'reference': 0},
        gauge = {'axis': {'range': [-30, 30]}}))
    placeholder.write(fig)
if __name__ == '__main__':
    st.sidebar.title('Motor Command & Control')
    info_bar = st.empty()
    speedometer = st.empty()
    # Create Arduino serial client
    arduino = serial.Serial(port='COM5', baudrate=9600)
    # Create PyGame client
    pg.init()
    # Create a list of available joysticks to initialize
    joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()
    if st.sidebar.button('Start motor'):
        info_bar.info('Motor started')
        # Connect to Arduino
        try:
            arduino.open()
        except Exception as e:
            print(e)
        if st.sidebar.button('Stop motor'):
            info_bar.warning('Motor stopped')
            arduino.write(bytes('90' +'\n', 'utf-8'))
            arduino.close()
            pg.quit()
        while True:
            # Report all joystick events
            for event in pg.event.get():
                print(event)
            for joystick in joysticks:
                if joystick.get_id() == 0: # Access the first connected joystick
                    axes = joystick.get_numaxes()
                    for x in range(axes): # Check all inputs of the joystick
                        target_speed = str(int(((joystick.get_axis(1)*-1)*30 + 90)))
                        press = joystick.get_button(0)
                        time.sleep(0.01)
            arduino.flushInput()
            arduino.flushOutput()
            arduino.flush()
            arduino.write(bytes(target_speed +'\n', 'utf-8')) # Send speed to Arduino
            speed_gauge(target_speed, speedometer)
            # Disconnect Arduino if joystick button pressed
            if press == 1:
                try:
                    arduino.write(bytes('90' +'\n', 'utf-8'))
                    arduino.close()
                except Exception as e:
                    print(e)
                break
    # Disconnect Arduino if 'Stop motor' button pressed
    info_bar.warning('Motor stopped')
    try:
        arduino.write(bytes('90' +'\n', 'utf-8'))
        arduino.close()
    except Exception as e:
        print(e)
    pg.quit()
