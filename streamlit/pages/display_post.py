from st_pages import add_page_title

import streamlit as st
from callbacks.comment import comment_on_post
from elements.comments import display_post_comments
from elements.posts import single_post

add_page_title()

st.session_state["current_page"] = "./pages/display_post.py"
st.header("View Post")

if st.session_state.get("view_post_id"):
    single_post(st.session_state.get("view_post_id"))

    st.subheader("Comments")
    display_post_comments(st.session_state.get("view_post_id"))

    with st.expander("Add Comment"):
        comment = st.text_input(
            label="Comment Here", label_visibility="hidden"
        )
        if st.button("Comment"):
            comment_on_post(st.session_state.get("view_post_id"), comment)
