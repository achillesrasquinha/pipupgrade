# imports - module imports
from pipupgrade.util.array import (
    compact,
    squash,
    flatten,
    sequencify
)

# imports - test imports
import pytest

def test_compat():
    assert compact([1, 2, None])                        == [1, 2]
    assert compact([1, 2])                              == [1, 2]
    assert compact([1, 2, "", "foo"])                   == [1, 2, "foo"]
    assert compact(["foo", "bar", ""], type_ = tuple)   == ("foo", "bar")

def test_squash():
    assert squash(["foo"])          == "foo"
    assert squash(["foo", "bar"])   == ["foo", "bar"]

def test_flatten():
    assert flatten([[1, 2], [3, 4]])    == [1, 2, 3, 4]
    assert flatten([[1, 2]])            == [1, 2]
    assert flatten([[1, 2], [ ]])       == [1, 2]

    with pytest.raises(TypeError):
        assert flatten([[1, 2], None])

def test_sequencify():
    assert sequencify("foobar") == ["foobar"]
    assert sequencify([1,2,3])  == [1,2,3]
    assert sequencify([1,2,3])  != [3,2,1]
    assert sequencify([])       == []
    assert sequencify(None)     == [None]

    assert sequencify("foobar", type_ = tuple) == ("foobar",)
    assert sequencify([1,2,3],  type_ = tuple) == (1,2,3)
    assert sequencify([1,2,3],  type_ = tuple) != (3,2,1)
    assert sequencify([],       type_ = tuple) == tuple()
    assert sequencify(None,     type_ = tuple) == (None,)