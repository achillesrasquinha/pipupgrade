# imports - compatibility imports
from __future__ import absolute_import

# imports - standard imports
import time
import datetime as dt

_DEFAULT_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_timestamp_str(format_ = _DEFAULT_TIMESTAMP_FORMAT):
    now       = time.time()
    
    datetime_ = dt.datetime.fromtimestamp(now)
    string    = datetime_.strftime(format_)

    return string