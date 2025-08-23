import streamlit as st
from Utils import *
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import config # config.py not to be mixed with config.yaml
with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Importing pages
from lr import lr_main
def main(engine):
    # Creating pages dictionary
    pages_ml_classifier = {
        'Logistic Regression Classifier': lr_main
        }
    # Creating pages menu
    st.sidebar.subheader('Menu')
    ml_module_selection = st.sidebar.selectbox('Select Classifier',
    ['Logistic Regression Classifier'])
    # Creating dataset uploader widgets
    if 'df_train' not in st.session_state:
        st.session_state['df_train'] = None
    if 'df_real' not in st.session_state:
        st.session_state['df_real'] = None
    st.sidebar.subheader('Training Dataset')
    _, st.session_state['df_train'] = file_upload('Please upload a training dataset')
    st.sidebar.subheader('Test Dataset')
    _, st.session_state['df_real'] = file_upload('Please upload a test dataset')
    # Running selected page
    pages_ml_classifier[ml_module_selection](engine)
if __name__ == '__main__':
    # Creating PostgreSQL client for insights database
    username = config.database_credentials['username']
    password = config.database_credentials['password']
    port = config.database_credentials['port']
    engine = db_engine(username, password, port)
    # Creating user authentication object
    authenticator = stauth.Authenticate(config.user_credentials['names'],
    config.user_credentials['usernames'], config.user_credentials['passwords'],
    'some_cookie_name','some_signature_key', cookie_expiry_days=30)
    # Displaying login bar
    try:
		authenticator.login()
	 except Exception as e:
		st.error(e)
    if st.session_state['authentication_status']:
        authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{st.session_state["name"]}*')
        main(engine)
    elif st.session_state['authentication_status'] == False:
        st.sidebar.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] == None:
        st.sidebar.warning('Please enter your username and password')
