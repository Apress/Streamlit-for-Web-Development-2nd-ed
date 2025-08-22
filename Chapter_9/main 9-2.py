import os 
import platform 
import streamlit as st 

st.title(f'Deployed on {platform.system()} ({os.name})') st.subheader('More details: ') st.write(f'_{platform.platform()}_')
