# imports - standard imports
from   contextlib      import contextmanager
import multiprocessing as mp
from   multiprocessing.pool import Pool

class NoDaemonProcess(mp.Process):
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass

class NoDaemonProcessPool(Pool):
    Process = NoDaemonProcess

@contextmanager
def pool(class_ = Pool, *args, **kwargs):
    pool = class_(*args, **kwargs)
    yield pool
    pool.terminate()

@contextmanager
def no_daemon_pool(*args, **kwargs):
    with pool(class_ = NoDaemonProcessPool, *args, **kwargs) as p:
        yield p

        p.close(); p.join()