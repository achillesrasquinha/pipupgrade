# imports - standard imports
import os.path as osp
import sqlite3

# imports - module imports
from pipupgrade.__attr__    import __name__ as NAME
from pipupgrade.util.string import strip
from pipupgrade.util.system import makedirs, read
from pipupgrade             import config, log

logger = log.get_logger()

IntegrityError      = sqlite3.IntegrityError
OperationalError    = sqlite3.OperationalError

def _get_queries(buffer):
    queries = [ ]
    lines   = buffer.split(";")

    for line in lines:
        line = strip(line)
        queries.append(line)

    return queries

class DB(object):
    def __init__(self, path, timeout = 10):
        self.path        = path
        self._connection = None
        self.timeout     = timeout

    @property
    def connected(self):
        _connected = bool(self._connection)
        return _connected

    def connect(self, bootstrap = True, **kwargs):
        if not self.connected:
            self._connection = sqlite3.connect(self.path,
                timeout = self.timeout, **kwargs)
            self._connection.row_factory = sqlite3.Row

    def query(self, *args, **kwargs):
        if not self.connected:
            self.connect()

        cursor  = self._connection.cursor()
        cursor.execute(*args, **kwargs)
        self._connection.commit()

        results = cursor.fetchall()
        results = [dict(result) for result in results]

        if len(results) == 1:
            results = results[0]

        cursor.close()

        return results

_CONNECTION = None

def get_connection(bootstrap = True, log = False):
    global _CONNECTION

    if not _CONNECTION:
        if log:
            logger.info("Establishing a DataBase connection...")

        basepath    = osp.join(osp.expanduser("~"), ".%s" % NAME)
        makedirs(basepath, exist_ok = True)

        abspath     = osp.join(basepath, "db.db")

        _CONNECTION = DB(abspath)
        _CONNECTION.connect(detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

        if bootstrap:
            if log:
                logger.info("Bootstrapping DataBase...")

            abspath = osp.join(config.PATH["DATA"], "bootstrap.sql")
            buffer  = read(abspath)

            queries = _get_queries(buffer)

            for query in queries:
                _CONNECTION.query(query)

    return _CONNECTION