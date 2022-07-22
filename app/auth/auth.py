from datetime import datetime, timedelta

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt  # type:ignore

from app.config import settings

ALGORITHM = "HS256"


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            self.validate_token(token=credentials.credentials)
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authorization code.",
        )

    def validate_token(self, token: str):
        try:
            jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
            return True
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )


jwt_bearer = JWTBearer()


def generate_token():
    expire = datetime.utcnow() + timedelta(
        minutes=settings.jwt_expiration_time_min
    )
    to_encode: dict = {"exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=ALGORITHM
    )
    return encoded_jwt
