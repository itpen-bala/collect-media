import datetime
from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class BaseImage(BaseModel):
    id: Optional[int] = None
    uuid: UUID
    url: str


class ImageCreate(BaseImage):
    format: str
    size: int
    width: int
    heigth: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ImageForUser(BaseImage):
    format: str
    size: int
    size: int
    width: int
    heigth: int
