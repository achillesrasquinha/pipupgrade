# imports - compatibility imports
from __future__ import absolute_import

# imports - standard imports
import subprocess

# imports - test imports
import pytest

# imports - module imports
from pipupgrade         import _pip

def test_imports():
    from pipupgrade._pip import (
        parse_requirements          as _,
        InstallRequirement          as _,
        # get_installed_distributions as _,
        Distribution                as _,
        DistInfoDistribution        as _,
        EggInfoDistribution         as _
    )

def test_call(tmpdir):
    def assert_pip_call(response, code = 0, output = True, err = False):
        rcode, rout, rerr = response
        assert rcode == code

        def _assert_outerr(routerr, outerr):
            if isinstance(output, bool):
                if output:
                    assert rout
                else:
                    assert not rout
            else:
                assert rout == output

        _assert_outerr(rout, output)
        _assert_outerr(rerr, err)

    directory = tmpdir.mkdir("tmp")
    tempfile  = directory.join("tmp.log")
    path      = str(tempfile)

    _pip.call("install", "pipupgrade")
    assert_pip_call(_pip.call("install", "pipupgrade", quiet = True))
    
    _pip.call("install", "pipupgrade", log = path)
    assert tempfile.read()

    # assert_pip_call(_pip.call("list", output = True))