# imports - compatibility imports
from pipupgrade._compat import urlopen, HTTPError

# imports - standard imports
import json

# imports - module imports
from pipupgrade.request.response import Response

def get(url):
    response = Response()

    try:
        http_response    = urlopen(url)
        status_code      = http_response.getcode()

        response.content = http_response.read()

        http_response.close()
    except HTTPError as e:
        status_code      = e.getcode()

    response.url         = url
    response.status_code = status_code

    return response