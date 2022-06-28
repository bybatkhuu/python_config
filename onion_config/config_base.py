# -*- coding: utf-8 -*-

import os
import glob
import json
import logging
import pprint

import yaml
from box import Box
from dotenv import load_dotenv
from cerberus import Validator

logger = logging.getLogger(__name__)


class ConfigBase:
    """A core class of 'onion_python' module to use as the base configuration.

    Attributes:
        _CONFIGS_DIR  (str     ): Default configs directory. Defaults to '${PWD}/configs'.
        _PRE_LOAD     (function): Default lambda function for 'pre_load'. Defaults to <lambda config: config>.

        configs_dir   (str     ): Main configs directory to load all config files. Defaults to _CONFIGS_DIR.
        required_envs (str     ): Required environment variables to check. Defaults to []
        valid_schema  (dict    ): Validation schema to validate 'config'. This schema is based on 'Cerberus' package. Defaults to None.
        config        (box.Box ): Main 'config' object based on 'python-box' package. Defaults to Box().

    Methods:
        set_pre_load()         : Setting method for custom 'pre_load' method.
        load()                 : Load and validate every configs into 'config'.
        _load_dotenv()         : Loading environment variables from .env file, if it's exits.
        _check_required_envs() : Check required environment variables are exist or not.
        _load_config_files()   : Load config files from 'config_dir' into 'config'.
        _load_extra_configs()  : Load extra config files from 'PY_EXTRA_CONFIGS_DIR' into 'config'.
        _pre_load()            : Custom pre-load method, this method will executed before validating 'config'. Defaults to ConfigBase._PRE_LOAD.
        _validate()            : Validate the 'config' by 'valid_schema'.
        _freeze_config()       : Freeze 'config' into immutable variable.
    """

    _CONFIGS_DIR = os.path.join(os.getcwd(), 'configs')
    _PRE_LOAD = lambda config: config

    def __init__(self, configs_dir: str=_CONFIGS_DIR, required_envs: list=[], pre_load: callable=_PRE_LOAD, valid_schema: dict=None):
        """ConfigBase constructor method.

        Args:
            configs_dir   (str,      optional): Main configs directory to load all config files. Defaults to ConfigBase._CONFIGS_DIR.
            required_envs (list,     optional): Required environment variables to check. Defaults to [].
            pre_load      (function, optional): Custom pre-load method, this method will executed before validating 'config'. Defaults to ConfigBase._PRE_LOAD.
            valid_schema  (dict,     optional): Validation schema to validate 'config'. This schema is based on 'Cerberus' package. Defaults to None.
        """

        self.configs_dir = configs_dir
        self.required_envs = required_envs
        if valid_schema:
            self.valid_schema = valid_schema
        self.set_pre_load(pre_load)

        self.config = Box()


    def set_pre_load(self, pre_load: callable=_PRE_LOAD):
        """Setting method for custom 'pre_load' method.

        Args:
            pre_load (function, optional): Custom pre-load method, this method will executed before validating 'config'. Defaults to ConfigBase._PRE_LOAD.

        Raises:
            TypeError: If 'pre_load' argument type is not callable function.
        """

        if callable(pre_load):
            self._pre_load = pre_load
        else:
            try:
                raise TypeError(f"'pre_load' argument type <{type(pre_load).__name__}> is invalid, should be callable <function>!")
            except Exception as err:
                logger.exception(err)
                exit(2)


    def load(self):
        """Load and validate every configs into 'config'.

        Returns:
            Box(): Returns loaded config as a 'python-box' Box().
        """

        self._load_dotenv()
        self._check_required_envs()
        self._load_config_files()
        self._load_extra_configs()
        self.config = self._pre_load(self.config)
        if self.valid_schema:
            self._validate()
        self._freeze_config()
        return self.config


    def _load_dotenv(self):
        """Loading environment variables from .env file, if it's exits.
        """

        _env_filename = '.env'
        _env_file_path = os.path.join(os.getcwd(), _env_filename)
        if os.path.isfile(_env_file_path):
            load_dotenv(dotenv_path=_env_file_path, override=True, encoding='utf8')


    def _check_required_envs(self):
        """Check required environment variables are exist or not.
        """

        for _env in self.required_envs:
            try:
                os.environ[_env]
            except KeyError:
                logger.exception(f"Missing required '{_env}' environment variable.")
                exit(2)


    def _load_config_files(self):
        """Load config files from 'config_dir' into 'config'.
        """

        ## Loading all JSON config files from 'configs' directory:
        _json_file_paths = glob.glob(os.path.join(self.configs_dir, '*.json'))
        for _json_file_path in _json_file_paths:
            try:
                with open(_json_file_path, "r", encoding='utf8') as _json_file:
                    self.config.merge_update(Box(json.load(_json_file) or {}))
            except Exception:
                logger.exception(f"Failed to load '{_json_file_path}' json config file:")
                exit(2)

        ## Loading all YAML config files from 'configs' directory:
        _yaml_file_paths = glob.glob(os.path.join(self.configs_dir, '*.yml'))
        _yaml_file_paths.extend(glob.glob(os.path.join(self.configs_dir, '*.yaml')))
        for _yaml_file_path in _yaml_file_paths:
            try:
                with open(_yaml_file_path, "r", encoding='utf8') as _yaml_file:
                    self.config.merge_update(Box(yaml.safe_load(_yaml_file) or {}))
            except Exception:
                logger.exception(f"Failed to load '{_yaml_file_path}' yaml config file:")
                exit(2)


    def _load_extra_configs(self):
        """Load extra config files from 'PY_EXTRA_CONFIGS_DIR' into 'config'.
        """

        ## Checking 'PY_EXTRA_CONFIGS_DIR' directory exists, and if it exists, loads config files from that directory:
        _extra_configs_dir = os.getenv('PY_EXTRA_CONFIGS_DIR')
        if _extra_configs_dir and os.path.isdir(_extra_configs_dir):

            _json_file_paths = glob.glob(os.path.join(_extra_configs_dir, '*.json'))
            for _json_file_path in _json_file_paths:
                try:
                    with open(_json_file_path, "r", encoding='utf8') as _json_file:
                        self.config.merge_update(Box(json.load(_json_file) or {}))
                except Exception:
                    logger.exception(f"Failed to load '{_json_file_path}' json config file:")
                    exit(2)

            _yaml_file_paths = glob.glob(os.path.join(_extra_configs_dir, '*.yml'))
            _yaml_file_paths.extend(glob.glob(os.path.join(self.configs_dir, '*.yaml')))
            for _yaml_file_path in _yaml_file_paths:
                try:
                    with open(_yaml_file_path, "r", encoding='utf8') as _yaml_file:
                        self.config.merge_update(Box(yaml.safe_load(_yaml_file) or {}))
                except Exception:
                    logger.exception(f"Failed to load '{_yaml_file_path}' yaml config file:")
                    exit(2)


    def _validate(self):
        """Validate the 'config' by 'valid_schema'.

        Raises:
            ValueError: If 'config' is invalid based on 'valid_schema'.
        """

        try:
            _v = Validator(self.valid_schema)
            _v.allow_unknown = True
            _v.require_all = True
            if not _v.validate(self.config.to_dict()):
                _err_str = "The 'config' is invalid:\n"
                for _key, _value in _v.errors.items():
                    _err_str = _err_str + f"'{_key}' field is invalid => {_value}\n"
                raise ValueError(_err_str)

            self.config = Box(_v.document)
        except Exception as err:
            logger.exception(err)
            exit(2)


    def _freeze_config(self):
        """Freeze 'config' into immutable variable.
        """

        self.config = Box(self.config, frozen_box=True)
        logger.debug('\n' + pprint.pformat(self.config) + '\n')


    ### ATTRIBUTES ###
    ## config ##
    @property
    def config(self):
        try:
            return self.__config
        except AttributeError:
            return None

    @config.setter
    def config(self, config):
        try:
            if not isinstance(config, Box):
                raise TypeError(f"The 'config' attribute type <{type(config).__name__}> is invalid, must be a 'python-box' <class 'Box'>.")
        except Exception as err:
            logger.exception(err)
            exit(2)

        self.__config = config
    ## config ##


    ## configs_dir ##
    @property
    def configs_dir(self):
        try:
            return self.__configs_dir
        except AttributeError:
            return ConfigBase._CONFIGS_DIR

    @configs_dir.setter
    def configs_dir(self, configs_dir):
        try:
            if not isinstance(configs_dir, str):
                raise TypeError(f"The 'configs_dir' attribute type <{type(configs_dir).__name__}> is invalid, must be a <str>!")

            configs_dir = configs_dir.strip()
            if configs_dir == '':
                raise ValueError("The 'configs_dir' attribute value is empty!")
        except Exception as err:
            logger.exception(err)
            exit(2)

        self.__configs_dir = configs_dir
    ## configs_dir ##


    ## required_envs ##
    @property
    def required_envs(self):
        try:
            return self.__required_envs
        except AttributeError:
            return []

    @required_envs.setter
    def required_envs(self, required_envs):
        try:
            if not isinstance(required_envs, list):
                raise TypeError(f"The 'required_envs' attribute type <{type(required_envs).__name__}> is invalid, must be a <list>!")
        except TypeError as err:
            logger.exception(err)
            exit(2)

        self.__required_envs = required_envs
    ## required_envs ##


    ## valid_schema ##
    @property
    def valid_schema(self):
        try:
            return self.__valid_schema
        except AttributeError:
            return None

    @valid_schema.setter
    def valid_schema(self, valid_schema):
        try:
            if not isinstance(valid_schema, dict):
                raise TypeError(f"The 'valid_schema' attribute type <{type(valid_schema).__name__}> is invalid, must be a <dict>!")
        except TypeError as err:
            logger.exception(err)
            exit(2)

        self.__valid_schema = valid_schema
    ## valid_schema ##
    ### ATTRIBUTES ###
