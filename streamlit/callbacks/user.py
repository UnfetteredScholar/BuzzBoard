import os

import requests

import streamlit as st

BACKEND = os.environ.get("BACKEND", "http://localhost:8000")


def register(username: str, email: str, password: str):
    """Registers a user"""

    body = {"username": username, "email": email, "password": password}

    response = requests.post(
        url=f"{BACKEND}/api/v1/register",
        json=body,
    )

    if response.ok:
        st.toast(
            "Account created successfully. Visit your email to activate your account."
        )
    else:
        st.warning("Invalid Email or Password")


def verify_email(token: str) -> bool:
    """Verifies a user's email"""

    body = {"verification_token": token}

    response = requests.post(
        url=f"{BACKEND}/api/v1/register/verify",
        json=body,
    )

    if response.ok:
        st.toast("Email verified successfully.")
        return True
    else:
        st.warning("Invalid Token")
        return False


def login(email: str, password: str) -> bool:
    """performs user login"""

    body = {"username": email, "password": password}

    response = requests.post(
        url=f"{BACKEND}/api/v1/login",
        data=body,
    )

    if response.ok:
        st.session_state["access_token"] = response.json().get("access_token")
        return True
    else:
        st.warning("Invalid Email or Password")
        return False


def logout():
    """Performs user logout"""

    if "access_token" in st.session_state:
        st.session_state["access_token"] = None
