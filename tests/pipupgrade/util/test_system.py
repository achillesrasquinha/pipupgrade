# imports - standard imports
import os, os.path as osp
import subprocess  as sp
from   distutils.spawn import find_executable

# imports - test imports
import pytest

# imports - module imports
from pipupgrade.util.system import read, write, popen, which

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

def test_write(tmpdir):
    directory   = tmpdir.mkdir("tmp")
    tempfile    = directory.join("foobar.txt")
    
    path        = str(tempfile) 
    
    prev, next_ = "foobar", "barfoo"

    write(path, prev)
    assert tempfile.read() == prev

    write(path, next_)
    assert tempfile.read() == prev

    write(path, next_, force = True)
    assert tempfile.read() == next_

def test_popen(tmpdir):
    directory = tmpdir.mkdir("tmp")
    dirpath   = str(directory)

    string    = "Hello, World!"

    code, out, err = popen("echo %s" % string,
        output = True)
    assert code == 0
    assert out  == string
    assert not err
    
    env = dict({ "FOOBAR": "foobar" })
    code, out, err = popen("echo $FOOBAR; echo $PATH",
        output = True, env = env)
    assert code == 0
    assert out  == "%s\n%s" % (env["FOOBAR"], os.environ["PATH"])
    assert not err

    with pytest.raises(sp.CalledProcessError):
        code = popen("exit 42")

    errstr = "foobar"
    code, out, err = popen('python -c "raise Exception("%s")"' % errstr,
        output = True, raise_err = False)
    assert code == 1
    assert not out
    assert errstr in err

    filename = "foobar.txt"
    popen("touch %s" % filename, cwd = dirpath)
    assert osp.exists(osp.join(dirpath, filename))

def test_which():
    assert which("foobar") == None
    assert which("python") == find_executable("python")

    with pytest.raises(ValueError) as e:
        which("foobar", raise_err = True)