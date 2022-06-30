from uuid import UUID

from fastapi import APIRouter, Response, status
from PIL import UnidentifiedImageError
from loguru import logger

from model.images import Image
from service.image_service import download_image, confirm_image, get_uuid

router = APIRouter(prefix='/images')


@router.post('/download')
async def download(image: Image) -> Response:
    try:
        received_image = await download_image(image)
    except UnidentifiedImageError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return received_image


@router.put('/confirm/{uuid}')
async def confirm(uuid: UUID) -> Response:
    try:
        result = await confirm_image(uuid)
    except Exception as err:
        logger.error(err)
    return Response(status_code=status.HTTP_200_OK)


@router.get('/get')
async def get():
    await get_uuid()
    return status.HTTP_200_OK
