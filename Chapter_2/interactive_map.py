import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Data with university locations
df = pd.DataFrame(data={'university': ['Harvard University', 'Yale University', 'Princeton University', 
                                       'Columbia University', 'Brown University', 'Dartmouth University', 
                                       'University of Pennsylvania', 'Cornell University'],
                        'latitude': [42.3770, 41.3163, 40.3573, 40.8075, 41.8268, 43.7044, 39.9522, 42.4534],
                        'longitude': [-71.1167, -72.9223, -74.6672, -73.9626, -71.4025, -72.2887, -75.1932, -76.4735]
                        })

# Create the scattergeo plot
fig = go.Figure(data=go.Scattergeo(
    lon=df['longitude'],
    lat=df['latitude'],
    text=df['university'],
    mode='markers',
    marker=dict(size=10, color='red', opacity=0.7)
))

# Update the layout to focus on the USA and set additional map properties
fig.update_layout(
    geo_scope='usa',
    geo=dict(
        projection_type='albers usa',
        showland=True,
        landcolor='lightgray',
        subunitwidth=1,
    ))

# Display the map using Streamlit
st.plotly_chart(fig)
