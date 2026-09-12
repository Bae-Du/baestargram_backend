from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.like import Like
from app.models.post import Post
from app.models.user import User
from app.schemas.common import LikeStatus


def _get_post(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


def _status(db: Session, post_id: int, user_id: int) -> LikeStatus:
    like_count = db.scalar(
        select(func.count()).select_from(Like).where(Like.post_id == post_id)
    )
    liked = (
        db.scalar(
            select(Like.id).where(Like.post_id == post_id, Like.user_id == user_id)
        )
        is not None
    )
    return LikeStatus(liked=liked, like_count=int(like_count or 0))


def like_post(db: Session, post_id: int, current_user: User) -> LikeStatus:
    _get_post(db, post_id)
    existing = db.scalar(
        select(Like).where(Like.post_id == post_id, Like.user_id == current_user.id)
    )
    if existing is None:
        db.add(Like(post_id=post_id, user_id=current_user.id))
        db.commit()
    return _status(db, post_id, current_user.id)


def unlike_post(db: Session, post_id: int, current_user: User) -> LikeStatus:
    _get_post(db, post_id)
    existing = db.scalar(
        select(Like).where(Like.post_id == post_id, Like.user_id == current_user.id)
    )
    if existing is not None:
        db.delete(existing)
        db.commit()
    return _status(db, post_id, current_user.id)
