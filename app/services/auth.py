from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, SignupRequest
from app.schemas.user import UserMe
from app.utils.profanity import reject_if_profane


def _to_auth_response(user: User) -> AuthResponse:
    return AuthResponse(
        access_token=create_access_token(str(user.id)),
        user=UserMe.model_validate(user),
    )


def signup_user(db: Session, payload: SignupRequest) -> AuthResponse:
    existing = db.scalar(
        select(User).where(
            or_(User.username == payload.username, User.email == payload.email)
        )
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        )

    reject_if_profane(payload.username, payload.display_name)
    display_name = (payload.display_name or "").strip() or payload.username
    reject_if_profane(display_name)
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        display_name=display_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _to_auth_response(user)


def login_user(db: Session, payload: LoginRequest) -> AuthResponse:
    user = db.scalar(
        select(User).where(
            or_(User.username == payload.username, User.email == payload.username)
        )
    )
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )

    return _to_auth_response(user)
