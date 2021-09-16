# imports - module imports
from pipupgrade.semver import parse, difference

# imports - test imports
import pytest

def test_parse():
    version = parse("1.2.3")
    assert version["major"] == 1
    assert version["minor"] == 2
    assert version["patch"] == 3
    assert not version["prerelease"]
    assert not version["build"]

    version = parse("1.2.3-develop+1234")
    assert version["major"] == 1
    assert version["minor"] == 2
    assert version["patch"] == 3
    assert version["prerelease"] == "develop"
    assert version["build"]      == "1234"

    with pytest.raises(ValueError):
        parse("foobar")
    
    with pytest.raises(ValueError):
        parse("1.0")

def test_difference():
    assert difference("1.2.3", "2.3.4") == "major"
    assert difference("1.2.3", "1.3.4") == "minor"
    assert difference("1.2.3", "1.2.1") == "patch"
    assert difference("1.2.3", "1.2.3") == None

    with pytest.raises(ValueError):
        difference("1.2.3", "1.0")

    with pytest.raises(ValueError):
        difference("1.2.3.4", "1.2.3.4")

    with pytest.raises(NotImplementedError):
        difference("1.2.3-develop", "1.2.3")