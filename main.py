import streamlit as st
import streamlit_authenticator as stauth

from utils import load_data, get_credentials, get_user_by_username
from student import student_page
from admin import admin_page

@st.cache_data
def _load_data():
    return load_data()

if "data" not in st.session_state:
    st.session_state.data = _load_data()

data = st.session_state.data


credentials = get_credentials(data)


authenticator = stauth.Authenticate(credentials, 'user_dashboard', 'abcdef', cookie_expiry_days=1)

name, authentication_status, username = authenticator.login('Login', 'main')


if authentication_status:
    authenticator.logout('Logout', 'main')
    user, type = get_user_by_username(data, username)

    if type == 'student':
        student_page(user, data)
    elif type == 'admin':   
        admin_page(user, data)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
