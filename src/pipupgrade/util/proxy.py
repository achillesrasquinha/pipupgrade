# imports - standard imports
import re

from pipupgrade.db  import get_connection

REGEX_PROXY_STRING = r"^(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]) (?P<country_code>[A-Z][A-Z])-(?P<anonymity>N|A|H)?(?P<secure>\s|-S)?(?P<one_way>\!)?\s*(?P<google_passed>\+|-)*"

def to_dict(proxy, db_cast = False):
    output = re.match(REGEX_PROXY_STRING, proxy)
    
    if output:
        output  = output.groupdict()

        type_   = int if db_cast else bool

        # sanitize output
        output["secure"]        = type_(output["secure"]        == "-S")
        output["one_way"]       = type_(output["one_way"]       == "!")
        output["google_passed"] = type_(output["google_passed"] == "+")

        print(proxy, output)

        return output

def _concat_helper(fn, b):
    return b if fn() else ""

def to_str(proxy):
    string  = "%s:%s %s-%s" % (proxy["ip"], str(proxy["port"]),
        proxy["country_code"], proxy["anonymity"])

    string += _concat_helper(lambda: proxy["secure"], "-S")
    string += _concat_helper(lambda: proxy["one_way"], "!")
    string += _concat_helper(lambda: proxy["google_passed"], " +")

    return string

def get_random_proxy(secure = False, google_passed = False):
    db      = get_connection()
    where   = "secure = %s and google_passed = %s" % (
        int(secure), int(google_passed)
    )

    result  = db.query("SELECT * FROM `tabProxies` WHERE %s ORDER BY RANDOM() LIMIT 1" % where)
    
    if result:
        return "%s://%s:%s" % ("https" if result["secure"] else "http", result["ip"], str(result["port"]))

def get_random_requests_proxies():
    return {
        "http":  get_random_proxy(),
        "https": get_random_proxy(secure = True)
    }