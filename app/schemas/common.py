from pydantic import BaseModel


class Message(BaseModel):
    message: str


class UploadRead(BaseModel):
    url: str
