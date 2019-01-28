# imports - standard imports
import os, os.path as osp
import subprocess  as sp

# imports - module imports
from pipupgrade.util.string import strip
from pipupgrade._compat     import iteritems

def read(fname):
    with open(fname) as f:
        data = f.read()
    return data

def write(fname, data = None, force = False):
    if not osp.exists(fname) or force:
        with open(fname, "w") as f:
            if data:
                f.write(data)

def popen(*args, **kwargs):
    output      = kwargs.get("output", False)
    directory   = kwargs.get("cwd")
    environment = kwargs.get("env")
    shell       = kwargs.get("shell", True)
    raise_err   = kwargs.get("raise_err", True)

    environ     = os.environ.copy()
    if environment:
        environ.update(environment)

    for k, v in iteritems(environ):
        environ[k] = str(v)

    command     = " ".join([str(arg) for arg in args])
    
    proc        = sp.Popen(command,
        stdin   = sp.PIPE if output else None,
        stdout  = sp.PIPE if output else None,
        stderr  = sp.PIPE if output else None,
        env     = environ,
        cwd     = directory,
        shell   = shell
    )

    code       = proc.wait()

    if code and raise_err:
        raise sp.CalledProcessError(code, command)

    if output:
        output, error = proc.communicate()

        if output:
            output = output.decode("utf-8")
            output = strip(output)

        if error:
            error  = error.decode("utf-8")
            error  = strip(error)

        return code, output, error
    else:
        return code
