# imports - module imports
from pipupgrade._pip import get_installed_distributions
from pipupgrade      import request as req
from pipupgrade.util import get_if_empty

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
    packages = get_installed_distributions()
    results  = [ ]

    for package in packages:
        result = dict()
        result["current_version"] = package.version
        package_info              = get_if_empty(
            _get_pypi_package_info(package.project_name, raise_err = False), { }
        )
    
        result["latest_version"]  = package_info.get("version",   None)
        result["url"]             = package_info.get("home_page", None)

    return results