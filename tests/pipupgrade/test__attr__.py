# imports - standard imports
import os.path as osp
import subprocess

# imports - test imports
import pytest

# imports - module imports
from pipupgrade.__attr__ import (
    read,
    pardir,
    strip,
    safe_decode,
    sequence_filter,
    get_revision
)

def call(*args, **kwargs):
    subprocess.call(args, **kwargs)

def test_read(tmpdir):
    directory = tmpdir.mkdir("tmp")
    tempfile  = directory.join("foobar.txt")
    tempfile.write("foobar")

    assert tempfile.read() == read(str(tempfile))

    tempfile  = directory.join("barfoo.txt")
    tempfile.write(\
        """
        foobar
        \n
        barfoo
        """
    )

    assert tempfile.read() == read(str(tempfile))

def test_pardir():
    assert pardir(__file__)    == osp.dirname(__file__)
    assert pardir(__file__, 2) == osp.dirname(osp.dirname(__file__))

def test_strip():
    string = "foobar"
    assert strip(string) == string

    string = "\n   foobar\nfoobar   \n   "
    assert strip(string) == "foobar\nfoobar"

    string = "\n\n\n"
    assert strip(string) == ""

    string = "\r\nfoobar\nfoobar\n"
    assert strip(string) == "foobar\nfoobar"

def test_safe_decode():
    assert safe_decode(b"foobar") == "foobar"
    assert safe_decode( "foobar") == "foobar"
    
    assert safe_decode(123456789) == 123456789

def test_sequence_filter():
    assert sequence_filter([0,1,2,3,4,5], filter_ = lambda x: x % 2 == 0)                == [0,2,4]
    assert sequence_filter([0,1,2,3,4,5], filter_ = lambda x: x % 2 != 0, type_ = tuple) == (1,3,5)

def test_get_revision(tmpdir):
    directory = tmpdir.mkdir("tmp")
    path      = str(directory)
    
    with pytest.raises(subprocess.CalledProcessError):
        get_revision(path)
    
    assert get_revision(path, raise_err = False) == None

    # Initialize the git repository
    call("git","init",path)
    call("git","config","user.email","foobar@foobar.com", cwd = path)
    call("git","config","user.name" ,"Foo Bar", cwd = path)

    with pytest.raises(subprocess.CalledProcessError):
        get_revision(path)

    tempfile  = directory.join("foobar.txt")
    tempfile.write("foobar")

    call("git","add",".", cwd = path)
    call("git","commit","-m","'Test Commit'", cwd = path)

    assert len(get_revision(path))               == 40
    assert len(get_revision(path, short = True)) == 7