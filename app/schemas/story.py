from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserPublic


class StoryCreate(BaseModel):
    media_url: str
    media_type: str = Field(default="image")


class StoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    media_url: str
    media_type: str
    expires_at: datetime
    created_at: datetime
    author: UserPublic
