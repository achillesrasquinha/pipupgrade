# imports - standard imports
import os.path as osp

# imports - module imports
from pipupgrade.util.system import pardir
from pipupgrade.util._dict  import autodict

PATH         = autodict()
PATH["BASE"] = pardir(__file__)
PATH["DATA"] = osp.join(PATH["BASE"], "data")

class Configuration:
    def __init__(self):
        pass