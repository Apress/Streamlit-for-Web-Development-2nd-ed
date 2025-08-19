import streamlit as st
from Streamlit.Views import FeedView, AddPostView
from Flask.Services import get_feed, add_post

AddPostView(add_post)
st.write("___")
FeedView(get_feed)

