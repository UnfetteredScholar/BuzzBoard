from callbacks import user
from st_pages import add_page_title, hide_pages

import streamlit as st

hide_pages(["verify_email"])
add_page_title()
st.header("BuzzBoard")


email = st.text_input(label="Email")
password = st.text_input(label="Password", type="password")

if st.button("Login"):
    if user.login(email, password):
        st.switch_page("./index.py")
