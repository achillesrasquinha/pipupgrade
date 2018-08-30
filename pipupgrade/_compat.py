# imports - standard imports
import sys

PY2 = int(sys.version.split(".")[0]) == 2

if PY2:
    import __builtin__ as builtins
else:
    import builtins