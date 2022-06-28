# -*- coding: utf-8 -*-

config_schema = {
    'env': { 'type': 'string', 'allowed': ['development', 'production'], 'default': 'development' },
    'app':
    {
        'type': 'dict',
        'schema':
        {
            'name': { 'type': 'string', 'minlength': 2, 'maxlength': 255 },
            'host': { 'type': 'string', 'minlength': 2, 'maxlength': 255 },
            'port': { 'type': 'integer', 'coerce': int, 'min': 1024, 'max': 65535 },
            'secret': { 'type': 'string', 'minlength': 12, 'maxlength': 255 },
            'debug': { 'type': 'boolean' },
            'logs_dir': { 'type': 'string'}
        }
    }
}
