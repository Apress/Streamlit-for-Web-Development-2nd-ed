from warehouse_utils import *
import config # Credentials file
# PostgreSQL credentials
username = config.username
password = config.password
port = config.port
if __name__ == '__main__':
    # Creating PostgreSQL client
    connection = psycopg2.connect(f"user={username} password='{password}'")
    engine = create_engine(
        f'postgresql://{username}:{password}@localhost:{port}/')
    st.title('Data Warehouse')
    st.write('___')
    st.subheader('Database Manager')
    col1, col2 = st.columns(2)
    with col1:
        st.write('**Create database**')
        database_name = st.text_input('Please enter database name')
        if st.button('Create database'):
            status = create_database(database_name, connection)
            if status is True:
                st.success(f'Database **{database_name }** created successfully')
            elif status is False:
                st.warning('Database with this name already exists')
        st.write('**Rename database**')
        database_name_old = st.selectbox('Please select a database to rename',
        read_databases(engine))
        if database_name_old is not None:
            database_name_new = st.text_input('Please enter new database name')
            if st.button('Rename database'):
                status = update_database(database_name_old, database_name_new, connection)
                if status is True:
                    st.success(f'Database renamed from **{database_name_old}** to **{database_name_new}**')
    with col2:
        st.write('**List databases**')
        database_selection = st.selectbox('Databases list',read_databases(engine))
        st.write('**Delete database**')
        database_selection = st.selectbox('Please select a database to delete',
        read_databases(engine))
        if database_selection is not None:
            if st.button('Delete database'):
                status = delete_database(database_selection, connection)
                if status is True:
                    st.success(f'Database **{database_selection}** deleted successfully')
    st.write('___')
    st.subheader('Table Manager')
    st.write('**Select database**')
    database_selection = st.selectbox('Please select a database',
    read_databases(engine))
    if database_selection is not None:
        engine_database = create_engine(f'postgresql://{username}:{password}@localhost:{port}/{'warehouse_db_' + database_selection}')
        col1_2, col2_2 = st.columns(2)
        with col1_2:
            st.write('**Create table**')
            table = st.file_uploader('Please upload data')
            if table is not None:
                table = pd.read_csv(table)
                table_name = st.text_input('Please enter table name')
                if st.button('Save table'):
                    if len(table_name) > 0:
                        create_table(table_name, table, engine_database)
                        st.success(f'**{table_name}** saved to database')
                    else:
                        st.warning('Please enter table name')
        with col2_2:
            st.write('**Delete table**')
            table_selection = st.selectbox('Please select table to delete',
            list_tables(engine_database))
            if table_selection is not None:
                if st.button('Delete table'):
                    delete_table(table_selection, engine_database)
                    st.success(f'**{table_selection}** deleted successfully')
        st.write('**Read and update table**')
        table_selection = st.selectbox('Please select table to reade and update',
        list_tables(engine_database))
        if table_selection is not None:
            crud(table_selection, engine_database)
    st.write('___')
    st.subheader('Data Visualizer')
    st.write('**Select database**')
    database_selection = st.selectbox('Please select a database to visualize',
    read_databases(engine))
    if database_selection is not None:
        engine_database = create_engine(f'postgresql://{username}:{password}@localhost:{port}/{'warehouse_db_' + database_selection}')
        col1_3, col2_3 = st.columns(2)
        with col1_3:
            table_selection = st.selectbox('Please select table to visualize',
            list_tables(engine_database))
            table = read_table(table_selection, engine_database)
        if table_selection is not None:
            with col2_3:
                columns = st.multiselect('Please select columns', table.columns)
                table[columns] = table[columns].apply(pd.to_numeric, errors='coerce')
            chart(table, columns)
