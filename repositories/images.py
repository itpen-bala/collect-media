import datetime
from uuid import UUID
from typing import Optional

from loguru import logger

from .base import BaseRepository
from db.tables import Image


class ImageRepository(BaseRepository):

    async def create(self, image: Image) -> Image:
        async with self.db.session() as session:
            session.add(image)
            await session.commit()
            await session.refresh(image)
        return image

    async def get_info_by_uuid(self, uuid: UUID) -> Optional[Image]:
        return None
        """
        query = image_files.select().where(image_files.c.uuid == uuid)
        image = await self.db.fetch_one(query=query)
        if not image:
            return None
        return Image.parse_obj(image)
        """

    async def get_info_by_id(self, image_id: int) -> Optional[Image]:
        return None
        """
        query = image_files.select().where(image_files.c.id == image_id)
        image = await self.db.fetch_one(query=query)
        if not image:
            return None
        return Image.parse_obj(image)
        """
    async def delete(self, uuid: UUID) -> Optional[Image]:
        return None
        """
        query = image_files.select().where(image_files.c.uuid == uuid)
        image = await self.db.fetch_one(query=query)
        if not image:
            return None
        query = image_files.delete().where(image_files.c.uuid == uuid)
        await self.db.execute(query=query)
        return Image.parse_obj(image)
        """
