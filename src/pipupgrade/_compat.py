# imports - standard imports
import sys

PYTHON_VERSION = sys.version_info

def _is_python_version(*args, **kwargs):
    major  = kwargs.get("major", None)
    minor  = kwargs.get("minor", None)
    patch  = kwargs.get("patch", None)

    result = True

    if major:
        result = result and major == PYTHON_VERSION.major
    if minor:
        result = result and minor == PYTHON_VERSION.minor
    if patch:
        result = result and patch == PYTHON_VERSION.micro
        
    return result

PY2 = _is_python_version(major = 2)

def cmp(a, b):
    return ((a > b) - (a < b))

def iteritems(dict_, **kwargs):
    if PY2:
        iterator = dict_.iteritems()
    else:
        iterator = iter(dict_.items(), **kwargs)
    return iterator

def iterkeys(dict_, **kwargs):
    if PY2:
        iterator = dict_.iterkeys()
    else:
        iterator = iter(dict_.keys(), **kwargs)
    return iterator

if PY2:
    import __builtin__ as builtins

    # moves
    from urllib2 import urlopen
    from urllib2 import HTTPError

    from __builtin__ import raw_input as input

    from StringIO import StringIO

    from itertools import izip         as zip
    from itertools import izip_longest as zip_longest
else:
    import builtins

    # moves
    from urllib.request import urlopen
    from urllib.error   import HTTPError

    from builtins import input

    from io import StringIO

    from itertools import zip_longest

    zip = zip