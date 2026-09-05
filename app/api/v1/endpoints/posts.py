from fastapi import APIRouter, status

from app.core.deps import CurrentUser, DBSession
from app.schemas.common import Message
from app.schemas.post import PostCreate, PostRead
from app.services import post as post_service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=list[PostRead])
def list_posts(db: DBSession) -> list[PostRead]:
    return post_service.list_posts(db)


@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: DBSession, current_user: CurrentUser) -> PostRead:
    return post_service.create_post(db, current_user, payload)


@router.get("/{post_id}", response_model=PostRead)
def get_post(post_id: int, db: DBSession) -> PostRead:
    return post_service.get_post(db, post_id)


@router.delete("/{post_id}", response_model=Message)
def delete_post(post_id: int, db: DBSession, current_user: CurrentUser) -> Message:
    post_service.delete_post(db, post_id, current_user)
    return Message(message="Post deleted")
