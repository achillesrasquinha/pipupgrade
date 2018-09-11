# imports - module imports
from pipupgrade.util.string import strip_ansi
from pipupgrade import cli

def test_strip_ansi():
    assert strip_ansi(cli.format("foobar", cli.GREEN)) == "foobar"
    assert strip_ansi(cli.format("barfoo", cli.BOLD))  == "barfoo"