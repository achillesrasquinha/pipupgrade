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