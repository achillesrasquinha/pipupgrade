# imports - standard imports
import re

from pipupgrade.db  import get_connection

def to_addr(proxy):
    return "%s://%s:%s" % ("https" if proxy["secure"] else "http", proxy["host"],
        str(proxy["port"]))

def get_random_proxy(secure = False, available = True):
    db      = get_connection()
    where   = "secure = %s and available = %s" % (int(secure), int(available))

    result  = db.query("SELECT * FROM `tabProxies` WHERE %s ORDER BY RANDOM() LIMIT 1" % where)

    if result:
        return to_addr(result)

def get_random_requests_proxies():
    return {
        "http":  get_random_proxy(),
        "https": get_random_proxy(secure = True)
    }