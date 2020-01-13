from pipupgrade.model.package import (
    _get_pypi_info,
    _get_package_version,
    _get_pip_info
)
from pipupgrade.__attr__ import (
    __name__    as NAME,
    __author__
)
from pipupgrade import semver

def test___get_pypi_info():
    info = _get_pypi_info("pipupgrade")
    assert info["author"] == "Achilles Rasquinha"

def test__get_package_version():
    version = _get_package_version("pipupgrade")
    semver.parse(version)

def test__get_pip_info():
    packages = _get_pip_info("pipupgrade", "pytest")

    assert packages["pipupgrade"]["name"]      == NAME
    assert packages["pipupgrade"]["author"]    == __author__

    assert packages["pytest"]["name"]          == "pytest"
    assert packages["pytest"]["license"]       == "MIT license"