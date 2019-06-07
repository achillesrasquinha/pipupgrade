# imports - standard imports
from   datetime import datetime
import threading

# imports - module imports
from pipupgrade import _pip, request as req, db, log

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

class Package:
	def __init__(self, package, sync = False):
		logger.info("Initializing Package %s of type %s..." % (package, type(package)))

		if   isinstance(package, (_pip.Distribution, _pip.DistInfoDistribution, _pip.EggInfoDistribution)):
			self.name            = package.project_name
			self.current_version = package.version
		elif isinstance(package, _pip.InstallRequirement):
			self.name            = package.name
			self.current_version = package.installed_version
		elif isinstance(package, dict):
			self.name            = package["name"]
			self.current_version = package["version"]
			self.latest_version  = package.get("latest_version")

		_db = db.get_connection()
		try:
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