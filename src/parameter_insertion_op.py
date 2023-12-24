import streamlit as st

param_dict = {}

def parameter_listing():
    st.header('Parameter Insertion')

    if 'flag' not in st.session_state:
        st.session_state.flag = 0

    with st.form(key='parameter_insertion_form', clear_on_submit=True):
        input_widgets = ['checkbox', 'toggle', 'text_input', 'text_area', 'number_input', 'time_input', 'camera_input']

        label = st.text_input('Label*')
        input_widget = st.selectbox('Input Widgets*', input_widgets)

        param_dict.update({
            label: input_widget
        })

        if st.form_submit_button(label='Submit'):
            if not(label and input_widget):
                st.write('Please fill all the * fields')
            else:
                st.success("Parameter added successfully")

        
