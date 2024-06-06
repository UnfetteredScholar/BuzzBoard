from callbacks import user
from st_pages import add_page_title, hide_pages

import streamlit as st

hide_pages(["verify_email"])
add_page_title()
st.header("BuzzBoard")
st.subheader("Sign Up")

username = st.text_input(label="Username")
email = st.text_input(label="Email")
password = st.text_input(label="Password", type="password")
confirm_password = st.text_input(label="Confirm Password", type="password")

if password == confirm_password:
    if st.button("Sign up"):
        user.register(username, email, password)
    # st.switch_page("./index.py")
else:
    st.warning("Passwords do not match")
