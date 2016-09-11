from .config import DBConfig as __DBConfig
from .config import WebConfig as __WebConfig
import os as __os
import yaml as __yaml


base = __os.path.dirname(__os.path.dirname(__file__))
file_name = __os.path.join(base, 'config.yaml')

with open(file_name, 'r') as f:
    __raw_config = __yaml.load(f)

db = __DBConfig(__raw_config['db'])
web = __WebConfig(__raw_config['web'])
__all__ = ['db', 'web']
