# imports - module imports
from bpyutils.cli.util     import *
from pipupgrade.cli.parser import get_args
from bpyutils.util._dict   import merge_dict
from bpyutils.util.types   import get_function_arguments

def command(fn):
    args    = get_args()
    
    params  = get_function_arguments(fn)

    params  = merge_dict(params, args)
    
    def wrapper(*args, **kwargs):
        return fn(**params)

    return wrapper