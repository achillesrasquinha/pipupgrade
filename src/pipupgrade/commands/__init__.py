# imports - compatibility imports
from __future__ import absolute_import
import os.path as osp

# imports - standard imports
import json
from   functools import partial
import traceback

# imports - module imports
from pipupgrade.commands.helper import (
    get_registry_from_requirements,
    get_registry_from_pip,
    update_pip,
    update_pipfile,
    update_registry,
    _DEPENDENCY_FORMATS
)
from pipupgrade.model           import Project
from pipupgrade.model.project 	import get_included_requirements
from pipupgrade.commands.util 	import cli_format
from bpyutils.util.array    	import flatten, sequencify
from bpyutils.util._dict        import merge_dict
from bpyutils.util.system   	import (touch, popen, which, remove)
from bpyutils.util.environ  	import getenvvar
from bpyutils.util.datetime 	import get_timestamp_str
from bpyutils.util.imports      import import_handler
from pipupgrade 		      	import _pip, cli
from bpyutils._compat			import builtins, iteritems
from pipupgrade.__attr__      	import __name__ as NAME
from bpyutils.config			import environment, get_config_path
from pipupgrade.exception       import DependencyNotFoundError

from bpyutils import request as req
from bpyutils import parallel, log

logger   = log.get_logger(level = log.DEBUG)

ARGUMENTS = dict(
    packages					= [ ],
    resolve                     = False,
    ignore						= [ ],
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
    upgrade_type				= ("minor", "patch"),
    latest						= False,
    format						= "table",
    all							= False,
    pip							= False,
    self 		 				= False,
    jobs						= 1,
    user		 				= False,
    check		 				= False,
    interactive  				= False,
    yes			 				= False,
    no_included_requirements 	= False,
    no_cache		            = False,
    no_color 	 				= True,
    output						= None,
    ignore_error				= False,
    force						= False,
    doctor                      = False,
    clean                       = False,
    verbose		 				= False
)

@cli.command
def command(**ARGUMENTS):
    try:
        return _command(**ARGUMENTS)
    except Exception as e:
        if not isinstance(e, DependencyNotFoundError):
            cli.echo()

            traceback_str = traceback.format_exc()
            cli.echo(traceback_str)

            cli.echo(cli_format("""\
An error occured while performing the above command. This could be an issue with
"pipupgrade". Kindly post an issue at https://github.com/achillesrasquinha/pipupgrade/issues""", cli.RED))
        else:
            raise e

def to_params(kwargs):
    class O(object):
        pass

    params = O()

    kwargs = merge_dict(ARGUMENTS, kwargs)

    for k, v in iteritems(kwargs):
        setattr(params, k, v)

    return params

def import_or_raise(package, name = None):
    name = name or package

    try:
        import_handler(package)
    except ImportError:
        raise DependencyNotFoundError((
            "Unable to import {package} for resolving dependencies. "
            "pipupgrade requires {package} to be installed. "
            "Please install {package} by executing 'pip install {name}'."
        ).format(package = package, name = name))

def _command(*args, **kwargs):
    a = to_params(kwargs)

    if not a.verbose:
        logger.setLevel(log.NOTSET)

    logger.info("Environment: %s" % environment())
    logger.info("Arguments Passed: %s" % locals())

    if a.doctor:
        logger.info("Performing Diagnostics and attempting to fix.")

        if a.clean:
            path_config = get_config_path(name = NAME)
            paths = [
                osp.join(path_config, "db.db")
            ]

            for path in paths:
                remove(path)

        # check database and repair.
    else:
        if a.resolve:
            import_or_raise("mixology")
            import_or_raise("semver", name = "poetry-semver")

            populate_db = import_handler("pipupgrade.pubgrub.populate_db")
            populate_db()

        file_ = a.output

        if file_:
            logger.info("Writing to output file %s..." % file_)
            touch(file_)

        cli.echo(cli_format("Checking...", cli.YELLOW), file = file_)

        pip_path    = a.pip_path or [ ]
        pip_path    = [which(p) for p in pip_path] or _pip._PIP_EXECUTABLES

        logger.info("`pip` executables found: %s" % pip_path)
        
        logger.info("Using %s jobs..." % a.jobs)

        registries  = [ ]

        if a.pip:
            logger.info("Updating pip executables: %s" % " ".join(pip_path))

            with parallel.no_daemon_pool(processes = a.jobs) as pool:
                pool.imap_unordered(
                    partial(
                        update_pip, **{ "user": a.user, "quiet": not a.verbose,
                            "file": file_ }
                    ),
                    pip_path
                )

        if a.self:
            package = NAME
            logger.info("Updating %s..." % package)

            cli.echo(cli_format("Updating %s..." % package, cli.YELLOW),
                file = file_)

            _pip.call("install", package, user = a.user, quiet = not a.verbose,
                no_cache = True, upgrade = True, output = file_)

            cli.echo("%s upto date." % cli_format(package, cli.CYAN),
                file = file_)
        else:
            requirements = sequencify(a.requirements or [])
            pipfile      = sequencify(a.pipfile or [])
            
            if a.project:
                project	 = sequencify(a.project)

                logger.info("Detecting projects and its dependencies...")
                
                with parallel.no_daemon_pool(processes = a.jobs) as pool:
                    project       = pool.imap_unordered(
                        partial(
                            Project.from_path,
                            **{ "depth_search": a.force }
                        ),
                        project
                    )

                    requirements += flatten(map(lambda p: p.requirements, project))
                    pipfile      += flatten(map(lambda p: [p.pipfile] if p.pipfile else [], project))
                
                logger.info("Updating projects %s..." % project)

            if requirements:
                logger.info("Detecting requirements...")

                if not a.no_included_requirements:
                    with parallel.no_daemon_pool(processes = a.jobs) as pool:
                        results       = pool.imap_unordered(get_included_requirements,
                            requirements)
                        requirements += flatten(results)

                    requirements = list(set(requirements))

                logger.info("Requirements found: %s" % requirements)
                
                with parallel.no_daemon_pool(processes = a.jobs) as pool:
                    results       = pool.imap_unordered(
                        partial(
                            get_registry_from_requirements,
                            **{ "sync": a.no_cache, "jobs": a.jobs,
                                "only_packages": a.packages, "file": file_,
                                "ignore_packages": a.ignore, "resolve": a.resolve,
                                "latest": a.latest
                            }
                        ),
                        requirements
                    )
                    registries    += results
            else:
                with parallel.no_daemon_pool(processes = a.jobs) as pool:
                    for registry in pool.imap_unordered(
                        partial(
                            get_registry_from_pip,
                            **{ "user": a.user, "sync": a.no_cache,
                                "outdated": not a.all,
                                "build_dependency_tree": a.format in _DEPENDENCY_FORMATS,
                                "jobs": a.jobs, "only_packages": a.packages,
                                "ignore_packages": a.ignore, "resolve": a.resolve,
                                "latest": a.latest
                            }
                        ),
                        pip_path
                    ):
                        registries.append(registry)

            logger.info("Updating registries: %s..." % registries)

            for registry in registries:
                update_registry(registry, yes = a.yes, user = a.user, check = a.check,
                    latest = a.latest, interactive = a.interactive, verbose = a.verbose,
                    format_ = a.format, all = a.all, filter_ = a.packages,
                    file = file_, raise_err = not a.ignore_error,
                    upgrade_type = a.upgrade_type
                )

            if pipfile:
                logger.info("Updating Pipfiles: %s..." % pipfile)

                cli.echo(cli_format("Updating Pipfiles: %s..." % ", ".join(pipfile), cli.YELLOW),
                    file = file_)

                with parallel.no_daemon_pool(processes = a.jobs) as pool:
                    results = pool.imap_unordered(
                        partial(
                            update_pipfile,
                            **{ "verbose": a.verbose }
                        ),
                        pipfile
                    )

                    if builtins.all(results):
                        cli.echo(cli_format("Pipfiles upto date.", cli.GREEN),
                            file = file_)

            if a.project and a.pull_request:
                errstr = '%s not found. Use %s or the environment variable "%s" to set value.'

                if not a.git_username:
                    raise ValueError(errstr % ("Git Username", "--git-username", getenvvar("GIT_USERNAME")))
                if not a.git_email:
                    raise ValueError(errstr % ("Git Email",    "--git-email",    getenvvar("GIT_EMAIL")))
                
                for p in project:
                    popen("git config user.name  %s" % a.git_username, cwd = p.path)
                    popen("git config user.email %s" % a.git_email,    cwd = p.path)

                    _, output, _ = popen("git status -s", output = True,
                        cwd = p.path)

                    if output:
                        branch   = get_timestamp_str(format_ = "%Y%m%d%H%M%S")
                        popen("git checkout -B %s" % branch, quiet = not a.verbose,
                            cwd = p.path
                        )

                        title    = "fix(dependencies): Update dependencies to latest"
                        body     = ""

                        # TODO: cross-check with "git add" ?
                        files    = p.requirements + [p.pipfile]
                        popen("git add %s" % " ".join(files), quiet = not a.verbose,
                            cwd = p.path)
                        popen("git commit -m '%s'" % title, quiet = not a.verbose,
                            cwd = p.path)

                        popen("git push origin %s" % branch, quiet = not a.verbose,
                            cwd = p.path)

                        if not a.github_reponame:
                            raise ValueError(errstr % ("GitHub Reponame", "--github-reponame", getenvvar("GITHUB_REPONAME")))
                        if not a.github_username:
                            raise ValueError(errstr % ("GitHub Username", "--github-username", getenvvar("GITHUB_USERNAME")))

                        url       = "/".join(["https://api.github.com", "repos", a.github_username, a.github_reponame, "pulls"])
                        headers   = dict({
                            "Content-Type": "application/json",
                            "Authorization": "token %s" % a.github_access_token
                        })
                        data      = dict(
                            head  = "%s:%s" % (a.git_username, branch),
                            base  = a.target_branch,
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

                            url      = "/".join(map(str, ["https://github.com", a.github_username, a.github_reponame, "pull", number]))
                            message  = "Created a Pull Request at %s" % url

                            cli.echo(cli_format(message, cli.GREEN), file = file_)
                        else:
                            response.raise_for_status()
