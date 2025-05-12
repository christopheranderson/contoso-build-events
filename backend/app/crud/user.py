from typing import Any
from uuid import UUID  # Import UUID for type annotations

from sqlmodel import Session, select

from ..core.security import get_password_hash, verify_password
from ..models import User, UserCreate, UserUpdate
from ..models.user import UserProfile


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def get_user_profile(*, session: Session, user_id: UUID) -> UserProfile | None:
    return session.exec(select(UserProfile).where(UserProfile.user_id == user_id)).one_or_none()


def create_user_profile(*, session: Session, user_id: UUID, profile_data: dict) -> UserProfile:
    db_profile = UserProfile(user_id=user_id, **profile_data)
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile


def update_user_profile(*, session: Session, db_profile: UserProfile, profile_data: dict) -> UserProfile:
    for field, value in profile_data.items():
        setattr(db_profile, field, value)
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile


def delete_user_profile(*, session: Session, user_id: UUID) -> None:
    db_profile = get_user_profile(session=session, user_id=user_id)
    if db_profile:
        session.delete(db_profile)
        session.commit()