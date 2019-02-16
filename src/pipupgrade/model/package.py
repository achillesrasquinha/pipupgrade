# imports - module imports
from pipupgrade import _pip, request as req

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
	def __init__(self, package):
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

		_pypi_info = _get_pypi_info(self.name, raise_err = False) or { }
		
		if not hasattr(self, "latest_version"):
			self.latest_version = _pypi_info.get("version")
			
		self.home_page = _pypi_info.get("home_page")