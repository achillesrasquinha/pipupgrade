# imports - standard imports
import os.path as osp
import glob

# imports - module imports
from pipupgrade import log
from pipupgrade.util.string import strip

logger = log.get_logger()

class Project:
	@staticmethod
	def from_path(path, *args, **kwargs):
		project = Project(path, *args, **kwargs)
		return project

	def __init__(self, path):
		path = osp.realpath(path)

		if not osp.exists(path):
			logger.error("Failed to initialize project for path %s." % path)
			raise ValueError("Path %s does not exist." % path)
		
		logger.info("Initializing project with path %s." % path)
		self.path         = path
		logger.info("Fetching requirements...")
		self.requirements = self._get_requirements()

		logger.info("Fetching Pipfile...")
		self.pipfile      = self._get_pipfile()

	def _get_requirements(self):
		# COLLECT ALL THE REQUIREMENTS FILES!
		path         = self.path
		requirements = [ ]

		# Detect Requirements Files
		# Check requirements*.txt files in current directory.
		for requirement in glob.glob(osp.join(path, "requirements*.txt")):
			logger.info("Requirement found at %s." % requirement)
			requirements.append(requirement)

		# Check if requirements is a directory
		if osp.isdir(osp.join(path, "requirements")):
			for requirement in glob.glob(osp.join(path, "requirements", "*.txt")):
				logger.info("Requirement found at %s." % requirement)
				requirements.append(requirement)

		return requirements

	def _get_pipfile(self):
		path    = self.path
		pipfile = osp.join(path, "Pipfile")

		if pipfile:
			logger.info("Pipfile found at %s." % pipfile)
		
		return pipfile if osp.exists(pipfile) else None

	def __repr__(self):
		repr_ = "<Project %s>" % self.path
		return repr_

def get_included_requirements(filename):
	path         = osp.realpath(filename)
	basepath     = osp.dirname(path)
	requirements = [ ]

	with open(path) as f:
		content = f.readlines()

		for line in content:
			line = strip(line)

			if line.startswith("-r "):
				filename = line.split("-r ")[1]
				realpath = osp.join(basepath, filename)
				requirements.append(realpath)

				requirements += get_included_requirements(realpath)

	return requirements