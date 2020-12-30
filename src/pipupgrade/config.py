# imports - compatibility imports
from __future__ import absolute_import

# imports - standard imports
import os.path as osp
import multiprocessing as mp
from threading import Lock
import platform
import json

# imports - module imports
from pipupgrade              import __name__ as NAME, __version__, _pip
from pipupgrade.util.system  import pardir, makedirs, touch
from pipupgrade.util.environ import getenv
from pipupgrade.util.types   import auto_typecast
from pipupgrade.util._dict   import autodict
from pipupgrade._compat      import iteritems, configparser as cp

PATH            = autodict()
PATH["BASE"]    = pardir(__file__)
PATH["DATA"]    = osp.join(PATH["BASE"], "data")
PATH["CACHE"]   = osp.join(osp.expanduser("~"), ".config", NAME)

class Configuration(object):
    # BUGFIX: #63 Always complains about invalid config.ini - https://github.com/achillesrasquinha/pipupgrade/issues/63
    #         Use threading.Lock() around disk IO
    locks = { "readwrite": Lock() }

    def __init__(self, location = PATH["CACHE"], name = "config"):
        config = getenv("CONFIG")

        if not config:
            self.name     = "%s.ini" % name
            self.location = location
            makedirs(self.location, exist_ok = True)
        else:
            self.name     = osp.basename(config)
            self.location = osp.dirname(config)
            
        self.config   = self.read()

    @classmethod
    def __del__(self):
        # Clean up leaked semaphores Lock() before thread exit
        # This function gets called atexit once per SpawnPoolWorker-1 thread
        for key in list(self.locks.keys()):
            self.locks[key].acquire()
            self.locks[key].release()
            del self.locks[key]

    def read(self):
        with self.locks['readwrite']:
            path        = osp.join(self.location, self.name)
            self.config = cp.ConfigParser()
            if osp.exists(path):
                self.config.read(path)
        return self.config

    def write(self):
        with self.locks['readwrite']:
            path = osp.join(self.location, self.name)
            with open(path, "w") as f:
                self.config.write(f)


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

        if force or not config.has_option(section, key):
            config.set(section, key, value)
            self.write()

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

    # NOTE: Doesn't comply with "--pip-path" flag.
    # environ["pip_executables"]  = [dict(
    #     executable = executable,
    #     version    = _pip.call("--version", pip_exec = executable,
    #         output = True)[1]
    # ) for executable in _pip._PIP_EXECUTABLES]

    from pipupgrade import settings
    environ["settings"]         = settings.to_dict()

    return environ