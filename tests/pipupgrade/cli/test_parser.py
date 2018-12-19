# imports - standard imports
from pipupgrade.cli.parser import get_parsed_args

def test_get_parsed_args():
    args = get_parsed_args()
    assert args.yes      == False
    assert args.check    == False
    assert args.no_color == False

    assert args.verbose  == False