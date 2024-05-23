from datetime import timedelta
from logging import getLogger
from typing import Dict

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError

from core.authentication.auth_token import (
    create_access_token,
    verify_access_token,
)
from core.storage import storage
from schemas import user as s_user
from schemas.token import EmailVerificationToken
from services.mailer import send_email_verification

router = APIRouter()


@router.post(path="/register", response_model=Dict[str, str])
def register_user(user_data: s_user.UserIn):
    """Registers a user"""
    logger = getLogger(__name__ + ".register_user")
    try:
        id = storage.create_user_record(user_data)

        verification_token = create_access_token(
            {"id": id, "sub": user_data.email, "type": "email_verification"},
            timedelta(hours=1),
        )

        send_email_verification(user_data.email, verification_token)

        response_message = {
            "message": "Account created successfully Email Verification sent.",
            "token_expire": "1 Hour",
            "email": user_data.email,
        }

        return JSONResponse(response_message)
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.post("/register/verify", response_model=Dict[str, str])
def verify_email(verification_token: EmailVerificationToken) -> JSONResponse:
    """Performs user email verification"""
    try:
        token_data = verify_access_token(verification_token.verification_token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Verification token expired",
        )

    if token_data.type != "email_verification":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type",
        )

    storage.update_user_record(
        filter={"email": token_data.email},
        update={"status": s_user.UserStatus.VERIFIED},
    )
    return JSONResponse({"message": "Account verified successfuly"})


@router.post("/register/verify/resend", response_model=Dict[str, str])
def resend_verification(email: str = Body(embed=True)) -> JSONResponse:
    """Resends email verification"""
    user = storage.verify_user_record({"email": email})

    if user.status != "unverified":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already verified",
        )

    verification_token = create_access_token(
        {
            "id": user.id,
            "sub": user.email,
            "type": "email_verification",
        },
        timedelta(hours=1),
    )

    send_email_verification(user.email, verification_token)

    response_message = {
        "message": "Email verification token resent",
        "token_expire": "1 Hour",
        "email": user.email,
    }

    return JSONResponse(response_message, status_code=200)
