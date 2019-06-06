# imports - standard imports
from   contextlib      import contextmanager
import multiprocessing as mp

@contextmanager
def pool(*args, **kwargs):
    pool = mp.Pool(*args, **kwargs)
    yield pool
    pool.terminate()