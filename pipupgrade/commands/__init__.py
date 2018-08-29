# imports - module imports
from pipupgrade.commands.parser import get_parser
from pipupgrade.util import list_filter
from pipupgrade import _pip
from pipupgrade import cli

def command():
    parser    = get_parser()
    args      = parser.parse_args()

    packages  = _pip.get_installed_distributions()
    npackages = len(packages)

    query     = "Do you wish to update {} packages?".format(npackages)
    
    if args.yes or cli.confirm(query):
        for i, package in enumerate(packages):
            name   = package.project_name

            info   = cli.format("Updating {} of {} packages: {}".format(
                i + 1,
                npackages,
                name if args.no_color else cli.format(name, cli.GREEN)
            ), cli.BOLD)

            cli.echo(info)

            params = list_filter([
                "install",
                "--quiet" if not args.verbose else None,
                "--upgrade",
                name
            ], filter_ = bool)

            _pip.main(params)

        cli.echo(cli.format("UPGRADED ALL THE PACKAGES!", cli.BOLD))
    
    return 0