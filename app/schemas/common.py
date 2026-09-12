from pydantic import BaseModel


class Message(BaseModel):
    message: str


class UploadRead(BaseModel):
    url: str


class LikeStatus(BaseModel):
    liked: bool
    like_count: int
