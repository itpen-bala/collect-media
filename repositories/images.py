from uuid import UUID
from typing import Optional

from sqlalchemy import select, delete

from .base import BaseRepository
from model.images import Image


class ImageRepository(BaseRepository):

    async def create(self, image: Image) -> Image:
        async with self.db.session() as session:
            session.add(image)
            await session.commit()
            await session.refresh(image)
        return image

    async def get_info_by_uuid(self, uuid: UUID) -> Optional[Image]:
        query = select(Image).where(Image.uuid == uuid)
        async with self.db.session() as session:
            result = await session.execute(query)
            image = result.scalar()
        if not image:
            return None
        return image

    async def get_info_by_id(self, image_id: int) -> Optional[Image]:
        query = select(Image).where(Image.id == image_id)
        async with self.db.session() as session:
            result = await session.execute(query)
            image = result.scalar()
        if not image:
            return None
        return image

    async def delete(self, uuid: UUID) -> Optional[Image]:
        query = select(Image).where(Image.uuid == uuid)
        async with self.db.session() as session:
            result = await session.execute(query)
            image = result.scalar()
            if not image:
                return None
            query = delete(Image).where(Image.uuid == uuid)
            await session.execute(query)
            await session.commit()
        return image
