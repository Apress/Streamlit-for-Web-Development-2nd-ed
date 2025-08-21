import streamlit as st

# Determine the current page
current_page = st.query_params.get('page', ['home'])

# Display the correct content based on the page
if current_page == 'home':
    st.title('Home Page')
elif current_page == 'contact':
    st.title('Contact Page')

# Add links to navigate between sub URLs
st.sidebar.title('Pages')
if st.sidebar.button('Home'):
    st.query_params['page'] = 'home'
    st.rerun()
if st.sidebar.button('Contact'):
    st.query_params['page'] = 'contact'
    st.rerun()
