# imports - module imports
from pipupgrade.__attr__    import (
    __name__,
    __version__,
    __author__
)
from pipupgrade.__main__    import main
from pipupgrade.config      import Settings
from pipupgrade             import _pip

settings = Settings()

from pipupgrade.tree import Node