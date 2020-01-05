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

def check_datetime_format(datetime, format_, raise_err = False):
    try:
        dt.datetime.strptime(datetime, format_)
    except ValueError:
        if raise_err:
            raise ValueError("Incorrect datetime format, expected %s" % format_)
        else:
            return False
    
    return True