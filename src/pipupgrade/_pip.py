# imports - compatibility imports
from pipupgrade._compat import iteritems

# imports - standard imports
from subprocess import call, list2cmdline
import pip

# imports - module imports
from pipupgrade.util.types   import list_filter
from pipupgrade.util.string  import kebab_case
from pipupgrade.util.environ import value_to_envval

PIP9 = int(pip.__version__.split(".")[0]) < 10

if PIP9:
    from pip                 import get_installed_distributions
    from pip.req             import parse_requirements
    from pip.req.req_install import InstallRequirement
else:
    from pip._internal.utils.misc      import get_installed_distributions
    from pip._internal.req             import parse_requirements
    from pip._internal.req.req_install import InstallRequirement

from pip._vendor.pkg_resources import (
    Distribution,
    DistInfoDistribution,
    EggInfoDistribution
)

def install(*packages, **options):
    params  = ["pip", "install"]

    for flag, value in iteritems(options):
        if value != False:
            flag  = "--%s" % kebab_case(flag, delimiter = "_")
            params.append(flag)

            if not isinstance(value, bool):
                value = value_to_envval(value)
                params.append(value)

    params.append(packages)

    command = list2cmdline(params)

    call(command, shell = True)