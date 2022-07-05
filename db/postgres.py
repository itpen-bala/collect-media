import datetime

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from .base import metadata

image_files = sqlalchemy.Table(
    "image_files",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("uuid", UUID, unique=True, nullable=False),
    sqlalchemy.Column("url", sqlalchemy.VARCHAR, nullable=False),
    sqlalchemy.Column("ftp_path", sqlalchemy.VARCHAR, nullable=False),
    sqlalchemy.Column("format", sqlalchemy.VARCHAR, nullable=False),
    sqlalchemy.Column("width", sqlalchemy.SmallInteger, nullable=False),
    sqlalchemy.Column("height", sqlalchemy.SmallInteger, nullable=False),
    sqlalchemy.Column("image_size", sqlalchemy.ARRAY(sqlalchemy.SmallInteger), nullable=False),
    sqlalchemy.Column("file_size", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)
