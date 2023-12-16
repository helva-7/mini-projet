import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import re

from utils import is_past_deadline, save_data, get_overdue_books, get_user_by_id, suspend_user, is_valid_email

def display_expired_deadlines(data):
    late_students = []
    for student in data['students']:
        if is_past_deadline(student):
            add_student = student.copy()
            add_student.pop('password')
            add_student['books'] = get_overdue_books(student)
            late_students.append(add_student)

    if len(late_students)>0:
        df = pd.DataFrame(late_students)
        # Add a new column 'Borrowed Books' to the DataFrame
        df['overdue books'] = df['books'].apply(lambda books: [book['book']['title'] for book in books])
        # Display the DataFrame
        st.dataframe(df[['name', 'family_name','username', 'email', 'overdue books']])
    else:
        st.write("No overdue deadline")

def display_students(data):
    st.subheader("Students")
    students = data.get('students', [])
    
    if len(students) > 0:
        df = pd.DataFrame(students)
        df['books'] = df['books'].apply(lambda books: [book['book']['title'] for book in books])

        st.dataframe(df[['id', 'name', 'family_name', 'username', 'email', 'books']])

        user_id_to_suspend = st.text_input("Enter User ID to suspend:", key='id_field')

        if user_id_to_suspend != '':
            user_id_to_suspend = re.sub(r'\D', '', user_id_to_suspend)
            user_id_to_suspend = int(user_id_to_suspend)

        suspend_button = st.button("Suspend User", key='suspend')

        # Handle button click event
        if suspend_button and user_id_to_suspend:
            user_to_suspend = get_user_by_id(data, user_id_to_suspend)
            if user_to_suspend is not None:
                suspend_user(data, user_to_suspend)
                st.success(f"User with ID {user_id_to_suspend} suspended successfully.")
            else:
                st.warning(f"User with ID {user_id_to_suspend} not found.")
    else:
        st.write("No student account")


def create_new_student_account(data):
    st.subheader("Create New Student Account")
    new_student_name = st.text_input("student name:")
    new_student_family_name = st.text_input("student family name:")
    new_student_email = st.text_input("student email:")
    new_student_username = st.text_input("student username:")
    new_student_password = st.text_input("student password:", type="password")
    
    if not is_valid_email(new_student_email):
        st.error("Please enter a valid email address.")
        return

    if st.button("Create Account"):
        new_student_id = len(data['students']) + 1
        new_student = {
            "id": new_student_id,
            "name": new_student_name,
            "family_name": new_student_family_name,
            "email": new_student_email,
            "username": new_student_username,
            "password": stauth.Hasher([new_student_password]).generate()[0],
            "books": []  # Assuming an empty list for borrowed books initially
        }
        data['students'].append(new_student)
        save_data(data)
        st.success("New student account created successfully!")

def admin_page(user, data):
    st.title(f"Welcome {user['name']}")

    st.divider()
    st.header("Manage Deadlines")
    deadline_expander = st.expander("Overdue deadlines list", expanded=True)
    with deadline_expander:
        display_expired_deadlines(data)

    st.divider()
    st.header("Manage Students")
    student_expander = st.expander("Student list", expanded=True)
    with student_expander:
        display_students(data)
    
    new_account = st.expander("New student", expanded=True)
    with new_account:
        create_new_student_account(data)
        
    
    st.divider()
    st.header("Manage Borrowed Books")
    book_expander = st.expander("Expand", expanded=True)
    with book_expander:
        st.write('available soon')
        # display_students(data)
        # add book
