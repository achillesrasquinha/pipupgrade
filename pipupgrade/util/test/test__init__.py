# imports - module imports
from pipupgrade.util import get_if_empty

def test_get_if_empty():
    assert get_if_empty("foo", "bar") == "foo"
    assert get_if_empty(None,  "bar") == "bar"
    assert get_if_empty("",    "bar") == "bar"
    assert get_if_empty([],    "bar") == "bar"