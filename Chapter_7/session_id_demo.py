import streamlit as st
import uuid

# Check if session ID already exists, if not, create one
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Access and display the session ID
st.title('Your session ID is:')
st.subheader(st.session_state.session_id)
