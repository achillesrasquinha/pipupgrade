# imports - standard imports
import logging

# imports - module imports
from pipupgrade.__attr__ import __name__ as NAME

NOTSET      = logging.NOTSET
DEBUG       = logging.DEBUG
INFO        = logging.INFO
WARNING     = logging.WARNING
ERROR       = logging.ERROR
CRITICAL    = logging.CRITICAL

_FORMAT     = '%(asctime)s | %(levelname)s | %(message)s'

def get_logger(name = NAME, level = DEBUG, format_ = _FORMAT):
    formatter = logging.Formatter(format_)

    handler   = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger    = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger