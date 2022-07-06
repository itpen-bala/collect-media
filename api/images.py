from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Response, status, HTTPException
from PIL import UnidentifiedImageError
from loguru import logger

import service.image_service as image_service
from model.images import BaseImage, Image
from exceptions import InternalServerException

router = APIRouter(prefix='/images')


@router.post('/download-image')
async def download_image(image: BaseImage) -> Response:
    try:
        received_image = await image_service.download_image(image)
    except UnidentifiedImageError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return received_image


@router.put('/confirm-image/{uuid}')
async def confirm_image(uuid: UUID) -> Optional[Image]:
    image = await image_service.confirm_image(uuid)
    return image


@router.get('/info-by-uuid/{uuid}')
async def get_image_info_by_uuid(uuid: UUID) -> Optional[Image]:
    image = await image_service.get_image_info_by_uuid(uuid)
    if image is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return image


@router.get('/info-by-id/{image_id}')
async def get_image_info_by_id(image_id: int):
    image = await image_service.get_image_info_by_id(image_id)
    if image is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return image


@router.delete('/delete/{uuid}')
async def delete_image(uuid: UUID) -> Optional[Image]:
    try:
        image = await image_service.delete_image(uuid)
    except InternalServerException as err:
        logger.exception(err)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not image:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return image
