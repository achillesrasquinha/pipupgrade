# imports - standard imports
from subprocess import call, list2cmdline

# imports - module imports
from pipupgrade.commands.outdated import command as pipupgrade_check
from pipupgrade.commands.util     import cli_format
from pipupgrade.util import list_filter
from pipupgrade import _pip
from pipupgrade import cli

@cli.command
def command(yes = False, check = False, no_color = True, verbose = False):
    code    = 0

    format_ = not no_color 

    if check:
        pipupgrade_check()
    else:
        packages  = _pip.get_installed_distributions()
        npackages = len(packages)

        query     = "Do you wish to update {} packages?".format(npackages)
        
        if yes or cli.confirm(query):
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
                    "--quiet" if not verbose else None,
                    "--no-cache",
                    "--upgrade",
                    name
                ], filter_ = bool)
                command = list2cmdline(params)

                call(command, shell = True)

            cli.echo(cli_format("UPGRADED ALL THE PACKAGES!", cli.BOLD))
        
    return code