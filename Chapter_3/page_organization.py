import streamlit as st
from datetime import datetime

tab1, tab2 = st.tabs(['Tab 1', 'Tab 2'])

with tab1:
    st.subheader('_Tab 1_')

    # Expander in sidebar
    st.sidebar.subheader('Expander')
    with st.sidebar.expander('Time'):
        time = datetime.now().strftime('%H:%M:%S')
        st.write(f'**{time}**')

    # Columns in sidebar
    st.sidebar.subheader('Columns')
    col1, col2 = st.sidebar.columns(2)
    with col1:
        option_1 = st.selectbox('Please select option 1', ['A', 'B'])
    with col2:
        option_2 = st.radio('Please select option 2', ['A', 'B'])

    # Container in sidebar
    container = st.sidebar.container()
    container.subheader('Container')
    option_3 = container.slider('Please select option 3')
    st.sidebar.warning('Elements outside of container will be displayed externally')
    container.info(f'**Option 3:** {option_3}')

    # Expander in main body
    st.subheader('Expander')
    with st.expander('Time'):
        time = datetime.now().strftime('%H:%M:%S')
        st.write(f'**{time}**')

    # Columns in main body
    st.subheader('Columns')
    col1, col2 = st.columns(2)
    with col1:
        option_4 = st.selectbox('Please select option 4', ['A', 'B'])
    with col2:
        option_5 = st.radio('Please select option 5', ['A', 'B'])

    # Container in main body
    container = st.container()
    container.subheader('Container')
    option_6 = container.slider('Please select option 6')
    st.warning('Elements outside of container will be displayed externally')
    container.info(f'**Option 6:** {option_6}')

with tab2:
    # Popover in main body
    st.subheader('Popover')
    with st.popover('Popover'):
        option_7 = st.radio('Please select option 7', ['A', 'B'])
    st.write(f'**Option 7:** {option_7}')

    # Dialog box in main body
    st.subheader('Dialog box')
    @st.dialog('Option 8')
    def dialog_box():
        option_8 = st.selectbox('Please select option 8', ['A', 'B'])
        if st.button('Submit'):
            st.session_state['option_8'] = option_8
            st.rerun()
    if 'option_8' not in st.session_state:
        if st.button('Dialog box'):
            dialog_box()
    else:
        st.write(f'**Option 8:** {st.session_state['option_8']}')
