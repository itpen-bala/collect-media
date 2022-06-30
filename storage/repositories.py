import datetime

from databases import Database

from model.images import ImageCreate
from storage.postgres import images


class BaseRepository:
    def __init__(self, db: Database):
        self.db = db


class ImageRepository(BaseRepository):

    async def create(self, image: ImageCreate) -> ImageCreate:
        image = ImageCreate(
            uuid=image.uuid,
            url=image.url,
            format=image.format,
            size=image.size,
            width=image.width,
            height=image.heigth,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        values = image.dict()
        values.pop('id')
        query = images.insert().values(**values)
        image.id = await self.db.execute(query=query)
        return image
