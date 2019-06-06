# imports - standard imports
import os.path as osp
import json

# imports - module imports
from pipupgrade             import _pip, log
from pipupgrade.model       import Registry
from pipupgrade.util.system import which, popen

logger = log.get_logger()

def get_registry_from_requirements(requirements, sync = False, verbose = False):
    if not verbose:
        logger.setLevel(log.NOTSET)

    path = osp.realpath(requirements)

    # if not osp.exists(path):
    #     cli.echo(cli_format("{} not found.".format(path), cli.RED))
    #     sys.exit(os.EX_NOINPUT)

    packages =  _pip.parse_requirements(requirements, session = "hack")
    registry = Registry(source = path, packages = packages, sync = sync,
        verbose = verbose)

    logger.info("Packages within requirements %s found: %s..." % (requirements, registry.packages))

    return registry

def get_registry_from_pip(pip_path, sync = False, verbose = False):
    if not verbose:
        logger.setLevel(log.NOTSET)

    _, output, _ = _pip.call("list", outdated = True, \
        format = "json", pip_exec = pip_path)
    packages     = json.loads(output)
    registry     = Registry(source = pip_path, packages = packages,
        installed = True, sync = sync, verbose = verbose)

    logger.info("Packages within `pip` %s found: %s..." % (pip_path, registry.packages))
    # _pip.get_installed_distributions() # https://github.com/achillesrasquinha/pipupgrade/issues/13

    return registry

def update_pipfile(pipfile, verbose = False):
    if not verbose:
        logger.setLevel(log.NOTSET)

    realpath = osp.realpath(pipfile)
    basepath = osp.dirname(realpath)

    logger.info("Searching for `pipenv`...")
    pipenv   = which("pipenv", raise_err = True)
    logger.info("`pipenv` found.")

    code     = popen("%s update" % pipenv, quiet = not verbose, cwd = basepath)

    return code == 0