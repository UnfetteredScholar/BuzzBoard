import os
from typing import List

import requests

import streamlit as st

BACKEND = os.environ.get("BACKEND")


def add_post(
    category_id: str,
    topic: str,
    post_title: str,
    post_content: str,
    post_image: List[bytes] = None,
):
    """Adds a post to a category"""
    if not st.session_state.get("access_token"):
        st.toast("Login to add a post")
        return

    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token')}"
    }
    data = {
        "category_id": category_id,
        "category_topic": topic,
        "title": post_title,
        "content": post_content,
    }
    files = []

    if post_image:
        files.append(("post_image", post_image))

    response = requests.post(
        url=f"{BACKEND}/api/v1/posts", data=data, headers=headers, files=files
    )

    st.write(response.content)

    # st.switch_page(st.session_state.get("current_page", "index.py"))
