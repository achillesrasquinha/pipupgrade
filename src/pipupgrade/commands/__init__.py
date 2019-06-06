# imports - standard imports
import sys, os, os.path as osp
import re
import json
import multiprocessing as mp
from   functools import partial

# imports - module imports
from pipupgrade.helper 			import (
	get_registry_from_requirements,
	get_registry_from_pip,
	update_pipfile
)
from pipupgrade.model         	import Project, Package, Registry
from pipupgrade.model.project 	import get as get_project, get_included_requirements
from pipupgrade.commands.util 	import cli_format
from pipupgrade.table      	  	import Table
from pipupgrade.util.types    	import flatten
from pipupgrade.util.string   	import strip, pluralize
from pipupgrade.util.system   	import read, write, popen, which
from pipupgrade.util.environ  	import getenvvar
from pipupgrade.util.datetime 	import get_timestamp_str
from pipupgrade 		      	import (_pip, request as req, cli, semver,
	log, parallel
)
from pipupgrade.__attr__      	import __name__

logger = log.get_logger(level = log.DEBUG)

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

@cli.command
def command(
	pip_path            = [ ],
	requirements 		= [ ],
	pipfile             = [ ],
	project      		= None,
	pull_request 		= False,
	git_username 		= None,
	git_email    		= None,
	github_access_token = None,
	github_reponame     = None,
	github_username     = None,
	target_branch       = "master",
	latest				= False,
	self 		 		= False,
	jobs				= 1,
	user		 		= False,
	check		 		= False,
	interactive  		= False,
	yes			 		= False,
	no_cache            = False,
	no_color 	 		= True,
	verbose		 		= False
):
	if not verbose:
		logger.setLevel(log.NOTSET)
		
	cli.echo(cli_format("Checking...", cli.YELLOW))
	logger.info("Arguments Passed: %s" % locals())

	pip_path    = pip_path or [ ]
	pip_path    = [which(p) for p in pip_path] or _pip._PIP_EXECUTABLES

	logger.info("`pip` executables found: %s" % pip_path)

	registries  = [ ]

	logger.info("Using %s jobs..." % jobs)

	if self:
		package = __name__
		logger.info("Updating %s..." % package)

		_pip.call("install", package, user = user, quiet = not verbose, no_cache = True, upgrade = True)
		cli.echo("%s upto date." % cli_format(package, cli.CYAN))
	else:
		if project:
			requirements = requirements or [ ]
			pipfile      = pipfile      or [ ]

			logger.info("Detecting Projects and its dependencies...")
			
			with parallel.pool(processes = jobs) as pool:
				project       = pool.map(get_project, project)
				requirements += flatten(map(lambda p: p.requirements, project))
				pipfile      += flatten(map(lambda p: [p.pipfile], project))
			
			logger.info("Updating projects %s..." % project)

		if requirements:
			logger.info("Detecting requirements...")
			
			with parallel.pool(processes = jobs) as pool:
				results       = pool.map(get_included_requirements, requirements)
				requirements += flatten(results)

			# cli.echo(cli_format("{} not found.".format(path), cli.RED))
			# sys.exit(os.EX_NOINPUT)

			logger.info("Requirements found: %s..." % requirements)
			
			with parallel.pool(processes = jobs) as pool:
				results       = pool.map(
					partial(
						get_registry_from_requirements,
						**{ "sync": no_cache, "verbose": verbose }
					),
					requirements
				)
				registries    += results
		else:
			with parallel.pool(processes = jobs) as pool:
				results       = pool.map(
					partial(
						get_registry_from_pip,
						**{ "sync": no_cache, "verbose": verbose }
					),
					pip_path
				)
				registries    += results

		for registry in registries:
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

		if pipfile:
			logger.info("Updating Pipfiles: %s..." % pipfile)

			with parallel.pool(processes = jobs) as pool:
				results = pool.map(
					partial(
						update_pipfile,
						**{ "verbose": verbose }
					),
					pipfile
				)

				if all(results):
					cli.echo("Pipfiles upto date.", cli.CYAN)

		if project and pull_request:
			errstr = '%s not found. Use %s or the environment variable "%s" to set value.'

			if not git_username:
				raise ValueError(errstr % ("Git Username", "--git-username", getenvvar("GIT_USERNAME")))
			if not git_email:
				raise ValueError(errstr % ("Git Email",    "--git-email",    getenvvar("GIT_EMAIL")))
			
			for p in project:
				popen("git config user.name  %s" % git_username, cwd = p.path)
				popen("git config user.email %s" % git_email,    cwd = p.path)

				_, output, _ = popen("git status -s", output = True)

				if output:
					branch   = get_timestamp_str(format_ = "%Y%m%d%H%M%S")
					popen("git checkout -B %s" % branch, quiet = not verbose)

					title    = "fix(dependencies): Update dependencies to latest"
					body     = ""

					# TODO: cross-check with "git add" ?
					files    = p.requirements + [p.pipfile]
					popen("git add %s" % " ".join(files), quiet = not verbose, cwd = p.path)
					popen("git commit -m '%s'" % title, quiet = not verbose, cwd = p.path)

					popen("git push origin %s" % branch, quiet = not verbose, cwd = p.path)

					if not github_reponame:
						raise ValueError(errstr % ("GitHub Reponame", "--github-reponame", getenvvar("GITHUB_REPONAME")))
					if not github_username:
						raise ValueError(errstr % ("GitHub Username", "--github-username", getenvvar("GITHUB_USERNAME")))

					url       = "/".join(["https://api.github.com", "repos", github_username, github_reponame, "pulls"])
					headers   = dict({
						 "Content-Type": "application/json",
						"Authorization": "token %s" % github_access_token
					})
					data      = dict(
						head  = "%s:%s" % (git_username, branch),
						base  = target_branch,
						title = title,
						body  = body
					)
					
					# Although there's monkey patch support for the "requests"
					# library, avoid using the "json" parameter which was
					# added in requests 2.4.2+
					response  = req.post(url, data = json.dumps(data), headers = headers)

					if response.ok:
						response = response.json()
						number   = response["number"]

						url      = "/".join(map(str, ["https://github.com", github_username, github_reponame, "pull", number]))
						message  = "Created a Pull Request at %s" % url

						cli.echo(cli_format(message, cli.GREEN))
					else:
						response.raise_for_status()