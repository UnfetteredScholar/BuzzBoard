import os
from typing import Any, Dict, List

import requests
from callbacks.reaction import react_to_target
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

BACKEND = os.environ.get("BACKEND", "http://localhost:8000")


def write(text: str):
    st.write(text)


def comment_card(id: str, content: str, likes: int, dislikes: int):
    """Displays a comment card"""

    with st.container(height=150):
        st.markdown(f"{content}")
        st.write(f"{likes - dislikes}")
        reaction_row = st.columns(3)

        with reaction_row[0]:
            if st.button(label=":arrow_up:", key=f"like_{id}"):
                react_to_target(id, ":arrow_up:")

        with reaction_row[1]:
            if st.button(label=":arrow_down:", key=f"dislike_{id}"):
                react_to_target(id, ":arrow_down:")

        with reaction_row[2]:
            if st.button(label=":zero:", key=f"unlike_undislike_{id}"):
                react_to_target(id, ":zero:")

        # reaction = st.radio(
        #     label=f"{likes - dislikes}",
        #     options=[
        #         ":arrow_up:",
        #         ":arrow_down:",
        #         ":zero:",
        #     ],
        #     horizontal=True,
        #     # label_visibility="hidden",
        #     index=2,
        #     key=id,
        # )

        # react_to_target(id, reaction)


def display_post_comments(
    post_id: str,
    page: int = 1,
    page_size: int = 10,
):
    params = {
        "page_number": page,
        "page_size": page_size,
    }
    response = requests.get(
        url=f"{BACKEND}/api/v1/posts/{post_id}/comments", params=params
    )

    comments: List[Dict[str, Any]] = response.json()

    for comment in comments:
        comment_card(
            id=comment.get("id"),
            content=comment.get("content"),
            likes=comment.get("likes"),
            dislikes=comment.get("dislikes"),
        )
