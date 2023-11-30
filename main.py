import streamlit as st
import streamlit_authenticator as stauth

from lib import DataManager
from student import student_page

@st.cache_data
def load_data():
    return DataManager.load_data('data.json')

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data


credentials = DataManager.get_credentials(data)


authenticator = stauth.Authenticate(credentials, 'user_dashboard', 'abcdef', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')


if authentication_status:
    authenticator.logout('Logout', 'main')
    user = DataManager.get_user_by_username(username, data)

    if username in [student.username for student  in data['students']]:
        student_page(user, data)
    elif username in [admin.username for admin  in data['admins']]:
        pass

        st.write(f'Welcome *{name}*')
        st.title('Dashboard')

elif not authentication_status:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
