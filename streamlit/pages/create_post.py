import streamlit as st
from callbacks import categories, posts

st.header("New Post")

if "post_categories" not in st.session_state:
    st.session_state["post_categories"] = categories.get_categories()

category_options = {}
topic_options = {}
for item in st.session_state["post_categories"]:
    category_options[item.get("name")] = item.get("id")
    topic_options[item.get("name")] = item.get("topics")

category = st.selectbox("Category", options=category_options.keys())
topic = st.selectbox("Topics", options=topic_options[category])
title = st.text_input("Post Title")
content = st.text_area("Post Content")
image = st.file_uploader("Post Image")

if st.button("Post"):
    posts.add_post(
        category_id=category_options[category],
        topic=topic,
        post_title=title,
        post_content=content,
        post_image=image,
    )
