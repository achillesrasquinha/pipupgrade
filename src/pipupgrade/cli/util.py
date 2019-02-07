# imports - compatibility imports
from __future__ import print_function
from pipupgrade._compat import input

# imports - standard imports
import inspect

_ACCEPTABLE_YES_INPUTS = ("", "y", "Y")

_ANSI_FORMAT = "\033[{}m"
_format_ansi = lambda x: _ANSI_FORMAT.format(x)

BOLD      = _format_ansi("0;1")
RED       = _format_ansi("0;91")
GREEN     = _format_ansi("0;92")
YELLOW    = _format_ansi("0;93")
CYAN      = _format_ansi("0;96")
CLEAR     = _format_ansi("0")

def confirm(query):
    query  = "{} [Y/n]: ".format(query)
    output = input(query)

    return output in _ACCEPTABLE_YES_INPUTS

def format(string, type_):
    string = "{}{}{}".format(type_, string, CLEAR)
    return string

def echo(string = "", nl = True):
    print(string, end = "\n" if nl else "")