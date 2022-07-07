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
    """Getting URL and UUID from client for downloading image file from this URL.
    The file is uploaded to the FTP server as a temporary file until client confirmation
    (see the method "confirm_image").
    UUID from client and FTP path of this file is uploaded to redis as KEY and VALUE.

    TODO: add deleting a temporary file from FTP server and deleting information about
     this file from Redis after a timeout, if there is no confirmation of saving the file."""
    try:
        received_image = await image_service.download_image(image)
    except UnidentifiedImageError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return received_image


@router.put('/confirm-image/{uuid}')
async def confirm_image(uuid: UUID) -> Optional[Image]:
    """Receiving confirmation from the client, that the temporary file with this UUID should
    become a permanent file. And information about this file with its parameters is inserting
    into SQL database."""
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
    """Deleting a permanent image file from FTP server
    and deleting information about this file from SQL database."""
    try:
        image = await image_service.delete_image(uuid)
    except InternalServerException as err:
        logger.exception(err)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not image:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return image
