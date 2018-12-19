# imports - standard imports
import sys

PY2 = int(sys.version.split(".")[0]) == 2

def cmp(a, b):
    return ((a > b) - (a < b))

if PY2:
    import __builtin__ as builtins

    # moves
    from urllib2 import urlopen
    from urllib2 import HTTPError

    from __builtin__ import raw_input as input

    from StringIO import StringIO

    from itertools import izip_longest as zip_longest
else:
    import builtins

    # moves
    from urllib.request import urlopen
    from urllib.error   import HTTPError

    from builtins import input

    from io import StringIO

    from itertools import zip_longest