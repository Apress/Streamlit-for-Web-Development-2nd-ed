import streamlit as st
from PIL import Image

icon = Image.open('favicon.ico')

# Page configuration
st.set_page_config(
    page_title='Hello World',
    page_icon=icon,
    layout='centered',
    initial_sidebar_state='auto',
    menu_items={
        'Get Help': 'https://streamlit.io/',
        'Report a bug': 'https://github.com',
        'About': 'About your application: **Hello World**'
    }
)

# Set up titles
title = 'Hello World'
st.sidebar.title(title)
st.title(title)
