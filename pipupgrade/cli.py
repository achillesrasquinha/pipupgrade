# imports - compatibility imports
from __future__ import print_function
from pipupgrade._compat import input

# imports - standard imports
import inspect

# imports - module imports
from pipupgrade.commands.parser import get_parsed_args
from pipupgrade.util import get_if_empty, merge_dict

_ACCEPTABLE_YES = ("", "y", "Y")

BOLD      = "\033[0;1m"
UNDERLINE = "\033[0;4m"
RED       = "\033[0;31m"
GREEN     = "\033[0;32m"
YELLOW    = "\033[0;33m"
CYAN      = "\033[0;36m"
CLEAR     = "\033[0m"

def confirm(query):
    query  = "{} [Y/n]: ".format(query)
    output = input(query)

    return output in _ACCEPTABLE_YES

def format(string, type_):
    string = "{}{}{}".format(type_, string, CLEAR)
    return string

def echo(string, nl = True):
    print(string, end = "\n" if nl else "")

def command(fn):
    argspec = inspect.getargspec(fn)
    
    keys    = argspec.args
    values  = get_if_empty(argspec.defaults, [ ])

    fnargs  = dict(zip(keys, values))

    parsed  = get_parsed_args()
    
    merged  = merge_dict(fnargs, parsed.__dict__)

    def wrapper(*args, **kwargs):
        return fn(**merged)

    return wrapper