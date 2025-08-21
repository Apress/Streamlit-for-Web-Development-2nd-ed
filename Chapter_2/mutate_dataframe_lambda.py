import streamlit as st
import pandas as pd
import numpy as np

# Set the seed for reproducibility
np.random.seed(0)

# Create DataFrame with random numbers
df = pd.DataFrame(
    np.random.randn(4, 3),
    columns=('Column 1', 'Column 2', 'Column 3')
)

# Display the original DataFrame
st.subheader('Original DataFrame')
st.dataframe(df)

# Create a new column 'Column 4' based on 'Column 1'
df = df.assign(Column_4 = lambda x: x['Column 1'] * 2)

# Display the mutated DataFrame
st.subheader('Mutated DataFrame')
st.dataframe(df)
