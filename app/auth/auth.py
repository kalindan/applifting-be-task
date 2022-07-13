from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from app.config.config import config
from jose import JWTError, jwt  # type:ignore
from app.db.database import Session, get_session


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_token():
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode: dict = {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def validate_token(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
    return
