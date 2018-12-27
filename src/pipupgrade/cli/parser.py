# imports - standard imports
import argparse

# imports - module imports
from pipupgrade.__attr__ import (
    __name__,
    __version__,
    __description__,
    __command__
)

def get_parser():
    parser = argparse.ArgumentParser(
        prog        = __command__,
        description = __description__,
        add_help    = False
    )
    parser.add_argument("-y", "--yes",
        action  = "store_true",
        help    = "Confirm for all dialogs."
    )
    parser.add_argument("-c", "--check",
        action  = "store_true",
        help    = "Check for outdated packages."
    )
    parser.add_argument("-l", "--latest",
        action  = "store_true",
        help    = "Update all packages to latest."
    )
    parser.add_argument("-s", "--self",
        action  = "store_true",
        help    = "Update %s." % __name__
    )
    parser.add_argument("-r", "--requirements",
        action  = "append",
        help    = "Path to requirements.txt file."
    )
    parser.add_argument("-u", "--user",
        action  = "store_true",
        help    = "Install to the Python user install directory for environment \
                    variables and user configuration."
    )
    parser.add_argument("--no-color",
        action  = "store_true",
        help    = "Avoid colored output."
    )
    parser.add_argument("-V", "--verbose",
        action  = "store_true",
        help    = "Display verbose output."
    )

    parser.add_argument("-v", "--version",
        action  = "version",
        version = __version__,
        help    = "Show %s's version number and exit." % __name__
    )
    parser.add_argument("-h", "--help",
        action  = "help",
        default = argparse.SUPPRESS,
        help    = "Show this help message and exit."
    )

    return parser

def get_args(args = None, known = True, as_dict = True):
    parser  = get_parser()

    if known:
        args, _ = parser.parse_known_args(args)
    else:
        args    = parser.parse_args(args)

    if as_dict:
        args = args.__dict__
        
    return args