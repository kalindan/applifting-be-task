import secrets

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.auth.auth import generate_token
from app.config import config
from app.models.login_model import LoginInfo

router = APIRouter(prefix="/login", tags=["Admin"])


@router.post("")
def login_admin(login: LoginInfo):
    correct_username = secrets.compare_digest(
        login.username, config.admin_username
    )
    correct_password = secrets.compare_digest(
        login.password, config.admin_password
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )
    jwt = generate_token()
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Admin logged in",
            "access_token": jwt,
            "token_type": "Bearer",
        },
    )
