<div align="center">
    <h1>
        pipupgrade
    </h1>
    <h4>The missing command for <code>pip</code></h4>
    <div align="center">
        <img src=".github/assets/demo.gif">
    </div>
</div>

<p align="center">
    <a href="https://travis-ci.org/achillesrasquinha/pipupgrade">
        <img src="https://img.shields.io/travis/achillesrasquinha/pipupgrade.svg?style=flat-square">
    </a>
    <a href="https://ci.appveyor.com/project/achillesrasquinha/pipupgrade">
        <img src="https://img.shields.io/appveyor/ci/achillesrasquinha/pipupgrade.svg?style=flat-square&logo=appveyor">
    </a>
    <a href="https://coveralls.io/github/achillesrasquinha/pipupgrade">
        <img src="https://img.shields.io/coveralls/github/achillesrasquinha/pipupgrade.svg?style=flat-square">
    </a>
    <a href="https://pypi.org/project/pipupgrade/">
		<img src="https://img.shields.io/pypi/v/pipupgrade.svg?style=flat-square">
	</a>
    <a href="https://pypi.org/project/pipupgrade/">
		<img src="https://img.shields.io/pypi/l/pipupgrade.svg?style=flat-square">
	</a>
    <a href="https://pypi.org/project/pipupgrade/">
		<img src="https://img.shields.io/pypi/pyversions/pipupgrade.svg?style=flat-square">
	</a>
    <a href="https://hub.docker.com/r/achillesrasquinha/pipupgrade">
		<img src="https://img.shields.io/docker/build/achillesrasquinha/pipupgrade.svg?style=flat-square&logo=docker">
	</a>
    <a href="https://git.io/boilpy">
      <img src="https://img.shields.io/badge/made%20with-boilpy-red.svg?style=flat-square">
    </a>
	<a href="https://saythanks.io/to/achillesrasquinha">
		<img src="https://img.shields.io/badge/Say%20Thanks-🦉-1EAEDB.svg?style=flat-square">
	</a>
	<a href="https://paypal.me/achillesrasquinha">
		<img src="https://img.shields.io/badge/donate-💵-f44336.svg?style=flat-square">
	</a>
</p>

### Table of Contents
* [Features](#Features)
* [Installation](#installation)
* [Usage](#usage)
* [License](#license)

#### Features
* Updates system packages and local packages.
* Discovers packages present within multiple Python Environments.
* Updates packages mentioned within a `requirements.txt` file (Also pins up-to-date versions if mentioned).
* Smart `requirements.txt` detector.
* [Pipfile](https://github.com/pypa/pipenv) support.
* Detects semantic version to avoid updates that break changes.
* Parallel updates (blazingly fast).
* Python 2.7+ and Python 3.4+ compatible. Also pip 9+, pip 10+, pip 18+ and [pip 19.0.1+](https://github.com/pypa/pip/issues/6158) compatible.
* Automate your Dependencies by installing `pipupgrade` in your CI workflow.
* Zero Dependencies!

#### Installation

```shell
$ pip install pipupgrade
```

#### Usage

##### Basic Usage

* [**`pipupgrade`**](https://git.io/pipupgrade)

*Upgrades all the packages across all detected pip environments.*

* [**`pipupgrade --self`**](https://git.io/pipupgrade)

*Upgrades `pipupgrade`.*

* [**`pipupgrade --pip-path PIP_PATH`**](https://git.io/pipupgrade)

*Upgrades all the packages within the defined pip environment.*

* [**`pipupgrade --check`**](https://git.io/pipupgrade)

*Checks and pretty prints outdated packages (Does not perform upgrades).*

* [**`pipupgrade --latest`**](https://git.io/pipupgrade)

*WARNING: Upgrades all packages (including the ones that break change).*

* [**`pipupgrade --interactive`**](https://git.io/pipupgrade)

*Prompts confirmation dialog for each package to be upgraded.*

* [**`pipupgrade --requirements REQUIREMENTS`**](https://git.io/pipupgrade)

*Upgrades the requirements file (if required).*

* [**`pipupgrade --pipfile PIPFILE`**](https://git.io/pipupgrade)

*Upgrades the Pipfile and Pipfile.lock file (if required).*

* [**`pipupgrade --project PROJECT`**](https://git.io/pipupgrade)

*Upgrades all the requirements file and/or Pipfile/Pipfile.lock within a project directory.*

That's basically it! Run the help for more details...

```
$ pipupgrade --help
usage: pipupgrade [--pip-path PIP_PATH] [-y] [-c] [-l] [-s] [-r REQUIREMENTS]
                  [--pipfile PIPFILE] [-i] [-p PROJECT]
                  [--git-username GIT_USERNAME] [--git-email GIT_EMAIL]
                  [--pull-request] [--github-access-token GITHUB_ACCESS_TOKEN]
                  [--github-reponame GITHUB_REPONAME]
                  [--github-username GITHUB_USERNAME]
                  [--target-branch TARGET_BRANCH] [-j JOBS] [-u]
                  [--no-included-requirements] [--no-cache] [--no-color] [-V]
                  [-v] [-h]

pipupgrade (v 1.5.1)

UPGRADE ALL THE PIP PACKAGES!

optional arguments:
  --pip-path PIP_PATH   Path to pip executable to be used. (default: None)
  -y, --yes             Confirm for all dialogs. (default: False)
  -c, --check           Check for outdated packages. (default: False)
  -l, --latest          Update all packages to latest. (default: False)
  -s, --self            Update pipupgrade. (default: False)
  -r REQUIREMENTS, --requirements REQUIREMENTS
                        Path(s) to requirements.txt file. (default: None)
  --pipfile PIPFILE     Path(s) to Pipfile (default: None)
  -i, --interactive     Interactive Mode (default: False)
  -p PROJECT, --project PROJECT
                        Path(s) to Project (default: None)
  --git-username GIT_USERNAME
                        Git Username (default: None)
  --git-email GIT_EMAIL
                        Git Email (default: None)
  --pull-request        Perform a Pull Request (default: False)
  --github-access-token GITHUB_ACCESS_TOKEN
                        GitHub Access Token (default: None)
  --github-reponame GITHUB_REPONAME
                        Target GitHub Repository Name (default: None)
  --github-username GITHUB_USERNAME
                        Target GitHub Username (default: None)
  --target-branch TARGET_BRANCH
                        Target Branch (default: master)
  -j JOBS, --jobs JOBS  Number of Jobs to be used. (default: 4)
  -u, --user            Install to the Python user install directory for
                        environment variables and user configuration.
                        (default: False)
  --no-included-requirements
                        Avoid updating included requirements (default: False)
  --no-cache            Avoid fetching latest updates from PyPI server.
                        (default: False)
  --no-color            Avoid colored output. (default: False)
  -V, --verbose         Display verbose output. (default: False)
  -v, --version         Show pipupgrade's version number and exit.
  -h, --help            Show this help message and exit.
```

#### Similar Packages

`pipupgrade` attempts to provide an all-in-one solution as compared to the following packages:

* [pur](https://github.com/alanhamlett/pip-update-requirements)
* [pip_upgrade_outdated](https://github.com/defjaf/pip_upgrade_outdated)
* [pipdate](https://github.com/nschloe/pipdate)
* [pip-review](https://github.com/jgonggrijp/pip-review)

#### Known Issues

* [I'm stuck at "Checking..." forever.](https://github.com/achillesrasquinha/pipupgrade/issues/30)

#### License

This repository has been released under the [MIT License](LICENSE).

---

<div align="center">
  Made with ❤️ using <a href="https://git.io/boilpy">boilpy</a>.
</div>
