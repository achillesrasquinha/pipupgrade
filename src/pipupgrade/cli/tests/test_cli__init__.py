# imports - compatibility imports
from pipupgrade._compat import StringIO, iteritems, iterkeys

# imports - module imports
from pipupgrade import cli
from pipupgrade.cli import get_args
from pipupgrade.util.types import merge_dict
from pipupgrade.util._test import mock_input, assert_input, assert_stdout

def test_confirm(capfd):
    query  = "foobar"
    stdout = "{} [Y/n]: ".format(query)

    assert_input(capfd, query, "Y", expected = True,  input_ = cli.confirm, stdout = stdout)
    assert_input(capfd, query, "y", expected = True,  input_ = cli.confirm, stdout = stdout)
    assert_input(capfd, query,"\n", expected = True,  input_ = cli.confirm, stdout = stdout)
    assert_input(capfd, query, "n", expected = False, input_ = cli.confirm, stdout = stdout)
    assert_input(capfd, query, "1", expected = False, input_ = cli.confirm, stdout = stdout)

def test_format():
    string = "foobar"

    def _assert_format(string, type_):
        assert cli.format(string, type_) == "{}{}{}".format(type_, string, cli.CLEAR)

    _assert_format(string, cli.GREEN)
    _assert_format(string, cli.RED)
    _assert_format(string, cli.BOLD)

def test_echo(capfd):
    query  = "foobar"
    cli.echo(query, nl = False)
    assert_stdout(capfd, query)
    
    cli.echo(query, nl = True)
    assert_stdout(capfd, "{}\n".format(query))

def test_command():
    def _assert_command(values, override = dict(), initial = dict()):
        @cli.command
        def foobar(*args, **kwargs):
            args    = get_args()
            params  = merge_dict(args, override)
            
            for k, v in iteritems(values):
                assert params[k] == v

            if initial:
                for k in iterkeys(initial):
                    assert initial[k] == args[k]
        
        foobar()
    
    _assert_command(dict(yes    = False))
    _assert_command(dict(latest = True), dict(latest = True), dict(latest = False))