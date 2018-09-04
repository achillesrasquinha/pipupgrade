# imports - standard imports
import argparse

# imports - module imports
from pipupgrade.__attr__ import __version__, __description__

def get_parser():
    parser = argparse.ArgumentParser(
        description = __description__
    )
    parser.add_argument("-y", "--yes",
        action  = "store_true",
        help    = "Confirm for all dialogs"
    )
    parser.add_argument("-s", "--self",
        action  = "store_true",
        help    = "Upgrade self"
    )
    parser.add_argument("-c", "--check",
        action  = "store_true",
        help    = "Check for outdated packages"
    )
    parser.add_argument("-l", "--latest",
        action  = "store_true",
        help    = "Install the latest version"
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

    return parser

def get_parsed_args():
    parser        = get_parser()
    args, unknown = parser.parse_known_args()

    return args