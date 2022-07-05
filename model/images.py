import datetime
from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class BaseImage(BaseModel):
    id: Optional[int] = None
    uuid: UUID
    url: str


class Image(BaseImage):
    ftp_path: str
    format: str
    width: int
    height: int
    image_size: tuple[int, int]
    file_size: int  # size in bytes
    created_at: datetime.datetime
    updated_at: datetime.datetime
