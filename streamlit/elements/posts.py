import os
from typing import Any, Dict, List

import requests
from callbacks.reaction import react_to_target
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

BACKEND = os.environ.get("BACKEND", "http://localhost:8000")


def post_card(
    id: str,
    topic: str,
    title: str,
    content: str,
    likes: int,
    dislikes: int,
    image: str = None,
):
    """Displays a post card"""

    with st.container(height=500):
        # st.page_link(
        #     page=f"http://localhost:8501/post?post_id={id}", label=title
        # )
        if st.button(label=title, type="primary"):
            st.session_state["view_post_id"] = id
            st.switch_page("./pages/display_post.py")
        st.markdown(f"**{topic}**")

        if image:
            st.image(image=image, width=300)

        st.markdown(f"{content}")
        # st.session_state[f"{id}_likes"] = likes - dislikes
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
        #     label_visibility="hidden",
        #     index=None,
        #     key=id,
        # )

        # react_to_target(id, reaction)


def general_posts_feed(
    category: str = None,
    topic: str = None,
    page: int = 1,
    page_size: int = 10,
    sort: str = "hot",
):
    params = {
        "page_number": page,
        "page_size": page_size,
        "category_id": category,
        "category_topic": topic,
        "sort_by": sort,
    }
    response = requests.get(
        url=f"{BACKEND}/api/v1/posts/general_feed", params=params
    )

    posts: List[Dict[str, Any]] = response.json()

    for post in posts:
        post_card(
            id=post.get("id"),
            topic=post.get("category_topic"),
            title=post.get("title"),
            content=post.get("content"),
            likes=post.get("likes"),
            dislikes=post.get("dislikes"),
            image=(
                f"{BACKEND}{post.get('post_image_url')}"
                if post.get("post_image_url")
                else None
            ),
        )


def personal_posts_feed(
    page: int = 1,
    page_size: int = 10,
    sort: str = "hot",
):
    params = {
        "page": page,
        "page_size": page_size,
        "sort_by": sort,
    }
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token')}"
    }
    response = requests.get(
        url=f"{BACKEND}/api/v1/posts/user_feed", params=params, headers=headers
    )

    posts: List[Dict[str, Any]] = response.json()

    for post in posts:
        post_card(
            id=post.get("id"),
            topic=post.get("category_topic"),
            title=post.get("title"),
            content=post.get("content"),
            likes=post.get("likes"),
            dislikes=post.get("dislikes"),
            image=(
                f"{BACKEND}{post.get('post_image_url')}"
                if post.get("post_image_url")
                else None
            ),
        )


def single_post(
    post_id: str,
):
    response = requests.get(url=f"{BACKEND}/api/v1/posts/{post_id}")

    post: Dict[str, Any] = response.json()

    post_card(
        id=post.get("id"),
        topic=post.get("category_topic"),
        title=post.get("title"),
        content=post.get("content"),
        likes=post.get("likes"),
        dislikes=post.get("dislikes"),
        image=(
            f"{BACKEND}{post.get('post_image_url')}"
            if post.get("post_image_url")
            else None
        ),
    )
