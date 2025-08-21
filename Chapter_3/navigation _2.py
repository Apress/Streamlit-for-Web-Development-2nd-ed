import streamlit as st

pages = {
    '🏠 Home': [
        st.Page('home.py', title='Home')
    ],
    '📞 Contact us': [
        st.Page('contact_us/message.py', title='Message'),
        st.Page('contact_us/address.py', title='Address'),
    ],
}

pg = st.navigation(pages)
pg.run()
