import streamlit as st
import pandas as pd
import numpy as np

# Create a DataFrame with random integers between 0 and 100
df = pd.DataFrame(
    np.random.randint(0, 101, size=(6, 3)),
    columns=('Exam 1', 'Exam 2', 'Exam 3')
)

# Assign 'Name' and 'Category' columns directly
df['Name'] = ['John', 'Jessica', 'Jessica', 'John', 'John', 'Jessica']
df['Category'] = ['B', 'A', 'A', 'B', 'A', 'B']

# Display the original DataFrame
st.subheader('Original DataFrame')
st.dataframe(df)

# Group by 'Name' and 'Category' and get the first row of each group
df_grouped = df.groupby(['Name', 'Category']).first()

# Display the mutated DataFrame after grouping
st.subheader('Mutated DataFrame')
st.dataframe(df_grouped)
