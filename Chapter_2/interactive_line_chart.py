import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Create a DataFrame
df = pd.DataFrame(data={
    'Exam': ['Exam 1', 'Exam 2', 'Exam 3'],
    'Jessica': [77, 76, 87],
    'John': [56, 97, 95]
})

# Create the plotly figure with line plots
fig = go.Figure(data=[
    go.Scatter(name='Jessica', x=df['Exam'], y=df['Jessica'], mode='lines+markers'),
    go.Scatter(name='John', x=df['Exam'], y=df['John'], mode='lines+markers')
])

# Update the layout
fig.update_layout(
    xaxis_title='Exam',
    yaxis_title='Score',
    legend_title='Name',
)

# Display the plot using Streamlit with selection enabled
event = st.plotly_chart(fig, on_select='rerun')

# Access selected points
if event and event.selection:
    selected_data = []
    for point in event.selection.points:
        selected_data.append({
            'Exam': point['x'],
            'Student': point['curve_number'],
            'Score': point['y']
        })
    
    # Map curveNumber to student names
    for item in selected_data:
        item['Student'] = fig.data[item['Student']].name

    st.write('Selected Exam Scores:')
    st.dataframe(selected_data)
