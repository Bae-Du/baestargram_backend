from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostRead


def list_posts(db: Session, current_user: User | None = None) -> list[PostRead]:
    return []


def create_post(db: Session, current_user: User, payload: PostCreate) -> PostRead:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


def get_post(db: Session, post_id: int, current_user: User | None = None) -> Post:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


def delete_post(db: Session, post_id: int, current_user: User) -> None:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
