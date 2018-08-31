# imports - module imports
from pipupgrade._pip  import get_installed_distributions
from pipupgrade       import request as req, cli
from pipupgrade.table import Table
from pipupgrade.util  import get_if_empty

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

def command():
    code         = 0
    
    packages     = get_installed_distributions()
    table        = Table()
    table.header = ["Name", "Current Version", "Latest Version", "Home Page"]

    cli.echo("Checking...")
    for package in packages:
        package_info = get_if_empty(
            _get_pypi_package_info(package.project_name, raise_err = False), { }
        )

        table.insert([
            package.version,
            package_info.get("version",   None),
            package_info.get("home_page", None)
        ])

    string = table.render()
    cli.echo(string)

    return code