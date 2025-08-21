import streamlit as st
from utility import calculate

st.title('Simple Calculator')
num1 = st.number_input('Enter first number', value=0.0, key='INPUT_1')
num2 = st.number_input('Enter second number', value=0.0, key='INPUT_2')
operation = st.selectbox('Select operation', ['+', '-', '*', '/'], key='OPERATION')

result = None
if st.button('Calculate', key='BUTTON'):
    result = calculate(operation, num1, num2)
    if result is None:
        st.error('Error: Cannot divide by zero')
    else:
        st.write(f'Result: {result}')
