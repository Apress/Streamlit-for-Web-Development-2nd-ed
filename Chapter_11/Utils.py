import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
import uuid
# Inserting new row in traffic insights table
def insert_row(session_id, engine):
    with engine.connect() as conn:
        if conn.execute(text(f"SELECT session_id FROM session_state WHERE session_id = '{session_id}'")).fetchone() is None:
            conn.execute(text(f"INSERT INTO session_state (session_id) VALUES ('{session_id}')"))
# Updating row in insights table
def update_row(column, new_value, session_id, engine):
    with engine.connect() as conn:
        if conn.execute(text(f"SELECT {column} FROM session_state WHERE session_id = '{session_id}'")).first()[0] is None:
            conn.execute(text(f"UPDATE session_state SET {column} = '{new_value}' WHERE session_id = '{session_id}'"))
# Session state function
def get_session():
    if 'session_id' not in st.session_state:
        session_id = str(uuid.uuid4())
        session_id = session_id.replace('-', '_')
        session_id = '_id_' + session_id
        st.session_state.session_id = session_id
    return st.session_state.session_id 
# File uploader function
def file_upload(name):
    uploaded_file = st.sidebar.file_uploader(name, key=name,
    accept_multiple_files=False)
    status = False
    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            status = True
            return status, uploaded_df
        except:
            try:
                uploaded_df = pd.read_excel(uploaded_file)
                status = True
                return status, uploaded_df
            except:
                st.error('Please ensure file is .csv or .xlsx format and/or reupload file')
                return status, None
    else:
        return status, None
@st.cache_resource
def db_engine(username, password, port):
    return create_engine(f'postgresql://{username}:{password}@localhost:{port}/')
