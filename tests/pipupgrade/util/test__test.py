# imports - module imports
from pipupgrade._compat    import StringIO, input
from pipupgrade.util._test import mock_input

def test_mock_input(capfd):
    query = "foobar"
    
    with mock_input(StringIO("Y")):
        output    = input(query)
        assert output == "Y"

        output, _ = capfd.readouterr()
        assert output == query