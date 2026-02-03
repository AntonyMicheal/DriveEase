from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.config import settings
from core.dependencies import get_db
from modules.users import service as user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        subject: str | None = payload.get("sub")
        if subject is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = user_service.get_user_by_email(db, subject)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(user=Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def get_current_admin(user=Depends(get_current_active_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
