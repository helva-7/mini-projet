import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd

from utils import is_past_deadline, save_data, get_overdue_books, get_user_by_id, suspend_user, is_valid_email, generate_student_id

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

        user_id_to_suspend = st.number_input("Enter User ID to suspend:",min_value=1, max_value=len(students), step=1, format='%d',  key='id_field')

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

def display_book(data, book):
    st.write(f"Title: {book['title']}")
    st.caption(f"Author: {book['author']}")
    st.caption(f"Year: {book['year']}")
    updated_books_available = st.number_input(f"Number of copies",min_value=0, value=book['num'], step=1, format='%d', key=book['ISBN'])
    if st.button(f"Update {book['title']}"):
        book['num'] = updated_books_available
        save_data(data)
        st.success("Number of books available updated successfully.")


def create_new_student_account(data):
    st.subheader("Create New Student Account")
    new_student_name = st.text_input("student name:")
    new_student_family_name = st.text_input("student family name:")
    new_student_email = st.text_input("student email:")
    new_student_username = st.text_input("student username:")
    new_student_password = st.text_input("student password:", type="password")
    
    if not is_valid_email(new_student_email):
        st.warning("Please enter a valid email address.")
        return

    if st.button("Create Account"):
        new_student_id = generate_student_id(data)
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

def add_new_book(data):
    st.subheader("Add New Book")
    new_book_title = st.text_input("Book Title:")
    new_book_author = st.text_input("Book Author:")
    new_book_editor = st.text_input("Book Editor:")
    new_book_ISBN = st.text_input("ISBN:")
    new_book_num = st.number_input("Number of Copies:", min_value=0, step=1)
    new_book_year = st.number_input("Year:", min_value=1800, step=1)

    if st.button("add book"):
        new_book_id = len(data['books']) + 1

        new_book = {
        "id": new_book_id,
        "title": new_book_title,
        "author": new_book_author,
        "editor": new_book_editor,
        "ISBN": new_book_ISBN,
        "num": new_book_num,
        "year": new_book_year
        }
        data['books'].append(new_book)
        save_data(data)
        st.success("New book added successfully!")


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
    book_expander = st.expander("Library", expanded=True)
    with book_expander:
        for i in range(0, len(data["books"]), 3):
            col1, col2, col3 = st.columns(3)
            with col1:
                display_book(data, data["books"][i])
            with col2:
                display_book(data, data["books"][i+1])
            with col3:
                display_book(data, data["books"][i+2])
    
    new_book_expander = st.expander("new book", expanded=True)
    with new_book_expander:
        add_new_book(data)
