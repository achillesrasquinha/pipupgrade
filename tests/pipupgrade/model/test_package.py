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
from pipupgrade._pip import InstallRequirement
from pipupgrade.model.package import Package

import sys
from pip._vendor.packaging.specifiers import SpecifierSet
if sys.version_info >= (3, 3):
    from unittest.mock import MagicMock, PropertyMock, patch
else:
    from mock import MagicMock, PropertyMock, patch

import pytest

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
    # Breaks on multiple Python Versions
    # assert packages["pytest"]["license"]       == "MIT"

@pytest.mark.parametrize(
    ["requirement", "installed_version", "current_version"],
    [
        ("==1.0.0", "5.0.0", "1.0.0"), # Pinned requirement
        ("", "1.0.0", "1.0.0"), # Installed version
        ("~=1.0", "2.0.0", "2.0.0"), # Installed version
        ("~=1.0", None, "~=1.0") # Requirement
    ]
)
def test_install_requirement_current_version(
    requirement, installed_version, current_version
):
    specifiers = SpecifierSet(requirement)
    with patch.multiple(
        InstallRequirement,
        specifier=PropertyMock(return_value=specifiers),
        installed_version=PropertyMock(return_value=installed_version),
        # Isolate test to version only, and prevent error with pip~=9.0
        __str__=MagicMock(return_value="mypackage")
    ):
        requirement = InstallRequirement(req=None, comes_from="")
        package = Package(requirement)

    assert package.current_version == current_version
