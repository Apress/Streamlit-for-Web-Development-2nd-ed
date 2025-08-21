import streamlit as st

# Function to display the name
def display_name(name):
    st.info(f'**Name:** {name}')

# Input for name
name = st.text_input('Please enter your name')

# Check if name is entered
if not name:
    st.error('No name entered')
else:
    display_name(name)
