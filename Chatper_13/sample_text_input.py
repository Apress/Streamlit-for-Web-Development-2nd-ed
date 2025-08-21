import streamlit as st

st.title('LLMs in Streamlit')
text = st.text_area('Write prompt here')
sent = st.button('Send')
if sent:
   output = 'Dummy Output' # Replace with LLM call
   st.text(output)
