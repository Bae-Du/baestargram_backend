from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserPublic


class PostMediaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    media_type: str
    sort_order: int


class PostCreate(BaseModel):
    caption: str | None = None
    media_urls: list[str] = Field(min_length=1)


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    caption: str | None
    created_at: datetime
    author: UserPublic
    media: list[PostMediaRead]
    like_count: int = 0
    comment_count: int = 0
    liked_by_me: bool = False
