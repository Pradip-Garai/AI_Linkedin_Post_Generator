import streamlit as st
import bcrypt
import Config.db
from Config.models import Users
from Config.send_otp import send_otp_email
from Config.recover_password_mail import send_password_email
import random

popup = st.empty()
gender = ['---Select Your Gender---','Male', 'Female', 'Others']
Occupations = ['---Describe Yourself---','Corporate Employee','Government Employee','Engineer','Doctor','Entrepreneur','Influencer','Freelancer','Student','Other']


if "otp" not in st.session_state: 
    st.session_state.otp = ""

if "email" not in st.session_state: 
    st.session_state.email = ""

def login_ui():
    st.title("Login to Your Workspace")
    email_input = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")

    col1,col2,col3 = st.columns([3,1,1])

    with col1:
        if st.button("Login"):
            user = Users.objects(email=email_input).first()
            
            if user:
              if user.verified == False:
                st.error("User Not Varified")
              else:
                stored_password_bytes = user.password.encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_bytes):
                    st.session_state.page = "main"
                    st.rerun()
                else:
                    st.error("Invalid Email or Password")
                    
            else:
                st.error("User Not Found!!!")
                  
    # with col2:
    #     if st.button("Forgot Password"):
    #         st.session_state.page = "forgot_password"
    #         st.rerun()
    with col3:
        if st.button("Create Account"):
            st.session_state.page = "signup"
            st.rerun()
    
def signup_ui():
    st.title("Signup & Launch Your Workspace")
    names = st.text_input("Enter Your Fullname")
    genders = st.selectbox("Gender",gender)
    occupations = st.selectbox("Occupation",Occupations)
    emails = st.text_input("Enter Your Email")
    password = st.text_input("Enter Your Password")
    confirm_password = st.text_input("Re-Enter Password")

    btn1, btn2 = st.columns([7,2])

    with btn1:
        if st.button("Signup"):
            if not names or not emails or genders=='---Select Your Gender---' or not password or not confirm_password or occupations=='---Describe Yourself---':
                st.error("Missing Fileds!!!\nAll Fileds are required")
            else:
                if password != confirm_password:
                    st.error("Password Missmatched")
                else:
                    password2=password.encode('utf-8')
                    hashed_password = bcrypt.hashpw(password2, bcrypt.gensalt())
                    user = Users(
                        name=names,
                        email=emails,
                        password=hashed_password,
                        gender = genders,
                        occupation = occupations
                    )
                    user.save()
                    Otp = random.randint(1000, 9999)
                    st.session_state.otp = Otp
                    st.session_state.email = emails
                    send_otp_email(emails,Otp)
                    st.session_state.page = "otp_ckeck"
                    st.rerun()


    with btn2:
        if st.button("<- Back to Login"):
            st.session_state.page = "login"
            st.rerun()

def otp_check():
    st.title("🔐 Verify OTP")
    st.caption("Enter the 4-digit code sent to your email")

    if "email" not in st.session_state or "otp" not in st.session_state:
        st.error("❌ Session expired. Please go back and request a new OTP.")
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        d1 = st.text_input("", max_chars=1, key="otp1")
    with col2:
        d2 = st.text_input("", max_chars=1, key="otp2")
    with col3:
        d3 = st.text_input("", max_chars=1, key="otp3")
    with col4:
        d4 = st.text_input("", max_chars=1, key="otp4")

    otp_entered = f"{d1}{d2}{d3}{d4}"

    if st.button("Verify"):
        if len(otp_entered) < 4:
            st.error("❌ Please enter complete OTP")

        elif otp_entered == str(st.session_state.otp):
            try:
                user = Users.objects(email=st.session_state.email).first()
                if user:
                    user.verified = True
                    user.save()

                    st.success("✅ User verified successfully")
                    st.session_state.page = "main"
                    st.rerun()
                else:
                    st.error("❌ User not found")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

        else:
            st.error("❌ Invalid OTP")

def forgot_password():
    st.title("Backdoor (Safe Mode) 🔐")
    st.caption("Lost the key? We’ve got the spare 🔑")

    email = st.text_input("Enter Your Registered Email")

    btn,btn2 = st.columns([6,2])

    with btn:
        if st.button("Send"):
          user = Users.objects(email=email).first()
          
          if user:
              password = user.password.encode('utf-8')
              send_password_email(email,password)
              st.success("Password Sent to Your Email")
          else:
              st.error("Email Not Registered!!!")
    with btn2:
        if st.button("<- Back to Login"):
            st.session_state.page = "login"
            st.rerun()
