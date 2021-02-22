import requests
import grequests
from fake_useragent import UserAgent

from pipupgrade.db import get_connection
from pipupgrade.util.proxy import get_random_requests_proxies
from pipupgrade.util._dict import merge_dict

user_agent = UserAgent()

def proxy_request(*args, **kwargs):
    fallback = kwargs.pop("fallback", False)

    session  = requests.Session()

    proxies = get_random_requests_proxies()
    session.headers.update({ "User-Agent": user_agent.random })
    session.proxies.update(proxies)

    try:
        response = session.request(*args, **kwargs, timeout = 5)
    except requests.exceptions.ConnectionError as e:
        if fallback:
            session.headers = kwargs.get("headers", {})
            session.proxies = kwargs.get("proxies", {})
            response = session.request(*args, **kwargs)
        else:
            raise e

    return response

def proxy_grequest(*args, **kwargs):
    proxies = get_random_requests_proxies()
    
    kwargs["headers"] = merge_dict(kwargs.get("headers", {}), {
        "User-Agent": user_agent.random })
    kwargs["proxies"] = merge_dict(kwargs.get("proxies", {}), proxies)

    return grequests.request(*args, **kwargs)