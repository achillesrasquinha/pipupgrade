# imports - compatibility imports
from __future__ import absolute_import

# imports - standard imports
import os.path as osp
from   datetime	import datetime, timedelta
import re

# imports - module imports
from pipupgrade.__attr__    import __name__ as NAME
from pipupgrade 	 		import _pip, semver
from pipupgrade.config 		import PATH
from bpyutils.tree 			import Node as TreeNode
from bpyutils.util.string 	import kebab_case, strip
from bpyutils.util._dict  	import merge_dict
from bpyutils._compat		import iterkeys, iteritems, string_types
from bpyutils.config		import Settings, get_config_path

from bpyutils import request as req, db, log

logger  	= log.get_logger(name = NAME)
_db			= db.get_connection(location = get_config_path(NAME))
_db.from_file(osp.join(PATH["DATA"], "bootstrap.sql"))

settings	= Settings()

def _get_pypi_info(name, raise_err = True):
	url  = "https://pypi.org/pypi/{}/json".format(name)
	res  = req.get(url)

	info = None

	if res.ok:
		data = res.json()
		info = merge_dict(data["info"], { "releases": data["releases"] })
	else:
		if raise_err:
			res.raise_for_status()

	return info

def _get_pip_info(*args, **kwargs):
	packages	= args
	pip_exec	= kwargs.get("pip_exec", None)
	
	_, out, _	= _pip.call("show", *packages, pip_exec = pip_exec,
		output = True)
	results		= [strip(o) for o in out.split("---")]
	
	info		= dict()
	
	for i, package in enumerate(packages):
		result = results[i]

		detail = dict((kebab_case(k), v.strip() if isinstance(v, string_types) else v) \
			for k, v in \
				iteritems(
					dict([(s + [""]) if len(s) == 1 else s \
						for s in [re.split(r":\s?", o, maxsplit = 1) \
							for o in result.split("\n")]]
					)
				)
		)

		info[package] = detail
	
	return info

# def _get_package_version(package, pip_exec = None):
# 	info = _get_pip_info(package, pip_exec = pip_exec)[package]
# 	return info["version"]

def to_datetime(string):
	return datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f")

class Package(object):
	def __init__(self, package, sync = False, pip_exec = None):
		logger.info("Initializing Package %s of type %s..." % (package, type(package)))

		self.current_version 	= None
		# self.dependencies       = [ ]

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
		elif isinstance(package, str):
			self.name = package
			if pip_exec:
				info = _get_pip_info(self.name)

				self.current_version = info["version"]
				# self.dependencies    = info["requires"]

		# if pip_exec and not self.dependencies:
		# 	self.dependencies = _get_pip_info(self.name)

		self.extras = frozenset()

		res = None

		try:
			logger.info("Fetching package %s information from DB..." % self.name)

			res = _db.query("""
				SELECT *
				FROM `tabPackage`
				WHERE name = '%s'
			""" % self.name)
		except db.OperationalError as e:
			logger.warning("Unable to fetch package name. %s" % e)

		if res:
			cache_timeout = settings.get("cache_timeout")

			if res["_updated_at"]:
				time_difference	= to_datetime(res["_updated_at"]) + timedelta(seconds = cache_timeout)

				if datetime.now() > time_difference:
					sync = True
			else:
				sync = True

		if not res or sync:
			logger.info("Fetching PyPI info for package %s..." % self)
			_pypi_info = _get_pypi_info(self.name, raise_err = False) or { }
		
			if not getattr(self, "latest_version", None) or sync:
				self.latest_version = _pypi_info.get("version")

			self.home_page  = _pypi_info.get("home_page")
			self.releases   = [version for version in iterkeys(_pypi_info.get("releases") or [])]

		if not res:
			try:
				values = (self.name, self.latest_version or "NULL", self.home_page, ",".join(self.releases), datetime.now(), datetime.now())
				logger.info("Attempting to INSERT package %s into database with values: %s." % (self, values))

				_db.query("""
					INSERT INTO `tabPackage`
						(name, latest_version, home_page, releases, _created_at, _updated_at)
					VALUES
						('%s', '%s', '%s', '%s', '%s', '%s')
				""" % values)
			except (db.IntegrityError, db.OperationalError) as e:
				logger.warning("Unable to save package name. %s" % e)
		else:
			if sync:
				logger.info("Attempting to UPDATE package %s within database." % self)

				try:
					_db.query("""
						UPDATE `tabPackage`
							SET latest_version = '%s', home_page = '%s', releases = '%s', _updated_at = '%s'
						WHERE
							name = '%s'
					""" % (self.latest_version, self.home_page, ",".join(self.releases), datetime.now(), self.name))
				except db.OperationalError as e:
					logger.warning("Unable to update package name. %s" % e)
			else:
				logger.info("Using cached info for package %s." % self)

				self.latest_version = res["latest_version"]
				self.home_page      = res["home_page"]
				self.releases       = res["releases"].split(",")

		self.dependency_tree = TreeNode(self)

	@property
	def difference(self):
		difference = None

		try:
			difference = semver.difference(
				self.current_version,
				self.latest_version
			)
		except (TypeError, ValueError):
			pass

		return difference

	def __repr__(self):
		repr_ = "<Package %s%s>" % (self.name,
			" (%s)" % self.current_version if self.current_version else "")
		return repr_

	def to_dict(self):
		dependencies = self.dependency_tree.to_dict(repr_ = lambda x: x.name)
		
		dict_ 		 = dict({
					   "name": self.name,
			"current_version": self.current_version,
			 "latest_version": self.latest_version,
				  "home_page": self.home_page,
                   "releases": self.releases,
			   "dependencies": dependencies[self.name]
		})

		return dict_