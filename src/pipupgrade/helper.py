# imports - standard imports
import os.path as osp

# imports - module imports
from pipupgrade       import _pip, log
from pipupgrade.model import Registry

logger = log.get_logger()

def get_registry_from_requirements(requirements, sync = False, verbose = False):
    if not verbose:
        logger.setLevel(log.NOTSET)

    path = osp.realpath(requirements)

    # if not osp.exists(path):
    #     cli.echo(cli_format("{} not found.".format(path), cli.RED))
    #     sys.exit(os.EX_NOINPUT)

    packages =  _pip.parse_requirements(requirements, session = "hack")
    registry = Registry(source = path, packages = packages, sync = sync)

    logger.info("Packages within requirements %s found: %s..." % (requirements, registry.packages))

    return registry