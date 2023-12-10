import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd


from utils import is_past_deadline, save_data

def display_expired_deadlines(data):
    late_students = []
    for student in data['students']:
        if is_past_deadline(student):
            add_student = student.copy()
            add_student.pop('password', None)
            late_students.append(add_student)

    if len(late_students)>0:
        df = pd.DataFrame(late_students)
        # Add a new column 'Borrowed Books' to the DataFrame
        df['books'] = df['books'].apply(lambda books: [book['book']['title'] for book in books])
        # Display the DataFrame
        st.dataframe(df[['name', 'family_name','username', 'email', 'books']])
    else:
        st.write("No overdue deadline")

def display_students(data):
    st.subheader("Students")
    students = []
    for student in data['students']:
        add_student = student.copy()
        add_student.pop('password', None)
        students.append(add_student)

    if len(students)>0:
        df = pd.DataFrame(students)
        df['books'] = df['books'].apply(lambda books: [book['book']['title'] for book in books])
        # Display the DataFrame
        st.dataframe(df[['name', 'family_name','username', 'email', 'books']])
    else : 
        st.write("No student account")


def create_new_student_account(data):
    st.subheader("Create New Student Account")
    new_student_name = st.text_input("student name:")
    new_student_family_name = st.text_input("student family name:")
    new_student_email = st.text_input("student email:")
    new_student_username = st.text_input("student username:")
    new_student_password = st.text_input("student password:", type="password")
    
    if st.button("Create Account"):
        # Replace this with your code to add the new student to the data dictionary
        # For example, you might want to generate a unique ID for the new student
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
        display_students(data)

