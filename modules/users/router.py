from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from core.dependencies import get_db
from core.uploads import save_image_upload
from modules.auth.dependencies import get_current_active_user, get_current_admin
from modules.users import schema, service

router = APIRouter()


@router.get("/me", response_model=schema.UserOut)
def read_me(current_user=Depends(get_current_active_user)):
    return current_user


@router.patch("/me", response_model=schema.UserOut)
def update_me(
    payload: schema.UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return service.update_user(db, current_user, payload)


@router.post("/me/avatar", response_model=schema.UserOut)
def upload_my_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    avatar_url = save_image_upload(file, "users")
    payload = schema.UserUpdate(avatar_url=avatar_url)
    return service.update_user(db, current_user, payload)


@router.get("/", response_model=list[schema.UserOut])
def list_all(db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    return service.list_users(db)


@router.get("/{user_id}", response_model=schema.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    user = service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=schema.UserOut)
def update_user(
    user_id: int,
    payload: schema.UserUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    user = service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return service.update_user(db, user, payload)
