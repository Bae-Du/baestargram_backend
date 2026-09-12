from fastapi import APIRouter

from app.core.deps import CurrentUser, DBSession
from app.schemas.post import PostRead
from app.services import post as post_service

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("", response_model=list[PostRead])
def get_feed(db: DBSession, current_user: CurrentUser) -> list[PostRead]:
    return post_service.list_posts(db, current_user)
