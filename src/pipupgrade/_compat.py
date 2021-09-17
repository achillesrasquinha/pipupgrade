# imports - standard imports
import sys, os

# imports - module imports
import platform

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
    if PY2: # pragma: no cover
        iterator = dict_.iteritems()
    else:
        iterator = iter(dict_.items(), **kwargs)
    return iterator

def iterkeys(dict_, **kwargs):
    if PY2: # pragma: no cover 
        iterator = dict_.iterkeys()
    else:
        iterator = iter(dict_.keys(), **kwargs)
    return iterator

def itervalues(dict_, **kwargs):
    if PY2: # pragma: no cover
        iterator = dict_.itervalues()
    else:
        iterator = iter(dict_.values(), **kwargs)
    return iterator

if PYTHON_VERSION < (3,6): # pragma: no cover
    class ModuleNotFoundError(ImportError):
        pass
else:
    ModuleNotFoundError = ModuleNotFoundError

if PYTHON_VERSION > (3,8): # pragma: no cover
    from collections.abc    import Iterable
else:
    from collections        import Iterable

if PY2: # pragma: no cover
    # moves
    from urllib2 import urlopen, Request
    
    try:
        from requests.exceptions import HTTPError
    except ImportError:
        from urllib2 import HTTPError

    from urllib  import urlencode

    import __builtin__ as builtins

    from __builtin__ import raw_input as input

    from StringIO import StringIO

    from itertools import izip         as zip
    from itertools import izip_longest as zip_longest

    import ConfigParser as configparser

    string_types = basestring
    
    range        = xrange
else:
    # moves
    from urllib.request import urlopen, Request
    from urllib.parse   import urlencode

    try:
        from requests.exceptions import HTTPError
    except (ImportError, ModuleNotFoundError):
        from urllib.error   import HTTPError

    import builtins

    from builtins import input, range

    from io import StringIO

    from itertools import zip_longest

    zip = zip

    import configparser

    string_types = str

if platform.system() in ['Linux', 'Darwin']:
    EX_OK      = os.EX_OK
    EX_NOINPUT = os.EX_NOINPUT
else: # pragma: no cover
    EX_OK      = 0
    EX_NOINPUT = 66