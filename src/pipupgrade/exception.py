<<<<<<< HEAD
class PipupgradeError(Exception):
    pass

=======
# imports - standard imports
import subprocess as sp

class PipupgradeError(Exception):
    pass

class PopenError(PipupgradeError, sp.CalledProcessError):
    pass

>>>>>>> template/master
class DependencyNotFoundError(ImportError):
    pass