# imports - module imports
from pipupgrade.cli.parser import get_parsed_args
from pipupgrade import cli

def cli_format(string, type_):
    args = get_parsed_args()

    if not args.no_color:
        string = cli.format(string, type_)

    return string