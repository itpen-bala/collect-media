from uuid import UUID

from fastapi import APIRouter, Response, status
from PIL import UnidentifiedImageError
from loguru import logger

import service.image_service as image_service
from model.images import BaseImage, Image

router = APIRouter(prefix='/images')


@router.post('/download-image')
async def download_image(image: BaseImage) -> Response:
    try:
        received_image = await image_service.download_image(image)
    except UnidentifiedImageError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return received_image


@router.put('/confirm-image/{uuid}')
async def confirm_image(uuid: UUID) -> Image:
    image = await image_service.confirm_image(uuid)
    return image


@router.get('/get')
async def get():
    await image_service.get_uuid()
    return status.HTTP_200_OK


@router.delete('/')
async def delete_key():
    await image_service.delete_key()
