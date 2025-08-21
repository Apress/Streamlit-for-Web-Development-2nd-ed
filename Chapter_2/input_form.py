import streamlit as st
from datetime import date  # Import to use the current date

# Create a feedback form
with st.form('feedback_form'):
    st.header('Feedback Form')
    
    # Organize form inputs into columns
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input('Please enter your name', placeholder='Your full name')
        rating = st.slider('Rate this app (0 = Worst, 10 = Best)', 0, 10, 5)
    with col2:
        dob = st.date_input('Enter your date of birth')
        recommend = st.radio('Would you recommend this app to others?', ('Yes', 'No'))
    
    # Submit button
    submit_button = st.form_submit_button('Submit')

# Handle form submission
if submit_button:
    # Check for empty name
    if not name.strip():
        st.error('Name cannot be empty. Please provide your name.')
    # Check for valid date of birth
    elif dob > date.today():
        st.error('Date of birth cannot be in the future.')
    else:
        st.success('Thank you for your feedback!')
        st.write('**Name:**', name)
        st.write('**Date of Birth:**', dob)
        st.write('**Rating:**', rating)
        st.write('**Would Recommend?:**', recommend)
