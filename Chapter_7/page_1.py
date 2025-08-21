import streamlit as st
import pandas as pd

st.title('Page One')
# Initializing session states for dataframe and slider
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'rows' not in st.session_state:
    st.session_state['rows'] = None
file = st.file_uploader('Upload file')
# Writing dataframe to session state
if file is not None:
    df = pd.read_csv(file)
    st.session_state['df'] = df
if st.session_state['df'] is not None:
    # Creating slider widget with default value from session state
    rows = st.slider('Rows to display',value=st.session_state['rows'], min_value=1,max_value=len(st.session_state['df']))
    # Writing slider value to session state
    st.session_state['rows'] = rows
    # Rendering dataframe from session state
    st.write(st.session_state['df'].iloc[:st.session_state['rows']])
