# imports - standard imports
import os.path as osp
import re
import csv

from pipupgrade.config      import PATH
from pipupgrade.db          import get_connection
from pipupgrade.util.system import popen
from pipupgrade.exception   import PopenError
from pipupgrade import log, db

PROXY_COLUMNS = "host,port,secure,anonymity,country_code,available,error_rate,average_response_time"

logger      = log.get_logger(level = log.DEBUG)
connection  = db.get_connection()

def save(values):
    connection.query("""
        BEGIN TRANSACTION;
        %s
        COMMIT;
    """ % "\n".join([ "INSERT OR IGNORE INTO `tabProxies` (%s) VALUES (%s);"
        % (PROXY_COLUMNS, ",".join(map(lambda x: '"%s"' % x, v)))
            for v in values])
    , script = True)

def fetch():
    dir_path = PATH["CACHE"]

    # seed database...
    repo = osp.join(dir_path, "proxy-list")

    if not osp.exists(repo):
        popen("git clone https://github.com/achillesrasquinha/proxy-list %s" % repo, cwd = dir_path)
    else:
        try:
            popen("git pull origin master", cwd = repo)
        except PopenError:
            logger.warn("Unable to pull latest branch")

    proxies_path = osp.join(repo, "proxies.csv")

    if osp.exists(proxies_path):
        logger.info("Reading cached proxies...")

        with open(proxies_path, newline = '') as csvfile:
            reader  = csv.reader(csvfile)
            values  = list(reader)[1:]

            save(values)

def to_addr(proxy):
    return "%s:%s" % (proxy["host"], str(proxy["port"]))

def get_random_proxy(secure = False, error_rate = 0.5, avg_resp_time = 0.5):
    db      = get_connection()
    where   = "secure = %s and error_rate <= %s and average_response_time <= %s" % (int(secure), error_rate,
        avg_resp_time)

    result  = db.query("SELECT * FROM `tabProxies` WHERE %s ORDER BY RANDOM() LIMIT 1" % where)

    if result:
        return to_addr(result)

def get_random_requests_proxies():
    return {
        "http": get_random_proxy(),
        # "https": get_random_proxy(secure = True)
    }