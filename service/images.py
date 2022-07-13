import os
import io
import datetime
from uuid import UUID, uuid4
from typing import Optional

from loguru import logger
from PIL import Image as PILImage, UnidentifiedImageError

from main import app
from config import settings
from client.client import create_session
from storage.ftp import FTPClient
from model.images import Image, MediaUUID
from repositories.images import ImageRepository


class ImageService:
    def __init__(self, repository: ImageRepository):
        self.image_repository = repository
        self._ftp = FTPClient()

    async def download_image(self, image_url: str) -> MediaUUID:
        data = io.BytesIO(await create_session(image_url))
        try:
            rcvd_image = PILImage.open(data)
            logger.info(f'Received file with format {rcvd_image.format}')
        except UnidentifiedImageError as err:
            logger.info('Can\'t download_image image. ', err)
            raise UnidentifiedImageError

        uuid = uuid4()
        ftp = FTPClient()
        ftp.mkd(parent_dir='/', directory=settings.ftp.tmpimagepath)
        data.seek(0)
        ftp.upload_opened_file(file=data, ftp_path=os.path.join(settings.ftp.tmpimagepath, str(uuid)))

        await app.state.redis.set(str(uuid), image_url)
        return MediaUUID.parse_obj({"uuid": uuid})

    async def confirm_image(self, uuid: UUID) -> Optional[Image]:
        str_uuid = str(uuid)
        image_url = await app.state.redis.get(str_uuid)
        image_url = image_url.decode('utf-8')
        logger.info(f'URL: {image_url}')

        src_file = settings.ftp.tmpimagepath + '/' + str_uuid
        dst_file = os.path.join(settings.ftp.imagepath, str_uuid)
        image = PILImage.open(self._ftp.get_opened_file(src_file))

        image_for_db = Image.build(
            uuid=uuid,
            url=image_url,
            ftp_path=dst_file,
            format=image.format,
            width=image.width,
            height=image.height,
            image_size=image.size,  # size in pixel array (for example: 1600 x 1200)
            file_size=self._ftp.get_size(src_file),  # size in bytes
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        inserting_image = await self.image_repository.create(image_for_db)

        self._ftp.mkd(parent_dir='/', directory=settings.ftp.imagepath)
        self._ftp.move_file(src_file=src_file, dst_file=dst_file)
        await app.state.redis.delete(str_uuid)

        return inserting_image

    async def get_image_info_by_uuid(self, uuid: UUID) -> Optional[Image]:
        return await self.image_repository.get_info_by_uuid(uuid)

    async def get_image_info_by_id(self, image_id: int) -> Optional[Image]:
        return await self.image_repository.get_info_by_id(image_id)

    async def delete_image(self, uuid: UUID) -> Optional[Image]:
        image = await self.image_repository.delete(uuid)
        if image is not None:
            self._ftp.delete(image.ftp_path)
            # TODO: added rollback if not possible to delete image file from FTP-server
        return image
