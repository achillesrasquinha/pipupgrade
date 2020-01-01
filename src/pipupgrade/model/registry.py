# imports - module imports
from pipupgrade.model.package import Package

class Registry:
    def __init__(self,
        source,
        packages        = [ ],
        installed       = False,
        sync            = False,
        dependencies    = False
    ):
        self.source = source

        args = { "sync": sync, "dependencies": dependencies }

        if installed:
            args.update({ "pip_exec": source })

        self.packages  = [Package(p, **args)
            for p in packages
        ]

        self.installed = installed