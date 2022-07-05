import datetime
from uuid import UUID
from typing import Optional

from loguru import logger

from .base import BaseRepository
from model.images import Image
from db.postgres import image_files


class ImageRepository(BaseRepository):

    async def create(self, image: Image) -> Image:
        image = Image(
            uuid=image.uuid,
            url=image.url,
            ftp_path=image.ftp_path,
            format=image.format,
            width=image.width,
            height=image.height,
            image_size=image.image_size,
            file_size=image.file_size,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = image.dict()
        values.pop('id', None)
        query = image_files.insert().values(**values)
        await self.db.execute(query=query)

    async def delete(self, uuid: UUID) -> Optional[Image]:
        query = image_files.select().where(image_files.c.uuid == uuid)
        image = await self.db.fetch_one(query=query)
        if not image:
            return None
        else:
            query = image_files.delete().where(image_files.c.uuid == uuid)
            await self.db.execute(query=query)
            return Image.parse_obj(image)
