import streamlit as st
import uuid
from datetime import datetime
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text

def get_session_id():
    if 'session_id' not in st.session_state:
        session_id = str(uuid.uuid4()).replace('-', '_')
        st.session_state.session_id = '_id_' + session_id
    return st.session_state.session_id

def insert_row(session_id, engine):
    with engine.connect() as conn:
        result = conn.execute(text(f'SELECT session_id FROM user_insights WHERE session_id = "{session_id}"')).fetchone()
        if result is None:
            conn.execute(text(f'INSERT INTO user_insights (session_id) VALUES ("{session_id}")'))
            conn.commit()

def update_row(column, new_value, session_id, mutable, engine):
    with engine.connect() as conn:
        if mutable:
            conn.execute(text(f'UPDATE user_insights SET {column} = "{new_value}" WHERE session_id = "{session_id}"'))
            conn.commit()
        else:
            result = conn.execute(text(f'SELECT {column} FROM user_insights WHERE session_id = "{session_id}"')).fetchone()
            if result and result[0] is None:
                conn.execute(text(f'UPDATE user_insights SET {column} = "{new_value}" WHERE session_id = "{session_id}"'))
                conn.commit()

if __name__ == '__main__':
    engine = create_engine('postgresql://<username>:<password>@localhost:<port>/<database>')
    session_id = get_session_id()
    with engine.connect() as conn:
        conn.execute(text('CREATE TABLE IF NOT EXISTS user_insights (session_id text, step_1 text, step_2 text, no_rows bigint)'))
        conn.commit()
    insert_row(session_id, engine)
    st.title('Hello world')
    st.subheader('Step 1')
    if st.button('Click'):
        st.write('Some content')
        update_row('step_1', datetime.now().strftime('%H:%M:%S %d/%m/%Y'), session_id, True, engine)
    st.subheader('Step 2')
    file = st.file_uploader('Upload data')
    if file is not None:
        df = pd.read_csv(file)
        st.write(df)
        update_row('step_2', datetime.now().strftime('%H:%M:%S %d/%m/%Y'), session_id, False, engine)
        update_row('no_rows', len(df), session_id, True, engine)
