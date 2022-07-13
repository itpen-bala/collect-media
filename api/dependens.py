from fastapi import Depends
from starlette.requests import Request

from db.db import Database
from repositories.images import ImageRepository
from service.image import ImageService


def get_database_client(request: Request) -> Database:
    return request.app.state.db


def get_image_repository(db: Database = Depends(get_database_client, use_cache=True)) -> ImageRepository:
    return ImageRepository(db=db)


def get_image_service(repository: ImageRepository = Depends(get_image_repository, use_cache=True)) -> ImageService:
    return ImageService(repository=repository)
