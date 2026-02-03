from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.dependencies import get_db
from core.security import create_access_token, get_password_hash, verify_password
from modules.auth.schema import Token
from modules.users import schema as user_schema
from modules.users import service as user_service
from modules.auth.dependencies import get_current_active_user

router = APIRouter()


@router.post("/register", response_model=user_schema.UserOut)
def register(payload: user_schema.UserCreate, db: Session = Depends(get_db)):
    existing = user_service.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = get_password_hash(payload.password)
    is_first_user = user_service.count_users(db) == 0
    return user_service.create_user(db, payload, hashed, is_admin=is_first_user)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_service.get_user_by_email(db, form_data.username)
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=user_schema.UserOut)
def me(current_user=Depends(get_current_active_user)):
    return current_user
