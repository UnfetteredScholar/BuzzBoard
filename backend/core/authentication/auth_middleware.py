import json

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.authentication.auth_token import (
    credentials_exception,
    verify_access_token,
)
from core.authentication.hashing import hash_verify
from core.storage import storage
from schemas.token import TokenData
from schemas.user import User, UserStatus

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_user(email: str) -> User:
    """
    Gets a user from the db storage using their email
    """
    users = storage.db["users"]

    user = users.find_one({"email": email})
    if user is None:
        return None
    user_data = json.loads(json.dumps(user, default=str))

    return user_data


def authenticate_user(email: str, password: str) -> User:
    user = storage.verify_user_record({"email": email})

    # print(user)
    if not hash_verify(password, user.password):
        # return False
        raise credentials_exception
    # if "password" in user:
    #     del user["password"]
    return user


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Gets the current user.

    Args:
        token: jwt string containing the user data

    Returns:
        Data about the active user
    """
    tokenData: TokenData = verify_access_token(token)

    if tokenData.type != "bearer":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type",
        )

    user = storage.get_user_record({"email": tokenData.email})

    if user is None:
        raise credentials_exception

    # if "password" in user:
    #     del user["password"]

    return user


def get_current_active_user(user: User = Depends(get_current_user)):
    """
    Gets the current user and verifies if
    their account is active
    """

    if user.status != UserStatus.VERIFIED.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account not activated",
        )

    return user


def get_current_admin_user(user: User = Depends(get_current_user)):
    """
    Gets the current user and verifies if
    their account is an admin
    """

    if user.role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unautorized action"
        )

    return user
