from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserUpdate
from app.utils.profanity import reject_if_profane


def get_user_by_username(db: Session, username: str) -> User:
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def update_me(db: Session, user: User, payload: UserUpdate) -> User:
    data = payload.model_dump(exclude_unset=True)
    if "website" in data and data["website"] is not None:
        data["website"] = str(data["website"])

    reject_if_profane(
        data.get("display_name") if isinstance(data.get("display_name"), str) else None,
        data.get("bio") if isinstance(data.get("bio"), str) else None,
    )
    for field, value in data.items():
        setattr(user, field, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
