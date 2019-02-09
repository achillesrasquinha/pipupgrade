# imports - compatibility imports
from pipupgrade._compat import iteritems

# imports - standard imports
import pip
import json

# imports - module imports
from pipupgrade.util.system  import which, popen
from pipupgrade.util.string  import kebab_case
from pipupgrade.util.environ import value_to_envval

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

def _get_pip_executable():
    execs = ("pip", "pip3", "pip2")
    exec_ = None

    for exec_ in execs:
        exec_ = which(exec_)
        if exec_:
            return exec_

    if not exec_:
        raise ValueError("pip executable not found.")

    return exec_

_PIP_EXECUTABLE = _get_pip_executable()

def call(*args, **kwargs):
    pip_exec = kwargs.pop("pip_exec", _PIP_EXECUTABLE)

    params   = [pip_exec, *args]
    
    for flag, value in iteritems(kwargs):
        if value != False:
            flag  = "--%s" % kebab_case(flag, delimiter = "_")
            params.append(flag)

            if not isinstance(value, bool):
                value = value_to_envval(value)
                params.append(value)

    return popen(*params, output = True)