# imports - standard imports
import os.path      as osp

# imports - module imports
from pipupgrade             import __name__ as NAME, __version__
from pipupgrade.util.system import pardir, makedirs, touch
from pipupgrade.util.types  import auto_typecast
from pipupgrade.util._dict  import autodict
from pipupgrade._compat     import iteritems, configparser as cp, string_types

PATH            = autodict()
PATH["BASE"]    = pardir(__file__)
PATH["DATA"]    = osp.join(PATH["BASE"], "data")
PATH["CACHE"]   = osp.join(osp.expanduser("~"), ".%s" % NAME)

class Configuration:
    def __init__(self, location = PATH["CACHE"], name = "config"):
        self.location   = location
        makedirs(self.location, exist_ok = True)
        
        self.name       = "%s.ini" % name
        
    @property
    def config(self):
        path    = osp.join(self.location, self.name)
        config  = cp.ConfigParser()
        
        if osp.exists(path):
            config.read(path)

        return config

    def get(self, section, key):
        config = self.config

        if not section in config:
            raise KeyError("No section %s found." % section)

        if not key in config[section]:
            raise KeyError("No key %s found." % key)
        
        value = auto_typecast(config[section][key])

        return value
        
    def set(self, section, key, value, force = False):
        config = self.config
        value  = string_types(value)

        if not section in config:
            config[section] = dict({ key: value })
        else:
            if not key in config[section]:
                config[section][key] = value
            else:
                if force:
                    config[section][key] = value

        path = osp.join(self.location, self.name)
        with open(path, "w") as f:
            config.write(f)
        
class Settings:
    _DEFAULTS = {
              "version": __version__,
        "cache_timeout": 60 * 60 * 24 # 1 day
    }

    def __init__(self):
        self.config = Configuration()

        self._init()

    def _init(self):
        for k, v in iteritems(Settings._DEFAULTS):
            self.set(k, v)

    def get(self, key):
        return self.config.get("settings", key)

    def set(self, key, value):
        self.config.set("settings", key, value)