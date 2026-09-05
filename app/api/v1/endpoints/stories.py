from fastapi import APIRouter, HTTPException, status

from app.core.deps import CurrentUser, DBSession
from app.schemas.story import StoryCreate, StoryRead

router = APIRouter(prefix="/stories", tags=["stories"])


@router.get("", response_model=list[StoryRead])
def list_stories(db: DBSession, current_user: CurrentUser) -> list[StoryRead]:
    return []


@router.post("", response_model=StoryRead, status_code=status.HTTP_201_CREATED)
def create_story(
    payload: StoryCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> StoryRead:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
