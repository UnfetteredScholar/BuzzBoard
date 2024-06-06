import os

import requests

import streamlit as st

BACKEND = os.environ.get("BACKEND", "http://localhost:8000")


def react_to_target(target_id: str, index: str):
    """Reacts to a post or comment"""
    if index is None or (
        not st.session_state.get("access_token") and index != ":zero:"
    ):
        st.toast("Login to react to posts and comments")
        return
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token')}"
    }
    body = {}
    if index == ":zero:":
        requests.delete(
            url=f"{BACKEND}/api/v1/posts_comments/{target_id}/reactions/me",
            headers=headers,
        )
        st.switch_page(st.session_state.get("current_page", "index.py"))

    if index == ":arrow_up:":
        # st.session_state[f"{target_id}_likes"] += 1
        body["is_like"] = True
    elif index == ":arrow_down:":
        # st.session_state[f"{target_id}_likes"] -= 1
        body["is_like"] = False

    requests.post(
        url=f"{BACKEND}/api/v1/posts_comments/{target_id}/reactions",
        json=body,
        headers=headers,
    )
    st.switch_page(st.session_state.get("current_page", "index.py"))
