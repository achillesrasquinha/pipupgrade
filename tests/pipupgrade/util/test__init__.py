# imports - module imports
from pipupgrade.util import get_if_empty, list_filter, merge_dict

def test_get_if_empty():
    assert get_if_empty("foo", "bar") == "foo"
    assert get_if_empty(None,  "bar") == "bar"
    assert get_if_empty("",    "bar") == "bar"
    assert get_if_empty([],    "bar") == "bar"

def test_list_filter():
    assert list_filter([1,2,3,None], filter_ = bool)                 == [1,2,3]
    assert list_filter([1,2,3,4,5],  filter_ = lambda x: x % 2 == 0) == [2,4]

def test_merge_dict():
    assert merge_dict({ "foo": "bar", "bar": "baz" }, { "foo": "baz" }) \
        == dict({ "foo": "baz", "bar": "baz" })
    assert merge_dict({ "foo": "bar" }, { 1: 2, 3: 4})                  \
        == dict({ "foo": "bar", 1: 2, 3: 4 }) 