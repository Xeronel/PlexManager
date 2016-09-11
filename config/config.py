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
