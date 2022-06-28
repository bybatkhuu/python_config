# -*- coding: utf-8 -*-

try:
    from onion_config.config_base import ConfigBase
    from onion_config.__version__ import __version__
except ImportError:
    from .config_base import ConfigBase
    from .__version__ import __version__
