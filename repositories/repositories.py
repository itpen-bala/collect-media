import datetime

from loguru import logger
from databases import Database

from model.images import Image
from db.postgres import image_files


class BaseRepository:
    def __init__(self, db: Database):
        self.db = db
        print('DB: ', self.db)


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
