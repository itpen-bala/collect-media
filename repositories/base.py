from dataclasses import dataclass

from db.postgres import Database


@dataclass
class BaseRepository:
    db: Database
