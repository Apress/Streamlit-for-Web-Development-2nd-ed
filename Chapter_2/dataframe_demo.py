import streamlit as st
import pandas as pd
import plotly.express as px

# Sidebar for program selection
program = st.sidebar.selectbox('Select program', ['Dataframe Demo', 'Other Demo'])
code = st.sidebar.checkbox('Display code')

# Program logic
if program == 'Dataframe Demo':
    df = px.data.stocks()
    st.title('DataFrame Demo')

    # Multiselect for stock selection
    stocks = st.multiselect('Select stocks', df.columns[1:], default=df.columns[1:])

    # Displaying stock data as a DataFrame
    st.subheader('Stock value')
    st.write(df[['date'] + stocks].set_index('date'))

    # Plotting a Plotly line chart
    fig = px.line(df, x='date', y=stocks, hover_data={'date': '|%Y %b %d'})
    st.write(fig)

    # Displaying the code when checkbox is selected
    if code:
        st.code(
            """
import streamlit as st
import pandas as pd
import plotly.express as px

df = px.data.stocks()
st.title('DataFrame Demo')

program = st.sidebar.selectbox('Select program', ['Dataframe Demo', 'Other Demo'])
code = st.sidebar.checkbox('Display code')

if program == 'Dataframe Demo':
    df = px.data.stocks()
    st.title('DataFrame Demo')
    stocks = st.multiselect('Select stocks', df.columns[1:], default=df.columns[1:])
    st.subheader('Stock value')
    st.write(df[['date'] + stocks].set_index('date'))
    fig = px.line(df, x='date', y=stocks, hover_data={'date': '|%Y %b %d'})
    st.write(fig)
"""
        )
elif program == 'Other Demo':
    st.title('Other Demo')
