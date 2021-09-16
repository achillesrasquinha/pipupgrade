# imports - standard imports
import sys
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
    parser.add_argument("packages",
        nargs   = "*",
        help    = "Packages to Upgrade."
    )
    parser.add_argument("--resolve",
        action  = "store_true",
        help    = "Resolve Dependencies"
    )
    parser.add_argument("--ignore",
        action  = "append",
        help    = "Ignore packages to upgrade."
    )
    parser.add_argument("--pip-path",
        action  = "append",
        help    = "Path to pip executable to be used."
    )
    parser.add_argument("-y", "--yes",
        action  = "store_true",
        default = getenv("ACCEPT_ALL_DIALOGS", False),
        help    = "Confirm for all dialogs."
    )
    parser.add_argument("--clean", 
        action  = "store_true",
        default = getenv("CLEAN", False),
        help    = "Clean metadata"
    )
    parser.add_argument("-c", "--check",
        action  = "store_true",
        default = getenv("DRY_RUN", False),
        help    = "Perform a dry-run, avoid updating packages."
    )
    parser.add_argument("--upgrade-type",
        choices = ("major", "minor", "patch"),
        nargs   = "+",
        default = ["minor", "patch"],
        help    = "Upgrade Type"
    )
    parser.add_argument("-l", "--latest",
        action  = "store_true",
        default = getenv("UPDATE_LATEST", False),
        help    = "Update all packages to latest."
    )
    parser.add_argument("-f", "--format",
        choices = ["table", "tree", "json", "yaml"],
        help    = "Display packages format.",
        default = getenv("DISPLAY_FORMAT", "table")
    )
    parser.add_argument("-a", "--all",
        action  = "store_true",
        default = getenv("DISPLAY_ALL_PACKAGES", False),
        help    = "List all packages."
    )
    parser.add_argument("--pip",
        action  = "store_true",
        default = getenv("UPDATE_PIP", False),
        help    = "Update pip."
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
        default = getenv("INTERACTIVE", False),
        help    = "Interactive Mode."
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
        help    = "Perform a Pull Request."
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
    parser.add_argument("-j", "--jobs",
        type    = int,
        help    = "Number of Jobs to be used.",
        default = getenv("JOBS", max(mp.cpu_count(), 4))
    )
    parser.add_argument("-u", "--user",
        action  = "store_true",
        default = getenv("USER_ONLY", False),
        help    = "Install to the Python user install directory for environment \
                    variables and user configuration."
    )
    parser.add_argument("--no-included-requirements",
        action  = "store_true",
        default = getenv("NO_INCLUDED_REQUIREMENTS", False),
        help    = "Avoid updating included requirements."
    )
    parser.add_argument("--no-cache",
        action  = "store_true",
        default = getenv("NO_CACHE", False),
        help    = "Avoid fetching latest updates from PyPI server."
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
        help    = "Force search for files within a project / Force clean."
    )
    parser.add_argument("--doctor",
        action  = "store_true",
        help    = "Perform diagnostics and fix it."
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