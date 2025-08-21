import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 

# Create a DataFrame
df = pd.DataFrame(data={'Name': ['Jessica', 'John'],
                        'Exam 1': [77, 56],
                        'Exam 2': [76, 97],
 'Exam 3': [87, 95]})

# Set the 'Name' column as the index and plot the bar chart
df.set_index('Name').plot(kind='bar', stacked=False, xlabel='Name', ylabel='Exam')

# Display the plot using Streamlit
st.pyplot(plt)
