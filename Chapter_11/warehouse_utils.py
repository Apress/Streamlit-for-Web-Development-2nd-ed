from sqlalchemy import create_engine, text
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import plotly.express as px
# Function to create a new database
def create_database(database_name, connection):
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    try:
        cursor.execute(f"""CREATE DATABASE {'warehouse_db_' + database_name} WITH OWNER = postgres ENCODING =
        'UTF8' CONNECTION LIMIT = -1;""")
        cursor.close()
        return True
    except:
        return False
# Function to return a list of databases
def read_databases(engine):
    with engine.connect() as conn:
        result = conn.execute(text('SELECT datname FROM pg_database'))
        result = [x[0].replace('warehouse_db_', '') for x in result
        if 'warehouse_db_' in x[0]]
        return result
# Function to rename a selected database
def update_database(database_name_old, database_name_new, connection):
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    try:
        cursor.execute(f"""SELECT pg_terminate_backend (pg_stat_activity.pid)
        FROM pg_stat_activity WHERE pg_stat_activity.datname = '{"warehouse_db_" + database_name_old}';""")
        cursor.execute(f"""ALTER DATABASE {'warehouse_db_' + database_name_old} RENAME TO {'warehouse_db_' + database_name_new};""")
        cursor.close()
        return True
    except Exception as e:
        print(e)
# Function to delete a selected database
def delete_database(database_name, connection):
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    try:
        cursor.execute(f"""SELECT pg_terminate_backend (pg_stat_activity.pid)
        FROM pg_stat_activity WHERE pg_stat_activity.datname = '{"warehouse_db_" + database_name}';""")
        cursor.execute(f"""DROP DATABASE {'warehouse_db_' + database_name};""")
        cursor.close()
        return True
    except Exception as e:
        print(e)
# Function to create a table in the selected database
def create_table(table_name, table, engine):
    table.to_sql(table_name, engine, index=False, if_exists='replace', chunksize=1000)
# Function to return a list of tables in the selected database
def list_tables(engine):
    with engine.connect() as conn:
        tables = conn.execute(text("""SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public' ORDER BY table_name;""")).fetchall()
        return [x[0] for x in tables]
# Function to read the selected table within the selected database
def read_table(table_name, engine):
    try:
        return pd.read_sql_table(table_name,engine)
    except Exception as e:
        print(e)
# Function to delete the selected table within the selected database
def delete_table(table_name, engine):
    with engine.begin() as conn:
        conn.execute(text(f'DROP TABLE IF EXISTS "{table_name}"'))
# Function to render an interactive 'create, read, update and delete' table
def crud(table_name, engine):
    df = read_table(table_name, engine)
    df = df.fillna('None')
    index = len(df)
    # Initiate the streamlit-aggrid widget
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True,
     aggFunc='sum', editable=True)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridOptions = gb.build()
    # Insert the dataframe into the widget
    df_new = AgGrid(df,gridOptions=gridOptions,enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED)
    # Add a new row to the widget
    if st.button('-----------Add a new row-----------'):
        df_new['data'].loc[index,:] = 'None'
        create_table(table_name, df_new['data'], engine)
        st.rerun()
    # Save the dataframe to disk if the widget has been modified
    if df.equals(df_new['data']) is False:
        create_table(table_name, df_new['data'], engine)
        st.rerun()
    # Remove selected rows from the widget
    if st.button('-----------Remove selected rows-----------'):
        if len(df_new['selected_rows']) > 0:
            exclude = pd.DataFrame(df_new['selected_rows'])
            create_table(table_name, pd.merge(df_new['data'], exclude, how='outer',
            indicator=True).query('_merge == "left_only"').drop('_merge', 1), engine)
            st.rerun()
        else:
            st.warning('Please select at least one row')
    # Check for duplicate rows
    if df_new['data'].duplicated().sum() > 0:
        st.warning(f'**Number of duplicate rows:** { df_new['data'].duplicated().sum()}')
        if st.button('---------Delete duplicates---------'):
            df_new['data'] = df_new['data'].drop_duplicates()
            create_table(table_name, df_new['data'], engine)
            st.rerun()
# Function to render a line chart for the selected table
def chart(df, columns):
    if len(columns) > 0:
        fig = px.line(df.sort_index(), df.index, columns)
        st.write(fig)
