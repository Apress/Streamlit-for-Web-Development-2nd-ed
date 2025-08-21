import streamlit as st
import pandas as pd

# Create the first DataFrame (df1)
df1 = pd.DataFrame(data={'Name': ['Jessica', 'John'],
                         'Exam 1': [77, 56]})

# Create the second DataFrame (df2)
df2 = pd.DataFrame(data={'Name': ['Jessica', 'John'],
                         'Exam 2': [76, 97]})

# Create the third DataFrame (df3)
df3 = pd.DataFrame(data={'Name': ['Jessica', 'John'],
                         'Exam 3': [87, 95]})

# Display the original dataframes
st.subheader('Original DataFrames')
st.dataframe(df1)
st.dataframe(df2)
st.dataframe(df3)

# Merge the dataframes on 'Name' column using inner join
df_merged = df2.merge(df3, how='inner', on='Name')
df_merged = df1.merge(df_merged, how='inner', on='Name')

# Display the mutated dataframe after merging
st.subheader('Mutated DataFrame')
st.dataframe(df_merged)
