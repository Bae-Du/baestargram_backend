from fastapi import APIRouter, HTTPException, status

from app.core.deps import CurrentUser, DBSession
from app.schemas.common import Message
from app.schemas.user import UserPublic, UserUpdate
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/me", response_model=UserPublic)
def update_me(payload: UserUpdate, db: DBSession, current_user: CurrentUser) -> UserPublic:
    return user_service.update_me(db, current_user, payload)


@router.get("/{username}", response_model=UserPublic)
def get_user(username: str, db: DBSession) -> UserPublic:
    return user_service.get_user_by_username(db, username)


@router.post("/{username}/follow", response_model=Message)
def follow_user(username: str, db: DBSession, current_user: CurrentUser) -> Message:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.delete("/{username}/follow", response_model=Message)
def unfollow_user(username: str, db: DBSession, current_user: CurrentUser) -> Message:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/{username}/followers", response_model=list[UserPublic])
def list_followers(username: str, db: DBSession) -> list[UserPublic]:
    return []


@router.get("/{username}/following", response_model=list[UserPublic])
def list_following(username: str, db: DBSession) -> list[UserPublic]:
    return []
