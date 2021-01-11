# imports - standard imports
import sys

# imports - module imports
from pipupgrade.commands import command as main

if __name__ == "__main__":
    try:
        main()
    except e:
        raise e