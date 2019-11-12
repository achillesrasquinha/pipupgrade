# imports - standard imports
import subprocess as sp

class PipupgradeError(Exception):
    pass

class PopenError(PipupgradeError, sp.CalledProcessError):
    pass