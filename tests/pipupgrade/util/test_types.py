# imports - module imports
from pipupgrade.util.types import (
    merge_dict,
    list_filter,
    dict_from_list,
    isdef,
    get_function_arguments
)

_TEST_GLOBAL = "foobar"

def test_merge_dict():
    assert merge_dict(dict(foo = "bar", bar = "baz"), dict(foo = "baz")) \
        == dict(foo = "baz", bar = "baz")
    assert merge_dict(dict(foo = "bar"), { 1: 2, 3: 4})                  \
        == { "foo": "bar", 1: 2, 3: 4 }

def test_list_filter():
    assert list_filter([1,2,3,None], filter_ = bool)                 == [1,2,3]
    assert list_filter([1,2,3,4,5],  filter_ = lambda x: x % 2 == 0) == [2,4]

def test_dict_from_list():
    assert dict_from_list(["foo", "bar"], [1, 2]) == dict(foo = 1, bar = 2)
    assert dict_from_list([1, 2], ["foo", "bar"]) == { 1: "foo", 2: "bar" }

def test_isdef():
    test_local = None

    assert isdef("_TEST_GLOBAL", scope = globals())
    assert isdef("test_local"  , scope =  locals())

def test_get_function_arguments():
    def foobar(foo = "bar", bar = "baz"):
        pass
    def barfoo():
        pass
    foobar(); barfoo() # Increase coverage
    
    assert get_function_arguments(foobar) == dict(foo = "bar", bar = "baz")
    assert get_function_arguments(barfoo) == dict()