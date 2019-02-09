# imports - standard imports
import subprocess

# imports - test imports
import pytest

# imports - module imports
from pipupgrade import _pip

def test_imports():
    from pipupgrade._pip import (
        # get_installed_distributions as _,
        DistInfoDistribution        as _
    )

def test_call(tmpdir):
    directory = tmpdir.mkdir("tmp")
    tempfile  = directory.join("tmp.log")
    path      = str(tempfile)

    _pip.call("install", "requests")
    _pip.call("install", "requests", quiet = True)
    _pip.call("install", "requests", log   = path)

    _pip.call("list")