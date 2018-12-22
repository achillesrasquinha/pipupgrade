# imports - module imports
from pipupgrade.util.string import strip_ansi, pluralize
from pipupgrade import cli

def test_strip_ansi():
    assert strip_ansi(cli.format("foobar", cli.GREEN)) == "foobar"
    assert strip_ansi(cli.format("barfoo", cli.BOLD))  == "barfoo"

def test_pluralize():
    assert pluralize("package",  1) == "package"
    assert pluralize("package",  2) == "packages"
    assert pluralize("packages", 2) == "packages"