from st_pages import add_page_title

import streamlit as st
from callbacks import user

add_page_title()
st.header("BuzzBoard")
st.subheader("Sign Up")

username = st.text_input(label="Username")
email = st.text_input(label="Email")
password = st.text_input(label="Password", type="password")

if st.button("Sign up"):
    user.register(username, email, password)
    # st.switch_page("./index.py")
