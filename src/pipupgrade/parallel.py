# imports - standard imports
from   contextlib      import contextmanager
import multiprocessing as mp
from   multiprocessing.pool import Pool

class NoDaemonProcess(mp.Process):
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class NoDaemonProcessPool(Pool):
    Process = NoDaemonProcess

@contextmanager
def pool(class_ = mp.Pool, *args, **kwargs):
    pool = class_(*args, **kwargs)
    yield pool
    pool.terminate()

@contextmanager
def no_daemon_pool(*args, **kwargs):
    with pool(class_ = NoDaemonProcessPool, *args, **kwargs) as p:
        yield p

        p.close(); p.join()