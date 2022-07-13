from dataclasses import dataclass

from db.db import Database


@dataclass
class BaseRepository:
    db: Database
