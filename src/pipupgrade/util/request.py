import requests

from pipupgrade.db import get_connection

def get_random_proxy(protocol = "http"):
    db      = get_connection()
    where   = "protocol = '%s'" % (protocol)

    result  = db.query("SELECT * FROM `tabProxies` WHERE %s ORDER BY RANDOM() LIMIT 1" % where)

    return "%s://%s:%s" % (result["protocol"], result["ip"], result["port"])

def proxy_request(*args, **kwargs):
    session = requests.Session()

    proxies = { "http": get_random_proxy(), "https": get_random_proxy(protocol = "https") }
    session.proxies = proxies

    try:
        response = session.request(*args, **kwargs, timeout = 5)
    except requests.exceptions.ConnectionError as e:
        session.proxies = {}
        response = session.request(*args, **kwargs)

    return response