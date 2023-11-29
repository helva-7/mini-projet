import streamlit as st
from lib import Admin, Student, Book, DataManager

@st.cache_data
def load_data():
    print("data loaded")
    return DataManager.load_data('data.json')


if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data


def borrow_callback(book, user):
    borrowed = user.borrow_book(book)
    if borrowed:
        st.success("Book borrowed successfuly")
    else : 
        st.error("You can't borrow more than 3 books")

def return_callback(book, user):
    returned = user.return_book(book)
    if returned:    
        st.success("Book returnedsuccessfuly")
    else : 
        st.error("Something went wrong")
    
def display_book(book, user):
    st.write(f"Title: {book.title}")
    st.caption(f"Author: {book.author}")
    st.caption(f"Year: {book.year}")
    st.button(f"Borrow {book.title}", on_click=borrow_callback, args=(book, user))

def display_borrowed_books(user):
    if len(user.books) > 0:
        columns = st.columns(len(user.books))
        for i, book in enumerate(user.books):
            with columns[i]:
                st.write(f"Title: {book['book'].title}")
                st.caption(f"Author: {book['book'].author}")
                st.caption(f"Year: {book['book'].year}")
                st.caption(f"Deadline: {book['deadline'].strftime('%m/%d/%Y, %H:%M:%S')}")
                st.button(f"Return {book['book'].title}", on_click=return_callback, args=(user, book))

    else : 
        st.caption("0 books borrowed")

def admin_page(user):
    st.title(f"Welcome {user.name}")


def student_page(user):
    st.title(f"Welcome {user.name}")

    st.header("Overview")
    if len(user.books) > 0:
        closest_deadline = user.books[0]["deadline"].strftime('%m/%d/%Y, %H:%M')
    else : closest_deadline = "None"

    num_books, time_left = st.columns(2)
    num_books.metric("Number of books", f"{len(user.books)}", 3-len(user.books))
    time_left.metric("Deadline", f"{closest_deadline}")


    st.divider()
    st.header("Borrowed books")
    display_borrowed_books(user)
                


    st.divider()
    st.header("Library")
    for i in range(0, len(data["books"]), 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            display_book(data["books"][i], user)
        with col2:
            display_book(data["books"][i+1], user)
        with col3:
            display_book(data["books"][i+2], user)
        
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
