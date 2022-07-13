from typing import Dict

import yaml
from loguru import logger

from app.model.settings import AllSettings


def get_settings_from_yaml(conf_path: str) -> Dict:
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


settings = AllSettings.parse_obj(get_settings_from_yaml('app/config.yaml'))
