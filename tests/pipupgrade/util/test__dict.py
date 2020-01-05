# imports - module imports
from pipupgrade.util._dict import (
    merge_dict,
    dict_from_list
)

def test_merge_dict():
    assert merge_dict({ "foo": "bar" }, { "bar": "baz" })     == { "foo": "bar", "bar": "baz" }
    assert merge_dict({ "foo": "bar" }, { "foo": "baz" })     == { "foo": "baz" }
    assert merge_dict({ 1: 2 }, { 3: 4 }, { 5: 6 }, { 7: 8 }) == { 1: 2, 3: 4, 5: 6, 7: 8 }
    assert merge_dict({ 1: 2 }, { 1: 3 }, { 1: 4 }, { 1: 1 }) == { 1: 1 }

def test_dict_from_list():
    assert dict_from_list(["foo", "bar"], [1, 2]) == dict(foo = 1, bar = 2)
    assert dict_from_list([1, 2], ["foo", "bar"]) == { 1: "foo", 2: "bar" }