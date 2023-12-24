import os
import streamlit as st
import pandas as pd

from src.db_ops import show_data, edit_data, delete_data
from src.parameter_insertion_op import param_dict


def save_expense(cursor, db):
    st.header('💸 Expense Entry')

    lst = []

    if 'flag' not in st.session_state:
        st.session_state.flag = 0

    with st.form(key='expense_submit_form', clear_on_submit=False):
        expense_category = ['Shopping', 'Snacks', 'Mobile Recharge', 
                            'Online Course', 'Subscription']

        expense_date = st.date_input('Expense Date*')
        category = st.selectbox('Expense Category*', expense_category)
        amount = st.text_input('Amount*')
        notes = st.text_area('Notes')

        for key, val in param_dict.items():
            if key is not '':
                widget_function = getattr(st, val)
                user_input = widget_function(key)
                lst.append(user_input)

        document_upload = st.file_uploader('Upload Document', 
                                           type=['txt','pdf', 
                                                 'jpg', 'png', 'jpeg'], 
                                            accept_multiple_files=True)
        
        if st.form_submit_button(label='Submit'):
            if not(expense_date and category and amount):
                st.write('Please fill all the * fields')
            else:
                st.session_state.flag = 1
                # st.success('Data Submitted Successfully')

    columns = ['expense_date', 'category', 'amount', 'notes', 'documents']

    for key, val in param_dict.items():
        if key is not '':
            columns.append(key.lower())

    columns_str = ', '.join(columns)
    placeholders_str = ', '.join(['%s'] * len(columns))

    if param_dict:
        new_column_name = columns[-1]
        new_column_data_type = 'VARCHAR(255)'

        # Check if the column already exists in the table
        check_column_query = f"SHOW COLUMNS FROM expense LIKE '{new_column_name}'"
        cursor.execute(check_column_query)
        result = cursor.fetchone()

        # Construct the ALTER TABLE statement
        if not result:
            # Column doesn't exist, add it to the table
            alter_table_query = f"ALTER TABLE expense ADD COLUMN {new_column_name} {new_column_data_type}"

            # Execute the ALTER TABLE statement
            cursor.execute(alter_table_query)

            # Commit the changes
            db.commit()

            # Close the cursor and connection
            cursor.close()
            db.close()


    if st.session_state.flag:
        # st.write(final_parameter_calculation)

        with st.form(key='final', clear_on_submit=True):
             # st.write(final_parameter_calculation)

            if st.form_submit_button('Are you Sure?'):
                # st.write(final_parameter_calculation)
                st.session_state.flag = 0
                # insert data into expense table
                
                # st.write(document_upload.read())
                # st.write(document_upload.name)
                # st.write(document_upload.getvalue())
                # file = open(document_upload.read(),'rb')
                all_documents = []
                for file in document_upload:
                    st.write(file.name)
                    # st.write(file.getvalue())
                    # st.write(file.read())
                    if file is not None:
                        # Get the file name and extract the extension
                        file_name = file.name
                        # st.write(file_name)
                        file_extension = os.path.splitext(file_name)[1]
                        dir_name = "./documents/expenses"
                        if not os.path.isdir(dir_name):
                            os.makedirs(dir_name)

                        file_url = dir_name + '/' + file_name
                        # file_url = dir_name + file_name
                        all_documents.append(file_url)

                        # Save the file in its original format
                        with open(file_url, "wb") as f:
                            f.write(file.read())
                        st.success("File has been successfully saved.")
        

                query = f'''INSERT INTO expense ({columns_str})
                           VALUES ({placeholders_str})
                        '''
                
                values_list = [expense_date, category, amount, notes, str(all_documents)]

                for val in lst:
                    values_list.append(val)

                # st.write(query, values)
                # st.write("Query:", query)
                # st.write("Values:", values_list)
                
                cursor.execute(query, values_list)
                db.commit()
                st.success("Expense Record Inserted Successfully!")
                st.balloons()

            else:
                st.write("Click above button If you are Sure")
    else:
        st.warning("Please fill up above form")

    # Construct the SQL query dynamically
    query = f'''SELECT id, {columns_str} FROM expense'''
    # st.write(query)
    df = pd.read_sql(query, con=db)
  
    columns.insert(0, 'id')

    # st.dataframe(df)
    show_data(df, columns)
    edit_data(cursor, db, df, columns, 'Edit Expenses', 'expense')
    delete_data(cursor, db, df, columns, 'Delete Expenses', 'expense')


