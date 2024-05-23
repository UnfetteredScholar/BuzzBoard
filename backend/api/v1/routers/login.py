from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.authentication.auth_middleware import authenticate_user
from core.authentication.auth_token import create_access_token
from schemas.token import Token
from schemas.user import UserStatus

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """Performs user login"""
    try:
        logger = getLogger(f"{__name__}.login")
        user = authenticate_user(form_data.username, form_data.password)
        logger.info("User Authenticated")
        if user.status != UserStatus.VERIFIED.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account not verified",
            )

        logger.info("User Verified")
        token_data = {
            "sub": user.email,
            "id": user.id,
            # "role": user.role,
            "type": "bearer",
        }
        access_token = create_access_token(token_data)
        logger.info("User Token Generated")

        return Token(access_token=access_token, token_type="bearer")
    except Exception as ex:
        logger.error(ex)
        raise ex
