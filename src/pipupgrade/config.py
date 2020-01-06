# imports - standard imports
import os.path      as osp
import configparser as cp

# imports - module imports
from pipupgrade             import __name__ as NAME
from pipupgrade.util.system import pardir, makedirs, touch
from pipupgrade.util._dict  import autodict
from pipupgrade._compat     import iteritems

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
        pass

    def _check_key(self, section, key):
        if not section in config:
            raise KeyError("No section %s found." % section)

        if not key in config[section]:
            raise KeyError("No key %s found." % key)

    def get(self, section, key, value):
        path    = osp.join(self.location, self.name)
        touch(path)

        self._check_key(section, key)
        
    def set(self, section, key, value):
        pass
        
class Settings:
    def __init__(self):
        self.config = Configuration()

        for k, v in iteritems(self.config["settings"]):
            print(k, v)

    def get(self, key):
        self.config.set("settings", key)

    def set(self, key, value):
        self.config.get("settings", key, value)