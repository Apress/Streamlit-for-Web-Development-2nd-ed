import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
def crud(path):
    df = pd.read_csv(path)
    df = df.fillna('None')
    index = len(df)
    # Initiate the streamlit-aggrid widget
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum',editable=True)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridOptions = gb.build()
    # Insert the dataframe into the widget
    df_new = AgGrid(df,gridOptions=gridOptions,enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED)
    # Add a new row to the widget
    if st.button('-----------Add a new row-----------'):
        df_new['data'].loc[index,:] = 'None'
        df_new['data'].to_csv(path, index=False)
        st.rerun()
    # Save the dataframe to disk if the widget has been modified
    if df.equals(df_new['data']) is False:
        df_new['data'].to_csv(path, index=False)
        st.rerun()
    # Remove selected rows from the widget
    if st.button('-----------Remove selected rows-----------'):
        if len(df_new['selected_rows']) > 0:
            exclude = pd.DataFrame(df_new['selected_rows'])
            pd.merge(df_new['data'], exclude, how='outer',
            indicator=True).query('_merge == "left_only"').drop('_merge', 1).to_csv(path, index=False)
            st.rerun()
        else:
            st.warning('Please select at least one row')
    # Check for duplicate rows
    if df_new['data'].duplicated().sum() > 0:
        st.warning(f'**Number of duplicate rows:** { df_new['data'].duplicated().sum()}')
        if st.button('-----------Delete duplicates-----------'):
            df_new['data'] = df_new['data'].drop_duplicates()
            df_new['data'].to_csv(path, index=False)
            st.rerun()
if __name__ == '__main__':
    st.title('Data')
    crud('data.csv')
