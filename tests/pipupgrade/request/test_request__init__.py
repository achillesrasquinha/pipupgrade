# imports - compatibility imports
from pipupgrade._compat import HTTPError

# imports - test imports
import pytest

# imports - standard imports
from pipupgrade import request as req

def test_get():
    res  = req.get("https://httpbin.org/get")
    assert res.ok
    assert res.status_code == 200
    
    json = res.json() 
    assert all(k in json for k in ("url", "origin", "headers", "args"))

    res.raise_for_status()
    
    res  = req.get("http://httpbin.org/status/404")
    assert not res.ok
    assert res.status_code == 404

    with pytest.raises(HTTPError):
        res.raise_for_status()

    assert str(res) == "<Response [{code}]>".format(
        code = 404
    )