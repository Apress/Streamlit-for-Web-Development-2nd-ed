import streamlit as st

st.title('Main Page')
# Initializing session state for page selection
if 'page_state' not in st.session_state:
    st.session_state['page_state'] = 'Main Page'
