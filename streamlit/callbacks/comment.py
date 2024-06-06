import os

import requests

import streamlit as st

BACKEND = os.environ.get("BACKEND", "http://localhost:8000")


def comment_on_post(post_id: str, comment: str, reply_to_id: str = None):
    """Adds a comment to a post"""
    if not st.session_state.get("access_token"):
        st.toast("Login to react to posts and comments")
        return

    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token')}"
    }
    body = {"reply_to_id": reply_to_id, "content": comment}

    requests.post(
        url=f"{BACKEND}/api/v1/posts/{post_id}/comments",
        json=body,
        headers=headers,
    )

    st.switch_page(st.session_state.get("current_page", "index.py"))
