# imports - standard imports
import os.path as osp
import glob

from pipupgrade import log

logger = log.get_logger()

class Project:
    def __init__(self, path):
        path         = osp.realpath(path)

        if not osp.exists(path):
            raise ValueError("Path %s does not exist." % path)
        
        self.path         = path
        self.requirements = self._get_requirements()

        self.pipfile      = self._get_pipfile()

    def _get_requirements(self):
        # COLLECT ALL THE REQUIREMENTS FILES!
        path         = self.path
        requirements = [ ]

        # Detect Requirements Files
        # Check requirements*.txt files in current directory.
        for requirement in glob.glob(osp.join(path, "requirements*.txt")):
            requirements.append(requirement)

        # Check if requirements is a directory
        if osp.isdir(osp.join(path, "requirements")):
            for requirement in glob.glob(osp.join(path, "requirements", "*.txt")):
                requirements.append(requirement)

        return requirements

    def _get_pipfile(self):
        path    = self.path
        pipfile = osp.join(path, "Pipfile")
        
        return pipfile if osp.exists(pipfile) else None

    def __repr__(self):
        repr_ = "<Project %s>" % self.path
        return repr_