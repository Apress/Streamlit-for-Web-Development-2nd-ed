import streamlit as st
import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(0)

# Create DataFrame with random data
df = pd.DataFrame(
    np.random.randn(4, 3),
    columns=('Column 1', 'Column 2', 'Column 3')
)

# Display the original DataFrame
st.subheader('Original DataFrame')
st.dataframe(df)

# Filter the DataFrame (mutating it)
df = df[df['Column 1'] > -1]

# Display the mutated DataFrame
st.subheader('Mutated DataFrame')
st.dataframe(df)
