from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class Image(BaseModel):
    id: Optional[int] = None
    uuid: UUID
    url: str
