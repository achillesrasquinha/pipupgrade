# imports - standard imports
import collections

# imports - module imports
from pipupgrade._compat import (cmp, input, StringIO, iteritems, iterkeys,
    PYTHON_VERSION, _is_python_version)

# imports - test imports
from testutils import mock_input, assert_input

def test_imports():
    from pipupgrade._compat import (
        StringIO    as _,

        urlopen     as _,
        HTTPError   as _,
        
        zip_longest as _,
        
        input       as _
    )

def test__is_python_version():
    def _assert_version(major, minor):
        if PYTHON_VERSION.major == major and PYTHON_VERSION.minor == minor:
            assert _is_python_version(major = major, minor = minor)

    _assert_version(2, 7)
    _assert_version(3, 4)
    _assert_version(3, 5)
    _assert_version(3, 6)
    _assert_version(3, 7)

    assert _is_python_version(
        major = PYTHON_VERSION.major,
        minor = PYTHON_VERSION.minor,
        patch = PYTHON_VERSION.micro
    )

def test_input(capfd):
    query = "foobar"
    assert_input(capfd, query, "Y", input_ = input)

def test_cmp():
    assert cmp(1, 2) == -1
    assert cmp(1, 1) ==  0
    assert cmp(2, 1) ==  1

def test_iteritems():
    dict_ = dict(foo = "bar")
    
    assert isinstance(iteritems(dict_), collections.Iterable)

    for k, v in iteritems(dict_):
        assert dict_[k] == v

def test_iterkeys():
    dict_ = dict(foo = "bar")
    
    assert isinstance(iterkeys(dict_), collections.Iterable)

    for k in iterkeys(dict_):
        assert k in dict_