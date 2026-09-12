from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentRead
from app.utils.profanity import reject_if_profane


def list_comments(db: Session, post_id: int) -> list[CommentRead]:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    comments = db.scalars(
        select(Comment)
        .where(Comment.post_id == post_id)
        .options(selectinload(Comment.author))
        .order_by(Comment.created_at.asc())
    ).all()
    return [CommentRead.model_validate(comment) for comment in comments]


def create_comment(
    db: Session,
    post_id: int,
    current_user: User,
    payload: CommentCreate,
) -> CommentRead:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    content = payload.content.strip()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Comment cannot be empty",
        )
    reject_if_profane(content)

    parent_id = payload.parent_id
    if parent_id is not None:
        parent = db.get(Comment, parent_id)
        if parent is None or parent.post_id != post_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid parent comment",
            )
        parent_id = parent.parent_id or parent.id

    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=content,
        parent_id=parent_id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    comment = db.scalar(
        select(Comment)
        .where(Comment.id == comment.id)
        .options(selectinload(Comment.author))
    )
    return CommentRead.model_validate(comment)
