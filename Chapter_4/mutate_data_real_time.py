import streamlit as st
import pandas as pd
import random

def random_data(n):
    y = [random.randint(1, n) for value in range(n)]
    return y

if __name__ == '__main__':
    df1 = pd.DataFrame(data={'y': [1, 2]})
    # Create columns for table and chart
    col1, col2 = st.columns([1, 3])
    with col1:
        # Use st.dataframe for dynamic updates
        table = st.dataframe(df1)
    
    with col2:
        # Display the initial chart
        chart = st.line_chart(df1)
        # User input for number of rows to add
        n = st.number_input('Number of rows to add', 0, 10, 1)
        # Update button
        if st.button('Update'):
            y = random_data(n)
            df2 = pd.DataFrame(data={'y': y})
            # Append the new data to the existing dataframe
            table.add_rows(df2)
            chart.add_rows(df2)
