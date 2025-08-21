import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Create a DataFrame
df = pd.DataFrame(data={'Exam': ['Exam 1', 'Exam 2', 'Exam 3'],
                        'Jessica': [77, 76, 87],
                        'John': [56, 97, 95]})

# Set 'Exam' as the index and plot the line chart
df.set_index('Exam').plot(kind='line', xlabel='Exam', ylabel='Score', subplots=True)

# Display the plot using Streamlit
st.pyplot(plt)
