import streamlit as st
from datetime import datetime

st.title('Clock')

# Create an empty placeholder for time display
clock = st.empty()

# Infinite loop to continuously update the time
while True:
    time = datetime.now().strftime('%H:%M:%S')
    
    # Display the current time in the placeholder
    clock.info(f'**Current time:** {time}')
    
    if time > '21:19:15':
        # Clear the time display when the alarm condition is met and display the alarm
        clock.empty()
        st.warning('Alarm!!')        
        break
