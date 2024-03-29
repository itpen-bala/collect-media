import datetime
from pydantic import BaseModel
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base, ConcreteBase
from sqlalchemy.dialects.postgresql import UUID as SQLUUID


class Base:
    @classmethod
    def get_real_column_name(cls, attr_name: str) -> str:
        return getattr(sa.inspect(cls).c, attr_name).name


MediaBase: ConcreteBase = declarative_base(cls=Base)


class Image(MediaBase):
    __tablename__ = "image_files"

    uuid = sa.Column("uuid", SQLUUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    url = sa.Column("url", sa.VARCHAR, nullable=False)
    ftp_path = sa.Column("ftp_path", sa.VARCHAR, nullable=False)
    format = sa.Column("format", sa.VARCHAR, nullable=False)
    width = sa.Column("width", sa.SmallInteger, nullable=False)
    height = sa.Column("height", sa.SmallInteger, nullable=False)
    image_size = sa.Column("image_size", sa.ARRAY(sa.SmallInteger), nullable=False)  # size in pixel array
    file_size = sa.Column("file_size", sa.Integer, nullable=False)  # size in bytes
    created_at = sa.Column("created_at", sa.DateTime, default=datetime.datetime.utcnow())
    updated_at = sa.Column("updated_at", sa.DateTime, default=datetime.datetime.utcnow())

    @classmethod
    def build(
            cls,
            uuid: SQLUUID,
            url: str,
            ftp_path: str,
            format: str,
            width: int,
            height: int,
            image_size: tuple[int, int],
            file_size: int,
            created_at: datetime,
            updated_at: datetime,
    ):
        return cls(
            uuid=uuid,
            url=url,
            ftp_path=ftp_path,
            format=format,
            width=width,
            height=height,
            image_size=image_size,
            file_size=file_size,
            created_at=created_at,
            updated_at=updated_at,
        )


class MediaURL(BaseModel):
    url: str


class MediaUUID(BaseModel):
    uuid: UUID
