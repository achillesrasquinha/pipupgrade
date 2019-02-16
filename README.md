<div align="center">
    <img src=".github/assets/meme.jpg" width="250">
    <h1>
        pipupgrade
    </h1>
    <h4>The missing command for <code>pip</code></h4>
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
* Updates packages mentioned within a `requirements.txt` file (Also pins upto-date versions if mentioned).
* Smart `requirements.txt` detector.
* [Pipfile](https://github.com/pypa/pipenv) support.
* Detects semantic version to avoid updates that break changes.
* Python 2.7+ and Python 3.4+ compatible. Also pip 9+, pip 10+, pip 18+ and [pip 19.0.1+](https://github.com/pypa/pip/issues/6158) compatible.
* Automate your Dependencies by installing `pipupgrade` in your CI workflow.
* Zero Dependencies!

#### Installation

```shell
$ pip install pipupgrade
```

#### Usage

<div align="center">
    <img src=".github/assets/demo.gif">
</div>

That's basically it! Run the help for more details...

```
$ pipupgrade --help
usage: pipupgrade [--pip-path PIP_PATH] [-y] [-c] [-l] [-s] [-r REQUIREMENTS]
                  [-i] [-u] [--no-color] [-V] [-v] [-h]

pipupgrade (v 1.4.0)

UPGRADE ALL THE PIP PACKAGES!

optional arguments:
  --pip-path PIP_PATH   Path to pip executable to be used. (default: pip)
  -y, --yes             Confirm for all dialogs. (default: False)
  -c, --check           Check for outdated packages. (default: False)
  -l, --latest          Update all packages to latest. (default: False)
  -s, --self            Update pipupgrade. (default: False)
  -r REQUIREMENTS, --requirements REQUIREMENTS
                        Path(s) to requirements.txt file. (default: None)
  -i, --interactive     Interactive Mode (default: False)
  -u, --user            Install to the Python user install directory for
                        environment variables and user configuration.
                        (default: False)
  --no-color            Avoid colored output. (default: False)
  -V, --verbose         Display verbose output. (default: False)
  -v, --version         Show pipupgrade's version number and exit.
  -h, --help            Show this help message and exit.
```

#### License

This repository has been released under the [MIT License](LICENSE).

---

<div align="center">
  Made with ❤️ using <a href="https://git.io/boilpy">boilpy</a>.
</div>