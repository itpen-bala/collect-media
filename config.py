import yaml
import typing as t
from loguru import logger
from pydantic import BaseModel
from fastapi import FastAPI


def get_settings_from_yaml(conf_path: str) -> t.Dict:
    settings = {}
    try:
        logger.info('Reading config file')
        with open(conf_path) as conf_file:
            settings.update(yaml.load(conf_file, Loader=yaml.FullLoader))
            return settings
    except EnvironmentError as err:
        logger.error(f'Cannot read settings from file {conf_file}: {err}')
    except yaml.YAMLError as err:
        logger.error(f'Cannot read settings from file {conf_file}: {err}')


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


settings = AllSettings.parse_obj(get_settings_from_yaml('config.yaml'))
app = FastAPI()
