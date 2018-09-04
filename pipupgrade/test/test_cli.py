# imports - compatibility imports
from pipupgrade._compat import StringIO

# imports - module imports
from pipupgrade import cli
from pipupgrade.util.test import mock_input

def test_confirm():
    query = "foobar"

    with mock_input(StringIO("Y")):
        assert cli.confirm(query) == True
    with mock_input(StringIO("y")):
        assert cli.confirm(query) == True
    with mock_input(StringIO("\n")):
        assert cli.confirm(query) == True

    with mock_input(StringIO("n")):
        assert cli.confirm(query) == False
    with mock_input(StringIO("1")):
        assert cli.confirm(query) == False

def test_format():
    string = "foobar"
    cli.format(string, cli.GREEN) == "{}{}{}".format(
        cli.GREEN,
        string,
        cli.CLEAR
    )

def test_echo(capfd):
    query    = "foobar"
    cli.echo(query, nl = False)
    out, err = capfd.readouterr()

    assert out == query

    cli.echo(query, nl = True)
    out, err = capfd.readouterr()
    assert out == "{}\n".format(query)