import streamlit as st
from utils import borrow_book, return_book, get_closest_deadline


def borrow_callback(data, book, user):
    borrowed = borrow_book(data, book, user)
    if borrowed == True:
        st.success("Book borrowed successfuly")
    else : 
        st.error(borrowed)

def return_callback(data, user, book):
    returned = return_book(data, user, book)
    if returned == True:
        st.success("Book returned successfuly")
    else : 
        st.error(returned)


def display_borrowed_books(data, user):
    if len(user['books']) > 0:
        columns = st.columns(len(user['books']))
        for i, book in enumerate(user['books']):
            with columns[i]:
                st.write(f"Title: {book['book']['title']}")
                st.caption(f"Author: {book['book']['author']}")
                st.caption(f"Year: {book['book']['year']}")
                st.caption(f"Deadline: {book['deadline'].strftime('%m/%d/%Y, %H:%M:%S')}")
                st.button(f"Return {book['book']['title']}", on_click=return_callback, args=(data, user, book),
                           key=	book['book']['ISBN']+'b')

    else : 
        st.caption("0 books borrowed")


def display_book(data, book, user):
    st.write(f"Title: {book['title']}")
    st.caption(f"Author: {book['author']}")
    st.caption(f"Year: {book['year']}")
    st.button(f"Borrow {book['title']}", on_click=borrow_callback, args=(data, book, user), key=book['ISBN'])

def student_page(user, data):
    st.title(f"Welcome {user['name']}")

    st.header("Overview")
    if len(user['books']) > 0:
        closest_deadline = get_closest_deadline(user)
        closest_deadline = closest_deadline.strftime('%m/%d/%Y, %H:%M')

    else : closest_deadline = "None"

    num_books, time_left = st.columns(2)
    num_books.metric("Number of books", f"{len(user['books'])}", 3-len(user['books']))
    time_left.metric("Deadline", f"{closest_deadline}")


    st.divider()
    st.header("Borrowed books")
    display_borrowed_books(data, user)
                


    st.divider()
    st.header("Library")
    for i in range(0, len(data["books"]), 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            display_book(data, data["books"][i], user)
        with col2:
            display_book(data, data["books"][i+1], user)
        with col3:
            display_book(data, data["books"][i+2], user)




