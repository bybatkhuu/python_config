# -*- coding: utf-8 -*-

import os

from onion_config import ConfigBase

from utils.validator_schemas import config_schema


def _pre_load(config):
    try:
        config.env = os.getenv('ENV', config.env).strip().lower()

        if config.env == 'production':
            config.app.debug = False

            if os.getenv('APP_SECRET') is None:
                raise KeyError("Missing required `APP_SECRET` environment variable on 'production'!")

        config.app.port = os.getenv('APP_PORT', config.app.port)
        config.app.debug = os.getenv('APP_DEBUG', config.app.debug)
        config.app.secret = os.getenv('APP_SECRET', config.app.secret)
    except Exception as err:
        print(f"ERROR: Error occured while pre-loading config:\n {err}")
        exit(2)

    return config


config = ConfigBase(pre_load=_pre_load, valid_schema=config_schema).load()
