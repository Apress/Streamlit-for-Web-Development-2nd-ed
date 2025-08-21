import streamlit as st

def calculate_sum(n1, n2):
    return n1 + n2

st.title('Add Numbers')

n1 = st.number_input('First Number', value=0)
n2 = st.number_input('Second Number', value=0)

if st.button('Calculate'):
    summation = calculate_sum(n1, n2)
    st.write(f'Summation is: {summation}')
