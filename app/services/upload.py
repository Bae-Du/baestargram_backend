from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.utils.storage import upload_dir

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}
MAX_BYTES = 8 * 1024 * 1024


def save_image(file: UploadFile) -> str:
    content_type = (file.content_type or "").lower()
    suffix = ALLOWED_TYPES.get(content_type)
    if suffix is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only jpeg, png, webp, or gif images are allowed",
        )

    data = file.file.read()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file",
        )
    if len(data) > MAX_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image is too large",
        )

    filename = f"{uuid4().hex}{suffix}"
    path: Path = upload_dir() / filename
    path.write_bytes(data)
    return f"/uploads/{filename}"
