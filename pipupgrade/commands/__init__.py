# imports - standard imports
import subprocess
from   subprocess import list2cmdline

# imports - module imports
from pipupgrade.commands.outdated import command as pipupgrade_check
from pipupgrade.commands.parser   import get_parsed_args
from pipupgrade.commands.util     import cli_format
from pipupgrade.util import list_filter
from pipupgrade import _pip
from pipupgrade import cli

def command():
    code    = 0
    args    = get_parsed_args()

    format_ = not args.no_color 

    if args.check:
        pipupgrade_check()
    else:
        packages  = _pip.get_installed_distributions()
        npackages = len(packages)

        query     = "Do you wish to update {} packages?".format(npackages)
        
        if args.yes or cli.confirm(query):
            for i, package in enumerate(packages):
                name   = package.project_name

                info   = cli_format("Updating {} of {} packages: {}".format(
                    i + 1,
                    npackages,
                    cli_format(name, cli.GREEN)
                ), cli.BOLD)

                cli.echo(info)

                params  = list_filter([
                    "pip",
                    "install",
                    "--quiet" if not args.verbose else None,
                    "--no-cache",
                    "--upgrade",
                    name
                ], filter_ = bool)
                command = list2cmdline(params)

                subprocess.call(command, shell = True)

            cli.echo(cli_format("UPGRADED ALL THE PACKAGES!", cli.BOLD))
        
    return code