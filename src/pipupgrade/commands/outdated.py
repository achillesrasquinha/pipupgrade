# imports - compatibility imports
from pipupgrade._compat import cmp

# imports - module imports
from pipupgrade.commands.util import cli_format
from pipupgrade._pip  import get_installed_distributions
from pipupgrade.table import Table
from pipupgrade       import request as req, cli, semver

def _get_pypi_package_info(package, raise_err = False):
    url      = "https://pypi.org/pypi/{}/json".format(package)
    response = req.get(url)

    info     = None

    if response.ok:
        json = response.json()
        info = json["info"]
    else:
        if raise_err:
            response.raise_for_status()

    return info

def _cli_format_semver(version, type_):
    def format_yellow(string):
        string = cli_format(string, cli.YELLOW)
        return string

    semver.parse(version)

    if type_ == "major":
        version    = format_yellow(version)
    if type_ == "minor":
        index      = version.find(".", 1) + 1
        head, tail = version[:index], version[index:]
        version    = "".join([head, format_yellow(tail)])
    if type_ == "patch":
        index      = version.find(".", 2) + 1
        head, tail = version[:index], version[index:]
        version    = "".join([head, format_yellow(tail)])

    return version

def get_packages_info(raise_err = True):
    packages = get_installed_distributions()
    info     = [ ]

    for package in packages:
        package_info    = _get_pypi_package_info(package.project_name, raise_err = raise_err) or { }

        project_name    = package.project_name

        version_current = package.version
        version_latest  = package_info.get("version")
        
        diff_type       = None

        if version_latest and version_current != version_latest:
            try:
                diff_type = semver.difference(version_current, version_latest)
            except ValueError:
                if raise_err:
                    raise

        info.append(dict(
            name             = package_info.get("name"),
            project_name     = project_name,
            version          = version_current,
            latest_version   = version_latest,
            semver_diff_type = diff_type,
            home_page        = package_info.get("home_page")
        ))

    return info
    
@cli.command
def command():
    cli.echo("Checking...")

    packages = get_packages_info(raise_err = False)
    # if diff_type == "major":
    #                 project_name = cli_format(project_name, cli.RED)
    #             if diff_type == "minor":
    #                 project_name = cli_format(project_name, cli.YELLOW)
    #             if diff_type == "patch":
    #                 project_name = cli_format(project_name, cli.GREEN)
                
    #             version_latest = _cli_format_semver(version_latest, type_ = diff_type)

    table    = Table(header = ["Package", "Current", "Latest", "Home Page"])
    for package in packages:
        table.insert([
            package.name,
            package.current_version,
            package.latest_version,
            package.home_page
        ])

    string = cli_format("All packages are upto date.", cli.GREEN) if table.empty else table.render()
    cli.echo(string)