# imports - module imports
from pipupgrade.cli.parser import get_args
from pipupgrade import cli

def cli_format(string, type_):
    args = get_args(as_dict = False)
    
    if hasattr(args, "no_color") and not args.no_color:
        string = cli.format(string, type_)

    return string