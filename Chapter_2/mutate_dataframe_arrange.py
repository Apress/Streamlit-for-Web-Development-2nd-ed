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
st.dataframe(df)  # Use st.dataframe for interactive display

# Mutate the DataFrame by sorting by 'Column 1'
df = df.sort_values(by='Column 1', ascending=True)

# Display the mutated DataFrame
st.subheader('Mutated DataFrame')
st.dataframe(df)  # Use st.dataframe for interactive display
