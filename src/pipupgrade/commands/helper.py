# imports - compatibility imports
from __future__ import absolute_import

# imports - standard imports
import sys, os, os.path as osp
import re
import json

# imports - module imports
from pipupgrade.model         	import Registry
from pipupgrade.commands.util 	import cli_format
from bpyutils.table      	  	import Table
from bpyutils.util.string     	import pluralize, strip
from bpyutils.util.system   	import read, write, popen, which
from bpyutils.util.array		import squash
from pipupgrade 		      	import _pip, cli, semver
from bpyutils.exception			import PopenError

from bpyutils import parallel, log

logger = log.get_logger()

_SEMVER_COLOR_MAP 	= dict(
	major = cli.RED,
	minor = cli.YELLOW,
	patch = cli.GREEN
)
_DEPENDENCY_FORMATS = ("tree", "json", "yaml")

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
					current_version = package.current_version

					if current_version:
						current_version = package.current_version.replace("==", "")

					line = line.replace(
						"==%s" % current_version,
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
	pipenv   = which("pipenv")

	if not pipenv:
		logger.info("Attempting to install pipenv...")

		_pip.call("install", "pipenv")

		pipenv = which("pipenv", raise_err = True)

	logger.info("`pipenv` found.")

	code     = popen("%s update" % pipenv, quiet = not verbose, cwd = basepath)

	return code == 0

def _format_package(package):
	difference = None
	
	try:
		difference = semver.difference(package.current_version,
			package.latest_version)
	except (TypeError, ValueError):
		pass

	string = "* %s" % cli_format(package.name, _SEMVER_COLOR_MAP.get(difference, cli.CLEAR))

	if getattr(package, "has_dependency_conflict", False):
		string += cli_format(" [dependency conflict]", cli.RED)

	if package.current_version:
		string += " (%s)" % package.current_version

	if package.latest_version and package.current_version != package.latest_version:
		string += " -> (%s)" % _cli_format_semver(package.latest_version, difference)

	string += " " + cli_format("[%s]" % package.home_page, cli.CYAN)

	return string

def _render_dependency_tree(packages):
	rendered = [ ]

	for package in packages:
		dependencies 	= package.dependency_tree
		string			= dependencies.render(indent = 4,
			formatter = lambda package: _format_package(package)
		)

		sanitized		= strip(string)
		
		rendered.append(sanitized)

	string = strip("\n".join(rendered))

	return string

def _render_json(packages):
	dicts = [ ]

	for package in packages:
		dict_ = package.to_dict()
		dicts.append(dict_)
		
	return dicts

def _render_yaml(packages):
	try:
		import yaml

		content = _render_json(packages)
		dict_   = dict()

		for details in content:
			name = details.pop("name")
			dict_[name] = details

		string  = strip(yaml.safe_dump(dict_))

		return string
	except ImportError:
		raise ValueError((
			"Unable to import yaml. "
			"Please install pyyaml. https://github.com/yaml/pyyaml."
		))

def _resolve_dependencies(nodes):
	for i, node in enumerate(nodes):
		deptree = node.dependency_tree
		found 	= deptree.find(
			lambda x: x.parent != None and x.obj.difference == "major"
		)

		if found:
			nodes[i].has_dependency_conflict = True
	
	return nodes

def update_registry(registry,
	yes         	= False,
	user 			= False,
	check	    	= False,
	latest			= False,
	interactive 	= False,
	format_			= "table",
	all				= False,
	filter_			= [ ],
	file			= None,
	raise_err		= True,
	verbose 		= False,
	upgrade_type 	= ("minor", "patch")
):
	source   = registry.source
	packages = registry.packages

	if filter_:
		packages = [p for p in packages if p.name in filter_]
	
	table 	 = Table(header = ["Name", "Current Version", "Latest Version",
		"Home Page"])
	nodes	 = [ ]
	render   = False
	dinfo 	 = [ ] # Information DataFrame

	for package in packages:
		package.source    	= source
		package.installed 	= registry.installed
		
		current_version		= package.current_version
		
		if all or current_version:
			current_version = current_version.replace("==", "")

		if all or (package.latest_version and current_version != package.latest_version):
			render	  = True

			if format_ in _DEPENDENCY_FORMATS:
				nodes.append(package)
			else:
				table.insert([
					cli_format(package.name, _SEMVER_COLOR_MAP.get(package.difference, cli.CLEAR)),
					package.current_version or "na",
					_cli_format_semver(package.latest_version, package.difference),
					cli_format(package.home_page, cli.CYAN)
				])

			dinfo.append(package)

	stitle = "Installed Distributions (%s)" % source if registry.installed else source
	
	if render:
		if format_ in _DEPENDENCY_FORMATS:
			nodes  = _resolve_dependencies(nodes)
			dinfo  = nodes

		if 	 format_ == "tree":
			string = _render_dependency_tree(nodes)
		elif format_ == "json":
			string = _render_json(nodes)
		elif format_ == "yaml":
			string = _render_yaml(nodes)
		elif format_ == "table":
			string = table.render()
	
		cli.echo("\nSource: %s\n" % stitle, file = file)
		
		if not interactive or check:
			cli.echo(string, file = file)
			cli.echo(file = file)

		if not check:
			packages  = [p for p in dinfo if p.difference in upgrade_type
				or p.difference == "major"]
			packages  = [p for p in dinfo if p.difference != "major" 
				or getattr(p, "has_dependency_conflict", False) or latest]

			npackages = len(packages)

			spackages = pluralize("package", npackages) # Packages "string"
			query     = "Do you wish to update %s %s?" % (npackages, spackages)

			if npackages and (yes or interactive or cli.confirm(query, quit_ = True)):
				for i, package in enumerate(packages):
					update = True
					
					query  = "%s (%s) -> (%s)" % (
						cli_format(package.name, _SEMVER_COLOR_MAP.get(package.difference, cli.CLEAR)),
						package.current_version,
						_cli_format_semver(package.latest_version, package.difference)
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
						, cli.BOLD), file = file)

						if not package.installed:
							_update_requirements(package.source, package)
						else:
							try:
								_pip.call("install", package.name,
									pip_exec = package.source, user = user,
									quiet = not verbose, no_cache_dir = True,
									upgrade = True
								)
							except PopenError as e:
								if raise_err:
									raise
	else:
		cli.echo("%s upto date." % cli_format(stitle, cli.CYAN),
			file = file)

def get_registry_from_pip(pip_path, user = False, sync = False, outdated = True,
	build_dependency_tree = False, resolve = False, jobs = 1, only_packages = [ ],
	ignore_packages = [ ], latest = False
):
	logger.info("Fetching installed packages for %s..." % pip_path)

	_, output, _ = _pip.call("list", user = user, outdated = outdated, \
		format = "json", pip_exec = pip_path, output = True)

	packages     = json.loads(output)
	logger.info("%s packages found for %s." % (len(packages), pip_path))

	if only_packages:
		packages = [p for p in packages if p["name"] in only_packages]

	if ignore_packages:
		packages = [p for p in packages if p["name"] not in ignore_packages]
	
	registry     = Registry(source = pip_path, packages = packages,
		installed = True, sync = sync,
		build_dependency_tree = build_dependency_tree, 
		resolve = resolve, jobs = jobs, latest = latest)

	logger.info("Packages within `pip` %s found: %s..." % (pip_path, registry.packages))
	# _pip.get_installed_distributions() # https://github.com/achillesrasquinha/pipupgrade/issues/13

	return registry

def get_registry_from_requirements(requirements, sync = False, jobs = 1,
	only_packages = [ ], resolve = False, file = None, ignore_packages = [ ],
    latest = False):
	path = osp.realpath(requirements)

	if not osp.exists(path):
		cli.echo(cli_format("{} not found.".format(path), cli.RED),
			file = file)
		sys.exit(os.EX_NOINPUT)
	else:
		packages =  _pip.parse_requirements(requirements, session = "hack")
		
		if only_packages:
			packages = [p for p in packages if p.name in only_packages]

		if ignore_packages:
			packages = [p for p in packages if p["name"] not in ignore_packages]

		registry = Registry(source = path, packages = packages, sync = sync,
			resolve = resolve, jobs = jobs, latest = latest
		)

	logger.info("Packages within requirements %s found: %s..." % (
		requirements, registry.packages)
	)

	return registry

def pip_upgrade(package, pip_exec = None, user = None, quiet = None):
	return _pip.call("install", package, pip_exec = pip_exec, 
		user = user, quiet = quiet, no_cache_dir = True, upgrade = True)

def update_pip(pip_exec, user = None, quiet = None, file = None):
	cli.echo(cli_format("Updating %s..." % pip_exec, cli.YELLOW),
		file = file)

	output = pip_upgrade("pip", pip_exec = pip_exec, user = user, quiet = quiet)

	if isinstance(output, int):
		code = output
	else:
		code = output[0]

	if not code:
		cli.echo("%s upto date." % cli_format(pip_exec, cli.CYAN),
			file = file)

	return output
