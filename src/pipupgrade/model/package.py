# imports - standard imports
from   	datetime	import datetime
from 	functools 	import partial
import 	os.path as osp
import 	re

# imports - module imports
from pipupgrade.__attr__    import __name__ as NAME
from pipupgrade 	 		import _pip, request as req, db, log
from pipupgrade.tree 		import Node as TreeNode
from pipupgrade.io			import _json
from pipupgrade.util.array  import compact
from pipupgrade.util.string import kebab_case
from pipupgrade.util.system import makedirs
from pipupgrade._compat		import iteritems
from pipupgrade				import parallel

logger = log.get_logger()

def _get_pypi_info(name, raise_err = True):
	url  = "https://pypi.org/pypi/{}/json".format(name)
	res  = req.get(url)

	info = None

	if res.ok:
		data = res.json()
		info = data["info"]
	else:
		if raise_err:
			res.raise_for_status()

	return info

def _get_package_info(package, pip_exec = _pip._PIP_EXECUTABLE):
	logger.info("Fetching Package Information %s..." % package)
	
	_, out, err	= _pip.call("show", package, pip_exec = pip_exec,
		output = True)
	
	info		= dict((kebab_case(k), v) \
		for k, v in \
			iteritems(
				dict([(s + [""]) if len(s) == 1 else s
					for s in [re.split(':\s?', o, maxsplit = 1) for o in out.split("\n")]]
				)
			)
	)

	return info

def _get_dependency_cache_path(package):
	path = osp.join(osp.expanduser("~"), ".%s" % NAME,
		"deps", package.name, package.current_version)
	return path

def _get_dependency_tree_from_cache(package):
	basepath	= _get_dependency_cache_path(package)
	depspath	= osp.join(basepath, "tree.json")
	
	tree		= None

	if osp.exists(depspath):
		dict_ 	= _json.read(depspath)
		tree 	= TreeNode.from_dict(dict_,
			# objectify = 
		)

	return tree
	
def _save_dependency_tree_to_cache(package, dependencies):
	basepath    = _get_dependency_cache_path(package)
	makedirs(basepath, exist_ok = True)

	depspath	= osp.join(basepath, "tree.json")

	if not osp.exists(depspath):
		_json.write(depspath, dependencies.to_dict(repr_ = lambda x: x.name))

def _get_dependency_tree_helper(dependency, pip_exec = None):
	child = _get_dependency_tree(Package(dependency, pip_exec = pip_exec,
		dependencies = True
	), pip_exec = pip_exec)
	return child

def _get_dependency_tree(package, pip_exec = _pip._PIP_EXECUTABLE):
	logger.info("Fetching Dependencies for %s..." % package)

	tree 		= TreeNode(package)
	info		= _get_package_info(package.name,
		pip_exec = pip_exec)

	dependencies = compact(info["requires"].split(", "))
	logger.info("Dependencies found: %s." % dependencies)

	with parallel.no_daemon_pool() as pool:
		children = pool.map(
			partial(
				_get_dependency_tree_helper,
				**{
					"pip_exec": pip_exec
				}
			),
			dependencies
		)
		
		if children:
			tree.add_children(*children)

	return tree

def _get_current_package_version(package, pip_exec = _pip._PIP_EXECUTABLE):
	info = _get_package_info(package,
		pip_exec = pip_exec)
	return info["version"]

class Package:
	def __init__(self, package, sync = False):
		logger.info("Initializing Package %s of type %s..." % (package, type(package)))

		if   isinstance(package, (_pip.Distribution, _pip.DistInfoDistribution,
			_pip.EggInfoDistribution)):
			self.name            = package.project_name
			self.current_version = package.version
		elif isinstance(package, _pip.InstallRequirement):
			self.name            = package.name

			if hasattr(package, "req"):
				if hasattr(package.req, "specifier"):
					self.current_version = str(package.req.specifier)
			else:
				self.current_version = package.installed_version
		elif isinstance(package, dict):
			self.name            = package["name"]
			self.current_version = package["version"]
			self.latest_version  = package.get("latest_version")

		_db = db.get_connection()
		res = None

		try:
			logger.info("Fetching package %s information from DB..." % self.name)

			res = _db.query("""
				SELECT *
				FROM `tabPackage`
				WHERE name = '%s'
			""" % self.name)
		except db.OperationalError as e:
			logger.warn("Unable to fetch package name. %s" % e)

		if not res or sync:
			logger.info("Fetching PyPI info for package %s..." % self)
			_pypi_info = _get_pypi_info(self.name, raise_err = False) or { }
		
			if not hasattr(self, "latest_version"):
				self.latest_version = _pypi_info.get("version")

			self.home_page = _pypi_info.get("home_page")

		self.dependencies = TreeNode("dependencies")

		if not res:
			try:
				logger.info("Attempting to INSERT package %s into database." % self)

				_db.query("""
					INSERT INTO `tabPackage`
						(name, latest_version, home_page, _created_at)
					VALUES
						('%s', '%s', '%s', '%s')
				""" % (self.name, self.latest_version, self.home_page, datetime.now()))
			except (db.IntegrityError, db.OperationalError) as e:
				logger.warn("Unable to save package name. %s" % e)
		else:
			if sync:
				logger.info("Attempting to UPDATE package %s within database." % self)

				try:
					_db.query("""
						UPDATE `tabPackage`
							SET latest_version = '%s', home_page = '%s', _updated_at = '%s'
						WHERE
							name = '%s'
					""" % (self.latest_version, self.home_page, datetime.now(), self.name))
				except db.OperationalError as e:
					logger.warn("Unable to update package name. %s" % e)
			else:
				logger.info("Using cached info for package %s." % self)

				self.latest_version = res["latest_version"]
				self.home_page      = res["home_page"]

	def __repr__(self):
		repr_ = "<Package %s (%s)>" % (self.name, self.current_version)
		return repr_

	def to_dict(self):
		pass

	def to_yaml(self):
		pass