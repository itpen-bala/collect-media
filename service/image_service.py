import os
import io
import datetime
from uuid import UUID

from loguru import logger
from PIL import Image as PILImage, UnidentifiedImageError

from config import settings, app
from client.client import create_session
from storage.ftp import FTPClient
from model.images import BaseImage, Image
from db.base import database
from repositories.repositories import ImageRepository

__image_repository = ImageRepository(database)


async def download_image(image: BaseImage):
    uuid = str(image.uuid)
    data = io.BytesIO(await create_session(image.url))
    try:
        rcvd_image = PILImage.open(data)
        logger.info(f'Received file with format {rcvd_image.format}')

    except UnidentifiedImageError as err:
        logger.info('Can\'t download_image image. ', err)
        raise UnidentifiedImageError

    ftp = FTPClient()
    ftp.mkd(parent_dir='/', directory=settings.ftp.tmpimagepath)
    data.seek(0)
    ftp.upload_opened_file(file=data, ftp_path=os.path.join(settings.ftp.tmpimagepath, uuid))

    await app.state.redis.set(uuid, image.url)
    return image


async def confirm_image(uuid: UUID):
    uuid = str(uuid)
    image_url = await app.state.redis.get(uuid)
    logger.info(f'URL: {image_url}')

    ftp = FTPClient()
    src_file = settings.ftp.tmpimagepath + '/' + uuid
    dst_file = os.path.join(settings.ftp.imagepath, uuid)
    image = PILImage.open(ftp.get_opened_file(src_file))

    image_for_db = Image(uuid=uuid,
                         url=image_url,
                         ftp_path=dst_file,
                         format=image.format,
                         width=image.width,
                         height=image.height,
                         image_size=image.size,
                         file_size=ftp.get_size(src_file),  # size in bytes
                         created_at=datetime.datetime.utcnow(),
                         updated_at=datetime.datetime.utcnow(),
                         )
    inserting_image = await __image_repository.create(image_for_db)

    ftp.mkd(parent_dir='/', directory=settings.ftp.imagepath)
    ftp.move_file(src_file=src_file, dst_file=dst_file)
    await app.state.redis.delete(uuid)

    return inserting_image


async def get_uuid():
    v = await app.state.redis.get('17a80487-0f33-49f9-b8cc-ba60bf79b0c9')
    logger.info('V: ', v)
    v = await app.state.redis.keys()
    logger.info('V: ', v)


async def delete_key():
    await app.state.redis.delete('17a80487-0f33-49f9-b8cc-ba60bf79b0c9')
