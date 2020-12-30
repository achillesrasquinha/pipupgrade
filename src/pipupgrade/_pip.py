# imports - compatibility imports
from pipupgrade._compat import iteritems

# imports - standard imports
import pip
import json
import os.path as osp

# imports - module imports
from pipupgrade.util.system  import which, popen
from pipupgrade.util.string  import kebab_case
from pipupgrade.util.environ import value_to_envval
from pipupgrade.util.array   import sequencify
from pipupgrade.log          import get_logger

logger = get_logger()

PIP9 = int(pip.__version__.split(".")[0]) < 10

if PIP9:
    # from pip                 import get_installed_distributions
    from pip.req             import parse_requirements
    from pip.req.req_install import InstallRequirement
else:
    # from pip._internal.utils.misc      import get_installed_distributions
    from pip._internal.req             import parse_requirements
    from pip._internal.req.req_install import InstallRequirement

from pip._vendor.pkg_resources import (
    Distribution,
    DistInfoDistribution,
    EggInfoDistribution
)

def _get_pip_executable(multiple = False):
    pips  = ("pip", "pip3", "pip2")
    execs = [ ]

    for pip_ in pips:
        exec_ = which(pip_)
        if exec_:
            if not multiple:
                return exec_
            else:
                if exec_ not in execs and not osp.islink(exec_):
                    execs.append(exec_)

    if not execs:
        raise ValueError("pip executable not found.")

    return execs

_PIP_EXECUTABLE  = _get_pip_executable()
_PIP_EXECUTABLES = _get_pip_executable(multiple = True)

def call(*args, **kwargs):
    pip_exec  = kwargs.pop("pip_exec", None)  or _PIP_EXECUTABLE
    quiet     = kwargs.pop("quiet", None)     or False
    output    = kwargs.pop("output", None)    or False
    raise_err = kwargs.pop("raise_err", None) or True

    params    = sequencify(pip_exec) + sequencify(args)
    
    for flag, value in iteritems(kwargs):
        if value != False:
            flag  = "--%s" % kebab_case(flag, delimiter = "_")
            params.append(flag)

            if not isinstance(value, bool):
                value = value_to_envval(value)
                params.append(value)

    output = output or quiet
	
    output = popen(*params, output = output, raise_err = raise_err)
    
    return output