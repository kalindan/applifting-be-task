import secrets

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.auth import generate_token
from app.config import settings
from app.models import LoginInfo

router = APIRouter(prefix="/login", tags=["Admin"])


@router.post("")
def login_admin(login: LoginInfo):
    correct_username: bool = secrets.compare_digest(
        login.username, settings.admin_username
    )
    correct_password: bool = secrets.compare_digest(
        login.password, settings.admin_password
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    jwt = generate_token()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Admin logged in",
            "access_token": jwt,
            "token_type": "Bearer",
        },
    )
