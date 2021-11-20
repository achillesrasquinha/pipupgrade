# imports - standard imports
import sys
import os
import argparse
import multiprocessing as mp

# imports - module imports
from pipupgrade.__attr__     import (
    __name__,
    __version__,
    __description__,
    __command__
)
from bpyutils.util.environ    import getenv
from bpyutils.cli             import util as _cli
from bpyutils.cli.formatter   import ArgumentParserFormatter
from bpyutils.cli.util        import _CAN_ANSI_FORMAT

_DESCRIPTION_JUMBOTRON = \
"""
%s (v %s)

%s
""" % (
    _cli.format(__name__,        _cli.RED),
    _cli.format(__version__,     _cli.BOLD),
    _cli.format(__description__, _cli.BOLD)
)

def get_parser():
    parser = argparse.ArgumentParser(
        prog            = __command__,
        description     = _DESCRIPTION_JUMBOTRON,
        add_help        = False,
        formatter_class = ArgumentParserFormatter
    )
    parser.add_argument("-y", "--yes",
        action  = "store_true",
        default = getenv("ACCEPT_ALL_DIALOGS", False),
        help    = "Confirm for all dialogs."
    )
    parser.add_argument("-c", "--check",
        action  = "store_true",
        default = getenv("DRY_RUN", False),
        help    = "Perform a dry-run."
    )
    parser.add_argument("-i", "--interactive",
        action  = "store_true",
        default = getenv("INTERACTIVE", False),
        help    = "Interactive Mode."
    )
    parser.add_argument("-j", "--jobs",
        type    = int,
        help    = "Number of Jobs to be used.",
        default = getenv("JOBS", max(mp.cpu_count(), 4))
    )
    parser.add_argument("-o", "--output",
        default = getenv("OUTPUT_FILE"),
        help    = "Print Output to File."
    )
    parser.add_argument("--ignore-error",
        action  = "store_true",
        default = getenv("IGNORE_ERROR", False),
        help    = "Ignore Error in case of failure."
    )
    parser.add_argument("--force",
        action  = "store_true",
        default = getenv("FORCE", False),
        help    = "Force."
    )

    if _CAN_ANSI_FORMAT or "pytest" in sys.modules:
        parser.add_argument("--no-color",
            action  = "store_true",
            default = getenv("NO_COLOR", False),
            help    = "Avoid colored output."
        )

    parser.add_argument("-V", "--verbose",
        action  = "store_true",
        help    = "Display verbose output.",
        default = getenv("VERBOSE", False)
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