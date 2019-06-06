# imports - standard imports
import os.path as osp

# imports - module imports
from pipupgrade.util.system import pardir
from pipupgrade.util.types  import autodict

PATH         = autodict()
PATH["BASE"] = pardir(__file__)
PATH["DATA"] = osp.join(PATH["BASE"], "data")