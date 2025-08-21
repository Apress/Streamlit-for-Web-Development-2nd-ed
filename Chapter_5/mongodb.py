import streamlit as st
import pandas as pd
from pymongo import MongoClient
@st.cache_resource
def create_client():
    return MongoClient('<connection_string>')
def query(cuisine,address):
    result = create_client()['sample_restaurants']['restaurants'].aggregate([
        {
            "$search": {
                "index": "default",
                "text": {
                    "query": f"{address}",
                    "path": ["borough", "address.street"],
                    "fuzzy": {
                        "maxEdits": 2,
                        "prefixLength": 2
                    }
                }
            }
        }, {
            "$project": {
                "Name": "$name",
                "Cuisine": "$cuisine",
                "Address": "$address.street",
                "Borough": "$borough",
                "Grade": "$grades.grade",
                "Score": {
                    "$meta": "searchScore"
                }
            }
        }, {
            "$match": {
                "Cuisine": f"{cuisine}"
            }
        }, {
            "$limit": 5
        }
    ])
    try:
        df = pd.DataFrame(result)[['Name','Address','Grade','Score']]
        df['Grade'] = [','.join(map(str, x)) for x in df['Grade']]
        return df
    except:
        return None
if __name__ == '__main__':
    st.title('Restaurants Explorer')
    cuisine = st.selectbox('Cuisine',['American','Chinese','Delicatessen',
    'Hamburgers','Ice Cream, Gelato, Yogurt, Ices','Irish'])
    address = st.text_input('Address')
    if st.button('Search'):
        if address != ":
            st.write(query(cuisine,address))
        else:
            st.warning('Please enter an address')
