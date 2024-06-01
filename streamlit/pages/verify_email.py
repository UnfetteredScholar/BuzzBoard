import streamlit as st
from callbacks import user

token = st.query_params.get("token")

result = user.verify_email(token)

if result:
    st.switch_page("index.py")
