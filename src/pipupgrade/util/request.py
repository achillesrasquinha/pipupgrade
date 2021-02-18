import requests

from pipupgrade.db import get_connection
from pipupgrade.util.proxy import get_random_requests_proxies

def proxy_request(*args, **kwargs):
    fallback = kwargs.pop("fallback", False)

    session  = requests.Session()

    proxies = get_random_requests_proxies()
    session.proxies = proxies

    try:
        response = session.request(*args, **kwargs, timeout = 5)
    except requests.exceptions.ConnectionError as e:
        if fallback:
            session.proxies = {}
            response = session.request(*args, **kwargs)
        else:
            raise e

    return response