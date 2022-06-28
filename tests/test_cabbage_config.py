# -*- coding: utf-8 -*-

import logging
import unittest

import pytest

from onion_config import ConfigBase

logger = logging.getLogger(__name__)


class TestOnionConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("Starting 'onion_config' unittest...\n")

    @classmethod
    def tearDownClass(cls):
        logger.info("Successfully tested 'onion_config'.")

    def test_init(self):
        logger.info("Testing initialization of 'onion_config' modules...")
        self.assertIsNotNone(ConfigBase)
        logger.info('Done.\n')


@pytest.mark.parametrize('configs_dir, required_envs, pre_load, valid_schema, expected', [
    ('configs', [], lambda config: config, {}, True)
])
def test_config_base(configs_dir, required_envs, pre_load, valid_schema, expected):
    config = ConfigBase(configs_dir, required_envs, pre_load, valid_schema).load()

    assert (config is not None) == expected
