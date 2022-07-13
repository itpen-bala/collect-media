from uuid import UUID
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
    status,
    HTTPException,
)
from PIL import UnidentifiedImageError
from loguru import logger

from api.dependens import get_image_service
from service.images import ImageService
from model.images import Image
from exceptions import InternalServerException

router = APIRouter(prefix='/images')


@router.post('/download-image')
async def download_image(
        request: Request,
        image_service: ImageService = Depends(get_image_service),
) -> Response:
    """Getting URL and UUID from client for downloading image file from this URL.
    The file is uploaded to the FTP server as a temporary file until client confirmation
    (see the method "confirm_image").
    UUID from client and FTP path of this file is uploaded to redis as KEY and VALUE.

    TODO: add deleting a temporary file from FTP server and deleting information about
     this file from Redis after a timeout, if there is no confirmation of saving the file."""
    image_url = await request.body()
    try:
        uuid = await image_service.download_image(image_url.decode())
    except UnidentifiedImageError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(content=f"{{'UUID': {uuid}}}", media_type="application/json")


@router.put('/confirm-image/{uuid}')
async def confirm_image(
        uuid: UUID,
        image_service: ImageService = Depends(get_image_service),
) -> Optional[Image]:
    """Receiving confirmation from the client, that the temporary file with this UUID should
    become a permanent file. And information about this file with its parameters is inserting
    into SQL database."""
    image = await image_service.confirm_image(uuid)
    return image


@router.get('/info-by-uuid/{uuid}')
async def get_image_info_by_uuid(
        uuid: UUID,
        image_service: ImageService = Depends(get_image_service),
) -> Optional[Image]:
    image = await image_service.get_image_info_by_uuid(uuid)
    if image is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return image


@router.get('/info-by-id/{image_id}')
async def get_image_info_by_id(
        image_id: int,
        image_service: ImageService = Depends(get_image_service),
):
    image = await image_service.get_image_info_by_id(image_id)
    if image is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return image


@router.delete('/delete/{uuid}')
async def delete_image(
        uuid: UUID,
        image_service: ImageService = Depends(get_image_service),
) -> Optional[Image]:
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
