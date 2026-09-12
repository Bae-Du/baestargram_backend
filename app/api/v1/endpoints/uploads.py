from fastapi import APIRouter, UploadFile

from app.core.deps import CurrentUser
from app.schemas.common import UploadRead
from app.services import upload as upload_service

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("", response_model=UploadRead)
def upload_image(file: UploadFile, current_user: CurrentUser) -> UploadRead:
    _ = current_user
    return UploadRead(url=upload_service.save_image(file))
