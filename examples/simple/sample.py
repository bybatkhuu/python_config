#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

from onion_config import ConfigBase


_valid_schema = {
    'hostname': { 'type': 'string' },
    'username': { 'type': 'string' },
    'password': { 'type': 'string' },
    'port': { 'type': 'integer', 'coerce': int }
}

def _pre_load(config):
    config.port = '8080'
    config.opt_val = 'optional value'
    return config

config = ConfigBase(pre_load=_pre_load, valid_schema=_valid_schema).load()


if __name__ == '__main__':
    print(config.hostname)
    print(config.username)
    print(config.port)
    print(config.opt_val)
    pprint(config.to_dict())
