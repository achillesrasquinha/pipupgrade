# imports - module imports
from pipupgrade.util import get_if_empty, list_filter

def test_get_if_empty():
    assert get_if_empty("foo", "bar") == "foo"
    assert get_if_empty(None,  "bar") == "bar"
    assert get_if_empty("",    "bar") == "bar"
    assert get_if_empty([],    "bar") == "bar"

def test_list_filter():
    assert list_filter([1,2,3,None], filter_ = bool)                 == [1,2,3]
    assert list_filter([1,2,3,4,5],  filter_ = lambda x: x % 2 == 0) == [2,4]