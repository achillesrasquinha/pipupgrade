# imports - compatibility imports
from __future__ import print_function
from pipupgrade._compat import input

# imports - standard imports
import sys, os
import inspect

_ACCEPTABLE_INPUTS_YES  = ("", "y", "Y")
_ACCEPTABLE_INPUTS_QUIT = ("q", "Q")

_ANSI_FORMAT = "\033[{}m"
_format_ansi = lambda x: _ANSI_FORMAT.format(x)

BOLD      = _format_ansi("0;1")
RED       = _format_ansi("0;91")
GREEN     = _format_ansi("0;92")
YELLOW    = _format_ansi("0;93")
CYAN      = _format_ansi("0;96")
CLEAR     = _format_ansi("0")

def confirm(query, quit_ = True):
    choices = "[Y/n%s]" % "/q" if quit_ else ""
    query   = "%s %s: " % (query, choices)

    output  = input(query)

    if output in _ACCEPTABLE_INPUTS_QUIT:
        sys.exit(os.EX_OK)
    
    return output in _ACCEPTABLE_INPUTS_YES

def format(string, type_):
    string = "{}{}{}".format(type_, string, CLEAR)
    return string

def echo(string = "", nl = True):
    print(string, end = "\n" if nl else "")