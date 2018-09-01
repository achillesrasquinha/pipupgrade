# imports - standard imports
import sys

PY2 = int(sys.version.split(".")[0]) == 2

if PY2:
    import __builtin__ as builtins

    # moves
    from urllib2  import urlopen
    from urllib2  import HTTPError
else:
    import builtins

    # moves
    from urllib.request import urlopen
    from urllib.error   import HTTPError

from builtins import input