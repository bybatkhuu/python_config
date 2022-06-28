# Python Config (onion_config)

Python-box based custom config package (onion_config) for python projects.

## Features

* Load environment variables - [https://pypi.org/project/python-dotenv](https://pypi.org/project/python-dotenv)
* Python-box based config - [https://pypi.org/project/python-box](https://pypi.org/project/python-box)
* Cerberus schema validation - [https://pypi.org/project/Cerberus](https://pypi.org/project/Cerberus)
* Custom base config module
* YAML or JSON based configs
* Update with extra configs
* Pre-load config
* Validate config
* Freeze config
* Config as dictioary

---

## Installation

### 1. Prerequisites

* **Python (>= v3.7)**
* **PyPi (>= v21)**

### 2. Install onion-config

#### A. [RECOMMENDED] PyPi install

```sh
# Install or upgrade onion-config package:
pip install --upgrade onion-config

# To uninstall package:
pip uninstall -y onion-config
```

#### B. Manually add to PYTHONPATH (Recommended for development)

```sh
# Clone repository by git:
git clone https://github.com/bybatkhuu/python_config.git onion_config
cd onion_config

# Install python dependencies:
pip install --upgrade pip
cat requirements.txt | xargs -n 1 -L 1 pip install --no-cache-dir

# Add current path to PYTHONPATH:
export PYTHONPATH="${PWD}:${PYTHONPATH}"
```

#### C. Manually compile and setup (Not recommended)

```sh
# Clone repository by git:
git clone https://github.com/bybatkhuu/python_config.git onion_config
cd onion_config

# Building python package:
pip install --upgrade pip setuptools wheel
python setup.py build
# Install python dependencies with built package to current python environment:
python setup.py install --record installed_files.txt

# To remove only installed onion-config package:
head -n 1 installed_files.txt | xargs rm -vrf
# Or to remove all installed files and packages:
cat installed_files.txt | xargs rm -vrf
```

## Usage/Examples

### Simple example

**configs/config.yml**:

```yaml
hostname: "localhost"
username: "admin"
password: "secret"
```

**sample.py**:

```python
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
```

### Advanced example

**configs/app.yml**:

```yaml
env: development

app:
    name: "My App"
    host: 0.0.0.0
    port: 80
    secret: "my-secret"
    debug: false
```

**configs/config.json**:

```json
{
    "app":
    {
        "logs_dir": "/var/log/app"
    },
    "opt":
    {
        "val": "optional value",
        "integer": 123
    }
}
```

**.env**:

```sh
ENV=production

APP_PORT=8080
APP_SECRET="My_s3crEt_k3y"

PY_EXTRA_CONFIGS_DIR="./extra_configs"
```

**extra_configs/app.yml**:

```yaml
app:
    name: "My App - Extra"
    description: "Extra description"
```

**utils/validator_schemas.py**:

```python
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
```

**config.py**:

```python
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
```

**app.py**:

```python
from pprint import pprint
from flask import Flask
from config import config


print("LOADED CONFIG:")
pprint(config.to_dict())
print()


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(host=config.app.host, port=config.app.port)
```

---

## Running Tests

To run tests, run the following command:

```sh
pytest
```

## Environment Variables

You can use the following environment variables inside **.env** file:

```bash
PY_EXTRA_CONFIGS_DIR="./extra_configs"
```

---

## References

* [https://saurabh-kumar.com/python-dotenv](https://saurabh-kumar.com/python-dotenv)
* [https://github.com/theskumar/python-dotenv](https://github.com/theskumar/python-dotenv)
* [https://github.com/cdgriffith/Box/wiki](https://github.com/cdgriffith/Box/wiki)
* [https://github.com/cdgriffith/Box](https://github.com/cdgriffith/Box)
* [https://docs.python-cerberus.org/en/stable](https://docs.python-cerberus.org/en/stable)
* [https://github.com/pyeve/cerberus](https://github.com/pyeve/cerberus)
