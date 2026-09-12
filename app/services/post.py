from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.comment import Comment  # noqa: F401
from app.models.like import Like  # noqa: F401
from app.models.post import Post, PostMedia
from app.models.user import User
from app.schemas.post import PostCreate, PostMediaRead, PostRead, PostUpdate
from app.schemas.user import UserPublic
from app.utils.profanity import reject_if_profane


def _load_options():
    return (
        selectinload(Post.author),
        selectinload(Post.media),
        selectinload(Post.likes),
        selectinload(Post.comments),
    )


def _to_post_read(post: Post, current_user: User | None = None) -> PostRead:
    liked_by_me = False
    if current_user is not None:
        liked_by_me = any(like.user_id == current_user.id for like in post.likes)
    return PostRead(
        id=post.id,
        caption=post.caption,
        created_at=post.created_at,
        author=UserPublic.model_validate(post.author),
        media=[PostMediaRead.model_validate(item) for item in post.media],
        like_count=len(post.likes),
        comment_count=len(post.comments),
        liked_by_me=liked_by_me,
    )


def _get_loaded_post(db: Session, post_id: int) -> Post | None:
    return db.scalar(select(Post).options(*_load_options()).where(Post.id == post_id))


def list_posts(
    db: Session,
    current_user: User | None = None,
    username: str | None = None,
) -> list[PostRead]:
    stmt = select(Post).options(*_load_options())
    if username:
        stmt = stmt.join(Post.author).where(User.username == username)
    stmt = stmt.order_by(Post.created_at.desc())
    posts = db.scalars(stmt).unique().all()
    return [_to_post_read(post, current_user) for post in posts]


def create_post(db: Session, current_user: User, payload: PostCreate) -> PostRead:
    media_urls = [url.strip() for url in payload.media_urls if url.strip()]
    if not media_urls:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one media url is required",
        )

    reject_if_profane(payload.caption)
    post = Post(user_id=current_user.id, caption=payload.caption)
    db.add(post)
    db.flush()
    for index, url in enumerate(media_urls):
        db.add(
            PostMedia(
                post_id=post.id,
                url=url,
                media_type="image",
                sort_order=index,
            )
        )
    db.commit()

    created = _get_loaded_post(db, post.id)
    if created is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load created post",
        )
    return _to_post_read(created, current_user)


def get_post(
    db: Session, post_id: int, current_user: User | None = None
) -> PostRead:
    post = _get_loaded_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return _to_post_read(post, current_user)


def _require_owned_post(db: Session, post_id: int, current_user: User) -> Post:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not post owner")
    return post


def update_post(db: Session, post_id: int, current_user: User, payload: PostUpdate) -> PostRead:
    post = _require_owned_post(db, post_id, current_user)
    if payload.caption is not None:
        caption = payload.caption.strip() or None
        reject_if_profane(caption)
        post.caption = caption
    db.add(post)
    db.commit()
    return get_post(db, post_id, current_user)


def delete_post(db: Session, post_id: int, current_user: User) -> None:
    post = _require_owned_post(db, post_id, current_user)
    db.delete(post)
    db.commit()
