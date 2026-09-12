from fastapi import APIRouter

from app.core.deps import CurrentUser, DBSession
from app.schemas.common import LikeStatus
from app.services import like as like_service

router = APIRouter(tags=["likes"])


@router.post("/posts/{post_id}/like", response_model=LikeStatus)
def like_post(post_id: int, db: DBSession, current_user: CurrentUser) -> LikeStatus:
    return like_service.like_post(db, post_id, current_user)


@router.delete("/posts/{post_id}/like", response_model=LikeStatus)
def unlike_post(post_id: int, db: DBSession, current_user: CurrentUser) -> LikeStatus:
    return like_service.unlike_post(db, post_id, current_user)
