from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str | None
    bio: str | None
    profile_image_url: str | None
    website: str | None
    is_private: bool
    created_at: datetime


class UserMe(UserPublic):
    email: EmailStr


class UserUpdate(BaseModel):
    display_name: str | None = Field(default=None, max_length=100)
    bio: str | None = None
    website: HttpUrl | None = None
    is_private: bool | None = None
    profile_image_url: str | None = None
