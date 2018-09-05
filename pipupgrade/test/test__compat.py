# imports - standard imports
from pipupgrade._compat    import cmp, input, StringIO
from pipupgrade.util._test import mock_input

def test_imports():
    from pipupgrade._compat import (
        builtins    as _,
        StringIO    as _,

        urlopen     as _,
        HTTPError   as _,
        
        zip_longest as _
    )

def test_input(capfd):
    query = "foobar"

    with mock_input(StringIO("Y")):
        assert input(query) == "Y"

        output, _ = capfd.readouterr()
        assert output == query

def test_cmp():
    assert cmp(1, 2) == -1
    assert cmp(1, 1) ==  0
    assert cmp(2, 1) ==  1