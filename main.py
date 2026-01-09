import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
from Pages.auth import *


if "page" not in st.session_state: 
    st.session_state.page = "login" 

if "logged_in" not in st.session_state: 
    st.session_state.logged_in = False 

if "username" not in st.session_state: 
    st.session_state.username = ""

length_options = ['Short', 'Medium', 'Long']
language_options = ['English', 'Hinglish']


def main_page():
    st.title("LinkedIn Post Generator")

    fs = FewShotPosts()
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_title = st.selectbox(
            "Title",
            options=sorted(list(fs.get_tags()))
        )

    with col2:
        selected_length = st.selectbox("Length", length_options)

    with col3:
        selected_language = st.selectbox("Language", language_options)

    top_left, top_right, top_mid = st.columns([6,0.8, 1])

    with top_left:
        if st.button("Generate"):
            post = generate_post(
                selected_length,
                selected_language,
                selected_title
            )
            st.write(post)

    with top_right:
        if st.button("Clear"):
            st.rerun()
    with top_mid:
        if st.button("Logout"):
            st.session_state.page = "login"
            st.rerun()


def main():
    if st.session_state.page == "login":
        login_ui()
    elif st.session_state.page == "signup":
        signup_ui()
    elif st.session_state.page == "otp_ckeck":
        otp_check()
    elif st.session_state.page == "forgot_password":
        forgot_password()
    elif st.session_state.page == 'main':
        main_page()
   


if __name__ == "__main__":
    main()