import streamlit as st

pg = st.navigation([st.Page('home.py', title='🏠 Home'),
                    st.Page('contact_us.py', title='📞 Contact us')])
pg.run()
