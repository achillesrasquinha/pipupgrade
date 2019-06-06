# imports - standard imports
import argparse

# imports - module imports
from pipupgrade.__attr__     import (
    __name__,
    __version__,
    __description__,
    __command__
)
from pipupgrade.util.environ  import getenv
from pipupgrade.cli           import util as _cli
from pipupgrade.cli.formatter import ArgumentParserFormatter
from pipupgrade._pip          import _PIP_EXECUTABLES

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
    parser.add_argument("--pip-path",
        action  = "append",
        help    = "Path to pip executable to be used."
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
        help    = "Path(s) to requirements.txt file."
    )
    parser.add_argument("--pipfile",
        action  = "append",
        help    = "Path(s) to Pipfile"
    )
    parser.add_argument("-i", "--interactive",
        action  = "store_true",
        help    = "Interactive Mode"
    )
    parser.add_argument("-p", "--project",
        action  = "append",
        help    = "Path(s) to Project"
    )
    parser.add_argument("--git-username",
        help    = "Git Username",
        default = getenv("GIT_USERNAME")
    )
    parser.add_argument("--git-email",
        help    = "Git Email",
        default = getenv("GIT_EMAIL")
    )
    parser.add_argument("--pull-request",
        action  = "store_true",
        help    = "Perform a Pull Request"
    )
    parser.add_argument("--github-access-token",
        help    = "GitHub Access Token",
        default = getenv("GITHUB_ACCESS_TOKEN")
    )
    parser.add_argument("--github-reponame",
        help    = "Target GitHub Repository Name",
        default = getenv("GITHUB_REPONAME")
    )
    parser.add_argument("--github-username",
        help    = "Target GitHub Username",
        default = getenv("GITHUB_USERNAME")
    )
    parser.add_argument("--target-branch",
        help    = "Target Branch",
        default = getenv("TARGET_BRANCH", "master")
    )
    parser.add_argument("-u", "--user",
        action  = "store_true",
        help    = "Install to the Python user install directory for environment \
                    variables and user configuration."
    )
    parser.add_argument("--no-cache",
        action  = "store_true",
        help    = "Avoid fetching latest updates from PyPI server."
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