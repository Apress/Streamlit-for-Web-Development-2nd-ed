import streamlit as st
from rating_stars import rating_stars
st.title('Rating stars demo!')
total_stars = st.slider(label='Total Stars', min_value=0, max_value=20, value=10, step=1) 
selected_stars = rating_stars(total_stars)
st.write(str(selected_stars) + ' star(s) have been selected')
