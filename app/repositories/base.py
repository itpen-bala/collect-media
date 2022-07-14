from dataclasses import dataclass

from app.db.postgres import Database


@dataclass
class BaseRepository:
    db: Database
