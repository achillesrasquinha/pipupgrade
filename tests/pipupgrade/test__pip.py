# imports - standard imports
import subprocess

# imports - test imports
import pytest

# imports - module imports
from pipupgrade import _pip

def test_imports():
    from pipupgrade._pip import (
        get_installed_distributions as _,
        DistInfoDistribution        as _
    )

def test_install(tmpdir):
    directory = tmpdir.mkdir("tmp")
    tempfile  = directory.join("tmp.log")
    path      = str(tempfile)

    _pip.install("foobar")
    _pip.install("foobar", quiet = True)
    _pip.install("foobar", log = path)