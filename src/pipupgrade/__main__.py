from __future__ import absolute_import

import sys

from   pipupgrade.commands import command as main

if __name__ == "__main__":
    code = main()
    sys.exit(code)