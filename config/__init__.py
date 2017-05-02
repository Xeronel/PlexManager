from .config import DBConfig as __DBConfig
from .config import WebConfig as __WebConfig
from .config import LoggingConfig as __LoggingConfig
import os as __os
import yaml as __yaml


base = __os.path.dirname(__os.path.dirname(__file__))
file_name = __os.path.join(base, 'config.yaml')

with open(file_name, 'r') as f:
    __raw_config = __yaml.load(f)

db = __DBConfig(__raw_config.get('db', {}))
web = __WebConfig(__raw_config.get('web', {}))
logging = __LoggingConfig(__raw_config.get('logging', {}))
__all__ = ['db', 'web', 'logging']
