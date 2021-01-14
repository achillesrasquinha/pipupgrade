# imports - compatibility imports
from pipupgrade._compat import HTTPError

# imports - standard imports
import json

_HTTP_RESPONSE_TYPE = {
    404: { "name": "Not Found" }
}

class Response(object):
    def __init__(self):
        self.status_code = None
        self.content     = None
        self.url         = None
        
    @property
    def ok(self):
        status_code = self.status_code
        
        if status_code < 400:
            return True
        else:
            return False
        
    def json(self):
        content = self.content
        string  = content.decode()

        json_   = json.loads(string)

        return json_

    def __repr__(self):
        string = "<Response [{}]>".format(self.status_code)
        return string

    def raise_for_status(self):
        if not self.ok:
            code  = self.status_code

            name  = _HTTP_RESPONSE_TYPE[code]["name"]
            error = "{} for URL {}".format(name, self.url)

            raise HTTPError(self.url, code, error, hdrs = { }, fp = None)