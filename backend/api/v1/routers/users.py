from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from core.authentication.auth_middleware import (
    authenticate_user,
    get_current_active_user,
)
from core.authentication.hashing import get_hash
from core.storage import storage
from schemas.user import User, UserOut

router = APIRouter()


@router.get(path="/users/me", response_model=UserOut)
async def get_user_details(
    current_user: User = Depends(get_current_active_user),
) -> UserOut:
    """Gets the user details"""
    # change_id_key(current_user)
    return current_user


@router.patch(path="/users/me")
async def update_user_details(
    username: str = Body(embed=True),
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, str]:
    """Updates the user's details"""
    storage.update_user_record(
        filter={"_id": current_user.id}, update={"username": username}
    )
    message = {"message": "details updated successfully"}
    return JSONResponse(content=message)


@router.delete(path="/users/me")
def delete_account(
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, str]:
    """Deletes a user's account"""

    storage.delete_user_record({"_id": current_user.id})
    message = {"message": "account deleted successfully"}
    return JSONResponse(content=message)


@router.post(path="/users/me/change_password", response_model=Dict[str, str])
async def change_user_password(
    current_password: str = Body(),
    new_password: str = Body(),
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, str]:
    """Changes a user's password"""

    authenticate_user(current_user.email, current_password)

    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password length. Password length must be at least 8 characters",
        )

    storage.update_user_record(
        {"_id": current_user.id}, {"password": get_hash(new_password)}
    )
    message = {"message": "password changed successfully"}
    return JSONResponse(content=message)


# @router.get(path="/users", response_model=List[UserOut])
# def get_users(
#     verified: Union[bool, None] = None,
#     current_user: User = Depends(get_current_admin_user),
# ):
#     """Gets all the active and/or inactive user accounts in the system"""
#     logger = getLogger(__name__)
#     try:
#         users_table = storage.db["users"]
#         filter = {}
#         if verified is not None:
#             filter["verified"] = verified

#         users = users_table.find(filter).sort({"date_created": -1})

#         users_list = []
#         for user in users:
#             user = change_id_key(json.loads(json.dumps(user, default=str)))
#             del user["password"]
#             users_list.append(user)
#         return users_list
#     except Exception as ex:
#         logger.error(ex)
#         raise ex


# @router.patch(path="/users/{user_id}")
# def update_user(
#     user_id: str,
#     data: UserUpdate,
#     current_user: User = Depends(get_current_admin_user),
# ):
#     """Sets the activation status or role of the user"""
#     logger = getLogger(__name__)
#     try:
#         user = storage.verify_user_record({"_id": user_id})

#         if hierarchy[user.role] >= hierarchy[current_user.role]:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Cannot modify admin users",
#             )
#         user_data = {}
#         for k, v in data.model_dump().items():
#             if v is not None:
#                 user_data[k] = v

#         new_value = {"$set": user_data}

#         storage.db["users"].update_one({"_id": ObjectId(user_id)}, new_value)

#         message = {"message": "Account details changed"}
#         return JSONResponse(message, status.HTTP_200_OK)
#     except Exception as ex:
#         logger.error(ex)

#         raise ex


# @router.delete(path="/users/{user_id}/reject_account")
# def remove_user(
#     user_id: str, current_user: User = Depends(get_current_admin_user)
# ):
#     """Rejects an account request and/ or removes the user"""
#     logger = getLogger(__name__)
#     try:
#         user = storage.verify_user_record({"_id": user_id})

#         if hierarchy[user.role] >= hierarchy[current_user.role]:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Cannot modify admin users",
#             )

#         storage.delete_user_record(user_id)

#         # try:
#         #     email_verification.send_account_rejection(user["email"])
#         # except SMTPRecipientsRefused as ex:
#         #     logger.error(ex)
#         #     raise HTTPException(
#         #         status_code=status.HTTP_400_BAD_REQUEST,
#         #         detail="Unable to send emails. Ensure email address is valid.",
#         #     )

#         message = {"message": "Account removed"}
#         return JSONResponse(message, status.HTTP_202_ACCEPTED)
#     except Exception as ex:
#         logger.error(ex)

#         raise ex
