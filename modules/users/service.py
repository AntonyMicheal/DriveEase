from sqlalchemy.orm import Session

from core.security import get_password_hash
from modules.users.model import User
from modules.users.schema import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id).all()


def count_users(db: Session) -> int:
    return db.query(User).count()


def create_user(
    db: Session,
    data: UserCreate,
    hashed_password: str | None = None,
    is_admin: bool = False,
) -> User:
    password_hash = hashed_password or get_password_hash(data.password)
    user = User(
        email=data.email,
        hashed_password=password_hash,
        full_name=data.full_name,
        phone=data.phone,
        is_admin=is_admin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.phone is not None:
        user.phone = data.phone
    if data.is_active is not None:
        user.is_active = data.is_active
    if data.is_admin is not None:
        user.is_admin = data.is_admin
    if data.password:
        user.hashed_password = get_password_hash(data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
