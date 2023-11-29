import streamlit as st
from lib import Admin, Student, Book, DataManager


data = DataManager.load_data('data.json')


def display_book(book):
    st.write(f"Title: {book.title}")
    st.write(f"Author: {book.author}")
    st.write(f"Year: {book.year}")
    borrow = st.button("Borrow", key=book.id)

def admin_page(user):
    st.title(f"Welcome {user.name}")


def student_page(user):
    st.title(f"Welcome {user.name}")

    st.header("Overview")
    if len(user.books) > 0:
        closest_deadline = user.books[0]["deadline"]
    else : closest_deadline = "None"
    num_books, time_left = st.columns(2)
    num_books.metric("Number of books", f"{len(user.books)}", 3-len(user.books))
    time_left.metric("Deadline", f"{closest_deadline}")
    # col3.metric("Humidity", "86%", "4%")

    st.divider()
    st.header("Borrowed books")
    if len(user.books) > 1:
        columns = st.columns(len(user.books))
        for i, book in enumerate(user.books):
            with columns[i]:
                display_book(book)
                


    st.divider()
    st.header("Library")
    for i in range(0, len(data["books"]), 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            display_book(data["books"][i])
        with col2:
            display_book(data["books"][i+1])
        with col3:
            display_book(data["books"][i+2])
        
def main():
    st.title("Login Screen")

    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        for user in data["students"]+data["admins"]:
            if user.login(username, password):
                if isinstance(user, Admin):
                    st.success("Login successful! User is an admin.")
                    admin_page(user)
                elif isinstance(user, Student):
                    st.success("Login successful! User is a student.")
                    student_page(user)

                break
        else:
            st.error("Invalid username or password.")

if __name__ == "__main__":
    main()