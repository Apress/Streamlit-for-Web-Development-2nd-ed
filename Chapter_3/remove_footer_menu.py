# Custom CSS to hide header and footer
hide_streamlit_style = """
    <style>
    /* Hide Streamlit header */
    header {
        visibility: hidden;
    }
    /* Hide Streamlit footer */
    footer {
        visibility: hidden;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
