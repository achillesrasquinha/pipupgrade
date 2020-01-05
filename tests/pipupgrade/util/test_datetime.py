# imports - test imports
import pytest

# imports - module imports
from   pipupgrade.util.datetime import (get_timestamp_str, check_datetime_format,
    _DEFAULT_TIMESTAMP_FORMAT)

def test_get_timestamp_str():
    assert check_datetime_format(get_timestamp_str(), _DEFAULT_TIMESTAMP_FORMAT)

    format_ = '%Y-%m-%d'
    assert     check_datetime_format(get_timestamp_str(format_), format_)
    assert not check_datetime_format(get_timestamp_str(),        format_)

    with pytest.raises(ValueError):
        assert check_datetime_format(get_timestamp_str(), format_, raise_err = True)