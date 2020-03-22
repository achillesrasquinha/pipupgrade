# imports - compatibility imports
from __future__ import absolute_import

# imports - standard imports
import os.path as osp
import multiprocessing as mp
import platform
import json

# imports - module imports
from pipupgrade             import __name__ as NAME, __version__, _pip
from pipupgrade.util.system import pardir, makedirs, touch
from pipupgrade.util.types  import auto_typecast
from pipupgrade.util._dict  import autodict
from pipupgrade._compat     import iteritems, configparser as cp

PATH            = autodict()
PATH["BASE"]    = pardir(__file__)
PATH["DATA"]    = osp.join(PATH["BASE"], "data")
PATH["CACHE"]   = osp.join(osp.expanduser("~"), ".%s" % NAME)

class Configuration(object):
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

        if not config.has_section(section):
            raise KeyError("No section %s found." % section)

        if not config.has_option(section, key):
            raise KeyError("No key %s found." % key)
        
        value = auto_typecast(config.get(section, key))

        return value
        
    def set(self, section, key, value, force = False):
        config = self.config
        value  = str(value)

        if not config.has_section(section):
            config.add_section(section)
            config.set(section, key, value)
        else:
            if not config.has_option(section, key):
                config.set(section, key, value)
            else:
                if force:
                    config.set(section, key, value)

        path = osp.join(self.location, self.name)
        with open(path, "w") as f:
            config.write(f)
        
class Settings(object):
    _DEFAULTS = {
              "version": __version__,
        "cache_timeout": 60 * 60 * 24, # 1 day
                 "jobs": mp.cpu_count() 
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

    def to_dict(self):
        parser      = self.config.config
        sections    = parser._sections

        sections    = json.loads(json.dumps(sections))

        return sections 

def environment():
    environ = dict()
    
    environ["version"]          = __version__
    environ["python_version"]   = platform.python_version()
    environ["os"]               = platform.platform()
    environ["config"]           = dict(
        path = dict(PATH)
    )
    environ["pip_executables"]  = [dict(
        executable = executable,
        version    = _pip.call("--version", pip_exec = executable,
            output = True)[1]
    ) for executable in _pip._PIP_EXECUTABLES]

    from pipupgrade import settings
    environ["settings"]         = settings.to_dict()

    return environ