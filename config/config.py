import logging


class BaseConfig:
    def __init__(self, defaults, section):
        self._set_attribs(defaults)
        self._set_attribs(section)

    def _set_attribs(self, data):
        for key in data:
            setattr(self, key, data[key])


class WebConfig(BaseConfig):
    def __init__(self, section):
        defaults = {'debug': False,
                    'autoreload': False,
                    'compiled_template_cache': True,
                    'host_port': 9999,
                    'static_path': 'web/static',
                    'template_path': 'web/templates',
                    'cookie_secret': {0: '__SECRET__'},
                    'key_version': 0}
        super(WebConfig, self).__init__(defaults, section)

        for key in defaults:
            setattr(self, key, defaults[key])

        for key in section:
            setattr(self, key, section[key])

        # Make sure cookie_secret is stored as a dictionary
        if type(self.cookie_secret) == str:
            self.cookie_secret = {0: self.cookie_secret}
            self.key_version = 0

        if self.key_version not in self.cookie_secret:
            raise ValueError('Invalid key version')


class DBConfig(BaseConfig):
    def __init__(self, section):
        defaults = {}
        super(DBConfig, self).__init__(defaults, section)

        
class LoggingConfig(BaseConfig):
    def __init__(self, section):
        defaults = {'journald': True,
                    'stdout': False,
                    'level': 'INFO'}
        super(LoggingConfig, self).__init__(defaults, section)

        # Convert log level to a value
        self.level = str(self.level).upper()
        new_level = logging.getLevelName(self.level)  # Returns int if level not defined
        if type(new_level) == str:
            new_level = 'NOTSET'
        self.level = new_level
