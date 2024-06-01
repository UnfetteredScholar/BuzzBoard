from st_pages import Page, Section, add_page_title, hide_pages, show_pages

import streamlit as st
from elements.posts import general_posts_feed, personal_posts_feed

add_page_title()

show_pages(
    [
        Page("index.py", "Home", "🏠"),
        Page("pages/create_post.py", "New Post", ":books:"),
        Page("pages/display_post.py", "Post", ":open_book:"),
        Page("pages/login.py", "Login", ":key:"),
        Page("pages/sign_up.py", "Sign Up", ":bust_in_silhouette:"),
        Page("pages/verify_email.py", "verify_email", ":unlock:"),
    ]
)
hide_pages(["verify_email"])

if "index_page_num" not in st.session_state:
    st.session_state["index_page_num"] = 1

if "index_page_sort" not in st.session_state:
    st.session_state["index_page_sort"] = "hot"

st.session_state["current_page"] = "index.py"


st.header("BuzzBoard")


row1 = st.columns([1, 10, 1])


with row1[1]:
    if not st.session_state.get("access_token"):
        general_posts_feed(
            page=st.session_state.get("index_page_num"),
            sort=st.session_state.get("index_page_sort"),
        )
    else:
        personal_posts_feed(
            page=st.session_state.get("index_page_num"),
            sort=st.session_state.get("index_page_sort"),
        )
