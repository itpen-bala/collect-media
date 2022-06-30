import datetime

import sqlalchemy
from databases import Database
from sqlalchemy.dialects.postgresql import UUID

DATABASE_URL = ""


db = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL,
)

images = sqlalchemy.Table(
    "images",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("uuid", UUID(as_uuid=True), unique=True, nullable=False),
    sqlalchemy.Column("url", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("format", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("size", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("width", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("height", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)
