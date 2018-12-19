# imports - standard imports
import argparse

# imports - module imports
from pipupgrade.__attr__ import (
    __version__,
    __description__
)
from pipupgrade.util import get_if_empty

def get_parser():
    parser = argparse.ArgumentParser(
        description = __description__,
        add_help    = False
    )
    parser.add_argument("-y", "--yes",
        action  = "store_true",
        help    = "Confirm for all dialogs"
    )
    parser.add_argument("-c", "--check",
        action  = "store_true",
        help    = "Check for outdated packages"
    )
    parser.add_argument("-l", "--latest",
        action  = "store_true",
        help    = "Update all packages to latest"
    )
    parser.add_argument("-r", "--requirements",
        action  = "append",
        help    = "Path to requirements.txt file"
    )
    parser.add_argument("--no-color",
        action  = "store_true",
        help    = "Avoid colored output"
    )
    parser.add_argument("-V", "--verbose",
        action  = "store_true",
        help    = "Display verbose output"
    )

    parser.add_argument("-v", "--version",
        action  = "version",
        version = __version__
    )
    parser.add_argument("-h", "--help",
        action  = "help",
        default = argparse.SUPPRESS,
        help    = "Show this help message and exit"
    )

    return parser

def get_args(args = None, known = True, as_dict = True):
    parser  = get_parser()
    args    = get_if_empty(args, None)

    if known:
        args, _ = parser.parse_known_args(args)
    else:
        args    = parser.parse_args(args)

    if as_dict:
        args = args.__dict__
        
    return args