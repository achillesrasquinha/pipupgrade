# imports - standard imports
import sys, os, os.path as osp
import re
import json

# imports - module imports
from pipupgrade.model         	import Registry
from pipupgrade.commands.util 	import cli_format
from pipupgrade.table      	  	import Table
from pipupgrade.util.string     import pluralize
from pipupgrade.util.system   	import read, write, popen, which
from pipupgrade 		      	import (_pip, cli, semver,
	log, parallel
)

logger = log.get_logger()

_SEMVER_COLOR_MAP = dict(
	major = cli.RED,
	minor = cli.YELLOW,
	patch = cli.GREEN
)

def _cli_format_semver(version, type_):
	def _format(x):
		return cli_format(x, cli.YELLOW)
	
	try:
		semver.parse(version)
		
		if type_ == "major":
			version    = _format(version)
		if type_ == "minor":
			index      = version.find(".", 1) + 1
			head, tail = version[:index], version[index:]
			version    = "".join([head, _format(tail)])
		if type_ == "patch":
			index      = version.find(".", 2) + 1
			head, tail = version[:index], version[index:]
			version    = "".join([head, _format(tail)])
	except ValueError:
		pass

	return version

def _update_requirements(path, package):
	path 	= osp.realpath(path)
	
	content = read(path)
		
	try:
		pattern = r"{package}(=={version})*".format(
			package = re.escape(package.name),
			version = re.escape(package.current_version)
		)
		lines   = content.splitlines()
		nlines  = len(lines)
		
		with open(path, "w") as f:
			for i, line in enumerate(lines):
				if re.search(pattern, line, flags = re.IGNORECASE):
					line = line.replace(
						"==%s" % package.current_version,
						"==%s" % package.latest_version
					)
					
				f.write(line)

				if i < nlines - 1:
					f.write("\n")
	except Exception:
		# In case we fucked up!
		write(path, content, force = True)

def update_pipfile(pipfile, verbose = False):
	if not verbose:
		logger.setLevel(log.NOTSET)

	realpath = osp.realpath(pipfile)
	basepath = osp.dirname(realpath)

	logger.info("Searching for `pipenv`...")
	pipenv   = which("pipenv", raise_err = True)
	logger.info("`pipenv` found.")

	code     = popen("%s update" % pipenv, quiet = not verbose, cwd = basepath)

	return code == 0

def get_registry_from_requirements(requirements, sync = False):
	path = osp.realpath(requirements)

	if not osp.exists(path):
		cli.echo(cli_format("{} not found.".format(path), cli.RED))
		sys.exit(os.EX_NOINPUT)
	else:
		packages =  _pip.parse_requirements(requirements, session = "hack")
		registry = Registry(source = path, packages = packages, sync = sync)

	logger.info("Packages within requirements %s found: %s..." % (requirements, registry.packages))

	return registry

def get_registry_from_pip(pip_path, sync = False):
	_, output, _ = _pip.call("list", outdated = True, \
		format = "json", pip_exec = pip_path, output = True)
	packages     = json.loads(output)
	registry     = Registry(source = pip_path, packages = packages,
		installed = True, sync = sync)

	logger.info("Packages within `pip` %s found: %s..." % (pip_path, registry.packages))
	# _pip.get_installed_distributions() # https://github.com/achillesrasquinha/pipupgrade/issues/13

	return registry

def update_registry(registry,
	yes         = False,
	user 		= False,
	check	    = False,
	latest		= False,
	interactive = False,
	verbose 	= False):
	source   = registry.source
	packages = registry.packages

	table 	 = Table(header = ["Name", "Current Version", "Latest Version", "Home Page"])
	dinfo 	 = [ ] # Information DataFrame

	for package in packages:
		package.source    = source
		package.installed = registry.installed

		if package.latest_version and package.current_version != package.latest_version:
			diff_type = None
			
			try:
				diff_type = semver.difference(package.current_version, package.latest_version)
			except (TypeError, ValueError):
				pass

			table.insert([
				cli_format(package.name, _SEMVER_COLOR_MAP.get(diff_type, cli.CLEAR)),
				package.current_version or "na",
				_cli_format_semver(package.latest_version, diff_type),
				cli_format(package.home_page, cli.CYAN)
			])

			package.diff_type = diff_type

			dinfo.append(package)

		if not registry.installed:
			_update_requirements(package.source, package)

	stitle = "Installed Distributions (%s)" % source if registry.installed else source

	if not table.empty:
		string = table.render()
	
		cli.echo("\nSource: %s\n" % stitle)
		
		if not interactive:
			cli.echo(string)
			cli.echo()

		if not check:
			packages  = [p for p in dinfo if p.diff_type != "major" or latest]
			npackages = len(packages)

			spackages = pluralize("package", npackages) # Packages "string"
			query     = "Do you wish to update %s %s?" % (npackages, spackages)

			if npackages and (yes or interactive or cli.confirm(query, quit_ = True)):
				for i, package in enumerate(packages):
					update = True
					
					query  = "%s (%s > %s)" % (
						cli_format(package.name, _SEMVER_COLOR_MAP.get(package.diff_type, cli.CLEAR)),
						package.current_version,
						_cli_format_semver(package.latest_version, package.diff_type)
					)

					if interactive:
						update = yes or cli.confirm(query)
						
					if update:
						cli.echo(cli_format(
							"Updating %s of %s %s: %s" % (
								i + 1,
								npackages,
								spackages,
								cli_format(package.name, cli.GREEN)
							)
						, cli.BOLD))

						_pip.call("install", package.name, pip_exec = package.source, user = user, quiet = not verbose, no_cache_dir = True, upgrade = True)

						if not package.installed:
							_update_requirements(package.source, package)
	else:
		cli.echo("%s upto date." % cli_format(stitle, cli.CYAN))