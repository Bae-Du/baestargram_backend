from fastapi import APIRouter

from app.core.deps import CurrentUser, DBSession
from app.schemas.post import PostRead

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("", response_model=list[PostRead])
def get_feed(db: DBSession, current_user: CurrentUser) -> list[PostRead]:
    return []
