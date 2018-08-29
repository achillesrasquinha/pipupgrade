# imports - standard imports
import pip

PIP9 = int(pip.__version__.split(".")[0]) <= 10

if PIP9:
    from pip import get_installed_distributions
    from pip import main
else:
    from pip._internal.utils.misc import get_installed_distributions
    from pip._internal import main