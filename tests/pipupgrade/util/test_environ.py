# imports - test imports
import pytest

# imports - module imports
from pipupgrade.util.environ import value_to_envval

def test_value_to_envval():
    assert value_to_envval(True)     == "true"
    assert value_to_envval(False)    == "false"
    assert value_to_envval(12345)    == "12345"
    assert value_to_envval("foobar") == "foobar"

    with pytest.raises(TypeError):
        value_to_envval(str)
        
    with pytest.raises(TypeError):
        value_to_envval([ ])