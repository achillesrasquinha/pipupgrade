# imports - module imports
from    pipupgrade import cli

# imports - test imports
import  pytest
from    testutils import assert_input, assert_stdout

def test_confirm(capfd):
    query  = "foobar"
    stdout = "{} [Y/n/q]: ".format(query)

    def _assert_confirm(stdout):
        assert_input(capfd, query, "Y", expected = True,  input_ = cli.confirm, stdout = stdout)
        assert_input(capfd, query, "y", expected = True,  input_ = cli.confirm, stdout = stdout)
        assert_input(capfd, query,"\n", expected = True,  input_ = cli.confirm, stdout = stdout)
        assert_input(capfd, query, "n", expected = False, input_ = cli.confirm, stdout = stdout)
        assert_input(capfd, query, "1", expected = False, input_ = cli.confirm, stdout = stdout)

    _assert_confirm(stdout)

    stdout = "{} [Y/n]: ".format(query)

    with pytest.raises(SystemExit):
        assert_input(capfd, query, "q", expected = False, input_ = cli.confirm, stdout = stdout)
    
    with pytest.raises(SystemExit):
        assert_input(capfd, query, "Q", expected = False, input_ = cli.confirm, stdout = stdout)

    # assert_input(capfd, query, "Y", expected = True,  input_ = cli.confirm, stdout = stdout, input_args = { 'quit_': False })
    # assert_input(capfd, query, "y", expected = True,  input_ = cli.confirm, stdout = stdout, input_args = { 'quit_': False })
    # assert_input(capfd, query,"\n", expected = True,  input_ = cli.confirm, stdout = stdout, input_args = { 'quit_': False })
    # assert_input(capfd, query, "n", expected = False, input_ = cli.confirm, stdout = stdout, input_args = { 'quit_': False })
    # assert_input(capfd, query, "1", expected = False, input_ = cli.confirm, stdout = stdout, input_args = { 'quit_': False })

def test_format():
    string = "foobar"

    def _assert_format(string, type_):
        assert cli.format(string, type_) == "{}{}{}".format(type_, string, cli.CLEAR)

    _assert_format(string, cli.GREEN)
    _assert_format(string, cli.RED)
    _assert_format(string, cli.BOLD)

def test_echo(capfd, tmpdir):
    query  = "foobar"
    cli.echo(query, nl = False)
    assert_stdout(capfd, query)
    
    cli.echo(query, nl = True)
    assert_stdout(capfd, "{}\n".format(query))

    f = tmpdir.join("tmp")
    cli.echo(query, nl = True, file = str(f))
    assert f.read() == "foobar\n"