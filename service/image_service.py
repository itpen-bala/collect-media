import os
import io
from uuid import UUID

from loguru import logger
from PIL import Image as PILImage, UnidentifiedImageError

from config import settings, app
from client.client import create_session
from storage.ftp import FTPClient
from model.images import BaseImage


async def download_image(image: BaseImage):
    uuid = str(image.uuid)
    data = io.BytesIO(await create_session(image.url))
    try:
        rcvd_image = PILImage.open(data)
        logger.info('Received file with format ', rcvd_image.format)
    except UnidentifiedImageError as err:
        logger.info('Can\'t download image. ', err)
        raise UnidentifiedImageError

    ftp = FTPClient()
    ftp.mkd(parent_dir='/', directory=settings.ftp.tmpimagepath)
    ftp.upload_opened_file(file=data, ftp_path=os.path.join(settings.ftp.tmpimagepath, uuid))

    await app.state.redis.set(uuid, image.url)
    return image


async def confirm_image(uuid: UUID):
    uuid = str(uuid)
    image_url = await app.state.redis.get(uuid)
    logger.info(f'URL: {image_url}')

    src_file = settings.ftp.tmpimagepath + '/' + uuid
    dst_file = os.path.join(settings.ftp.imagepath, uuid)
    ftp = FTPClient()
    ftp.mkd(parent_dir='/', directory=settings.ftp.imagepath)
    ftp.move_file(src_file=src_file, dst_file=dst_file)

    await app.state.redis.delete(uuid)


async def get_uuid():
    v = await app.state.redis.get('17a80487-0f33-49f9-b8cc-ba60bf79b0c9')
    logger.info('V: ', v)
    v = await app.state.redis.keys()
    logger.info('V: ', v)
