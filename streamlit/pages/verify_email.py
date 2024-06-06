from callbacks import user
from st_pages import hide_pages

import streamlit as st

hide_pages(["verify_email"])
token = st.query_params.get("token")

result = user.verify_email(token)

if result:
    st.switch_page("index.py")
