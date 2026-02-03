from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from core.config import settings

ALLOWED_IMAGE_TYPES: dict[str, str] = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def get_media_root() -> Path:
    return Path(settings.MEDIA_ROOT)


def save_image_upload(file: UploadFile, subdir: str) -> str:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image type")

    ext = ALLOWED_IMAGE_TYPES[file.content_type]
    filename = f"{uuid4().hex}{ext}"

    media_root = get_media_root()
    target_dir = media_root / subdir
    target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / filename
    with target_path.open("wb") as buffer:
        buffer.write(file.file.read())

    return f"{settings.MEDIA_URL}/{subdir}/{filename}"
