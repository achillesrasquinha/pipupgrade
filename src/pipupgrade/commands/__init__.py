# imports - standard imports
import sys, os, os.path as osp
import re
import json
import multiprocessing as mp
from   functools import partial

# imports - module imports
from pipupgrade.commands.helper import (
	get_registry_from_requirements,
	get_registry_from_pip,
	update_pipfile,
	update_registry
)
from pipupgrade.model           import Project
from pipupgrade.model.project 	import get_included_requirements
from pipupgrade.commands.util 	import cli_format
from pipupgrade.util.types    	import flatten
from pipupgrade.util.system   	import read, write, popen, which
from pipupgrade.util.environ  	import getenvvar
from pipupgrade.util.datetime 	import get_timestamp_str
from pipupgrade 		      	import (_pip, request as req, cli,
	log, parallel
)
from pipupgrade.__attr__      	import __name__

logger = log.get_logger(level = log.DEBUG)

@cli.command
def command(
	pip_path          		 	= [ ],
	requirements 				= [ ],
	pipfile            			= [ ],
	project      				= None,
	pull_request 				= False,
	git_username 				= None,
	git_email    				= None,
	github_access_token			= None,
	github_reponame   		 	= None,
	github_username   			= None,
	target_branch    			= "master",
	latest						= False,
	self 		 				= False,
	jobs						= 1,
	user		 				= False,
	check		 				= False,
	interactive  				= False,
	yes			 				= False,
	no_included_requirements 	= False,
	no_cache		            = False,
	no_color 	 				= True,
	verbose		 				= False
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

		cli.echo(cli_format("Updating %s..." % package, cli.YELLOW))

		_pip.call("install", package, user = user, quiet = not verbose,
			no_cache = True, upgrade = True)
		cli.echo("%s upto date." % cli_format(package, cli.CYAN))
	else:
		if project:
			requirements = requirements or [ ]
			pipfile      = pipfile      or [ ]

			logger.info("Detecting projects and its dependencies...")
			
			with parallel.pool(processes = jobs) as pool:
				project       = pool.map(Project.from_path, project)
				requirements += flatten(map(lambda p: p.requirements, project))
				pipfile      += flatten(map(lambda p: [p.pipfile], project))
			
			logger.info("Updating projects %s..." % project)

		if requirements:
			logger.info("Detecting requirements...")

			if not no_included_requirements:
				with parallel.pool(processes = jobs) as pool:
					results       = pool.map(get_included_requirements, requirements)
					requirements += flatten(results)

			logger.info("Requirements found: %s" % requirements)
			
			with parallel.pool(processes = jobs) as pool:
				results       = pool.map(
					partial(
						get_registry_from_requirements,
						**{ "sync": no_cache }
					),
					requirements
				)
				registries    += results
		else:
			with parallel.pool(processes = jobs) as pool:
				results       = pool.map(
					partial(
						get_registry_from_pip,
						**{ "sync": no_cache }
					),
					pip_path
				)
				registries    += results

		if yes:
			with parallel.pool(processes = jobs) as pool:
				results = pool.map(
					partial(
						update_registry,
						**{ "yes": yes, "user": user, "check": check,
							"latest": latest, "interactive": interactive,
							"verbose": verbose }
					),
					registries
				)
		else:
			for registry in registries:
				update_registry(registry, yes = yes, user = user, check = check,
					latest = latest, interactive = interactive, verbose = verbose
				)

		if pipfile:
			logger.info("Updating Pipfiles: %s..." % pipfile)

			cli.echo(cli_format("Updating Pipfiles: %s..." % ", ".join(pipfile), cli.YELLOW))

			with parallel.pool(processes = jobs) as pool:
				results = pool.map(
					partial(
						update_pipfile,
						**{ "verbose": verbose }
					),
					pipfile
				)

				if all(results):
					cli.echo(cli_format("Pipfiles upto date.", cli.GREEN))

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
