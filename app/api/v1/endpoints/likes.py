from fastapi import APIRouter, HTTPException, status

from app.core.deps import CurrentUser, DBSession
from app.schemas.common import Message

router = APIRouter(tags=["likes"])


@router.post("/posts/{post_id}/like", response_model=Message)
def like_post(post_id: int, db: DBSession, current_user: CurrentUser) -> Message:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.delete("/posts/{post_id}/like", response_model=Message)
def unlike_post(post_id: int, db: DBSession, current_user: CurrentUser) -> Message:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
