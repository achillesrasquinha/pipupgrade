class Registry:
    def __init__(self,
        source,
        packages  = [ ],
        installed = False
    ):
        self.source    = source
        self.packages  = packages

        self.installed = installed