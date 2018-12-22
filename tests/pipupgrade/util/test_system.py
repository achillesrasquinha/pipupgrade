from pipupgrade.util.system import read, write

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
