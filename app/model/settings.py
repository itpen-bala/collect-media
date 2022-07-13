from pydantic import BaseModel


class PostgreSQLSettings(BaseModel):
    url: str


class FTPSettings(BaseModel):
    host: str
    user: str
    passwd: str
    imagepath: str
    tmpimagepath: str


class RedisSettings(BaseModel):
    url: str


class AllSettings(BaseModel):
    postgresql: PostgreSQLSettings
    ftp: FTPSettings
    redis: RedisSettings
