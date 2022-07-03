import datetime

from databases import Database

from model.images import ImageCreate
from db.postgres import images


class BaseRepository:
    def __init__(self, db: Database):
        self.db = db


class ImageRepository(BaseRepository):

    async def create(self, image: ImageCreate) -> ImageCreate:
        image = ImageCreate(
            uuid=image.uuid,
            url=image.url,
            format=image.format,
            width=image.width,
            height=image.height,
            image_size=image.image_size,
            file_size=image.file_size,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = image.dict()
        values.pop('id')
        query = images.insert().values(**values)
        image.id = await self.db.execute(query=query)
        return image
