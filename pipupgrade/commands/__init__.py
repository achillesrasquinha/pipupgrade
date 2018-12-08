# imports - standard imports
import os.path as osp

from subprocess import call, list2cmdline

# imports - module imports
from pipupgrade.commands.outdated import command as pipupgrade_check, get_packages_info
from pipupgrade.commands.util     import cli_format
from pipupgrade.util       import get_if_empty
from pipupgrade.table      import Table
from pipupgrade.util.types import list_filter
from pipupgrade import _pip, request as req, cli, semver

def _get_pypi_info(name, raise_err = True):
    url  = "https://pypi.org/pypi/{}/json".format(name)
    res  = req.get(url)

    info = None

    if res.ok:
        data = res.json()
        info = data["info"]
    else:
        if raise_err:
            res.raise_for_status()

    return info

class PackageInfo:
    def __init__(self, package):
        if isinstance(package, _pip.InstallRequirement):
            self.name            = package.name
            self.current_version = package.installed_version

        _pypi_info = get_if_empty(_get_pypi_info(self.name, raise_err = False), { })

        self.latest_version = _pypi_info.get("version")
        self.home_page      = _pypi_info.get("home_page")

@cli.command
def command(yes = False, check = False, latest = False, requirements = [ ], no_color = True, verbose = False, user = False):
    cli.echo(cli_format("Checking...", cli.YELLOW))

    if requirements:
        # Discover requirements.txt
        for requirement in requirements:
            path = osp.abspath(requirement)
            
            if not osp.exists(path):
                cli.echo(cli_format("{} not found.".format(path), cli.RED))
            else:
                packages = _pip.parse_requirements(path, session = "hack")
                table    = Table(header = ["Name", "Current Version", "Latest Version", "Home Page"])

                for package in packages:
                    package = PackageInfo(package)
                    
                    if package.latest_version and package.current_version != package.latest_version:
                        diff_type = None

                        try:
                            diff_type = semver.difference(package.current_version, package.latest_version)
                            
                            if diff_type == "major":
                                
                        except ValueError:
                            pass

                        table.insert([
                            package.name,
                            package.current_version,
                            package.latest_version,
                            package.home_page
                        ])

                string   = table.render()

                cli.echo(string)
    else:
        pass

    # cli.echo(cli_format("Checking...", cli.YELLOW))

    # packages  = get_packages_info(raise_err = False)
    # npackages = len(packages)

    # query     = "Do you wish to upgrade {} packages?".format(npackages)

    # if yes or cli.confirm(query):
    #     for i, package in enumerate(packages):
    #         name = package.name


    #         info = cli_format("Updating {} of {} packages: {}".format(
    #             i + 1,
    #             npackages,
    #             cli_format(name, cli.GREEN)
    #         ), cli.BOLD)

    #         cli.echo(info)
            
    # packages  = get_packages_info(raise_err = True)
    # npackages =  
    
    # if check:
    #     pipupgrade_check()
    # else:
    #     cli.echo("Checking...")

    #     packages  = get_packages_info(raise_err = False)
    #     npackages = len(packages)

    #     query     = "Do you wish to update {} packages?".format(npackages)

    #     if yes or 


    
    # if check:
    #     pipupgrade_check()
    # else:
    #     cli.echo("Checking...")
        
    #     packages  = get_packages_info(raise_err = False)
    #     npackages = len(packages)

    #     query     = "Do you wish to update {} packages?".format(npackages)
        
    #     if yes or cli.confirm(query):
    #         for i, package in enumerate(packages):
    #             name   = package.project_name

    #             info   = cli_format("Updating {} of {} packages: {}".format(
    #                 i + 1,
    #                 npackages,
    #                 cli_format(name, cli.GREEN)
    #             ), cli.BOLD)

    #             cli.echo(info)

    #             params  = list_filter([
    #                 "pip",
    #                 "install",
    #                 "--quiet" if not verbose else None,
    #                 "--no-cache",
    #                 "--upgrade",
    #                 name
    #             ], filter_ = bool)
    #             command = list2cmdline(params)

    #             call(command, shell = True)

    #         cli.echo(cli_format("UPGRADED ALL THE PACKAGES!", cli.BOLD))
