# imports - compatibility imports
from pipupgrade._compat import builtins

# imports - test imports
import mock

# imports - module imports
from pipupgrade import cli

def test_confirm():
    query = "foobar"

    with mock.patch.object(builtins, "input", lambda _: "Y"):
        assert cli.confirm(query) == True
    with mock.patch.object(builtins, "input", lambda _: "y"):
        assert cli.confirm(query) == True
    with mock.patch.object(builtins, "input", lambda _: "" ):
        assert cli.confirm(query) == True

    with mock.patch.object(builtins, "input", lambda _: "n"):
        assert cli.confirm(query) == False
    with mock.patch.object(builtins, "input", lambda _: 1  ):
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