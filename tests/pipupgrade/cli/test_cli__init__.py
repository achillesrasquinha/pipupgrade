# imports - compatibility imports
<<<<<<< HEAD
from bpyutils._compat import iteritems, iterkeys
=======
from pipupgrade._compat import iteritems, iterkeys
>>>>>>> template/master

# imports - module imports
from pipupgrade import cli
from pipupgrade.cli import get_args
from bpyutils.util._dict import merge_dict

def test_command():
    def _assert_command(values, override = dict(), initial = dict()):
        @cli.command
        def foobar(*args, **kwargs):
            args    = get_args()
            params  = merge_dict(args, override)
            
            for k, v in iteritems(values):
                assert params[k] == v

            if initial:
                for k in iterkeys(initial):
                    assert initial[k] == args[k]
        
        foobar()
    
<<<<<<< HEAD
    _assert_command(dict(yes    = False))
    _assert_command(dict(latest = True), dict(latest = True), dict(latest = False))
    _assert_command(dict(force  = True), dict(force  = True), dict(force  = False))
=======
    _assert_command(dict(yes = False))
    _assert_command(dict(force = True), dict(force = True), dict(force = False))
>>>>>>> template/master
