# imports - module imports
from pipupgrade.model.package import Package

class Registry:
    def __init__(self,
        source,
        packages  = [ ],
        installed = False,
        sync      = False
    ):
        self.source    = source
        self.packages  = [Package(p, sync = sync) for p in packages]

        self.installed = installed