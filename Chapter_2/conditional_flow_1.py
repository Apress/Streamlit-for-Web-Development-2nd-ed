import streamlit as st

# Function to display the name
def display_name(name):
    st.info(f'**Name:** {name}')

# Input for name
name = st.text_input('Please enter your name')

# Validation: If name is entered, show info; else, show an error message
if name:
    display_name(name)
else:
    st.error('No name entered')
