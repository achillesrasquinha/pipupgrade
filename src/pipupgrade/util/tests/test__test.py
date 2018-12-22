# imports - module imports
from pipupgrade._compat    import StringIO, input
from pipupgrade.util._test import mock_input, assert_input

def test_mock_input(capfd):
    query = "foobar"

    assert_input(capfd, query, "Y")
    assert_input(capfd, query, "Y", input_ = input)