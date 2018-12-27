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
    <a href="https://coveralls.io/github/achillesrasquinha/pipupgrade">
        <img src="https://img.shields.io/coveralls/github/achillesrasquinha/pipupgrade.svg?style=flat-square">
    </a>
    <a href="https://pypi.org/project/pipupgrade/">
		<img src="https://img.shields.io/pypi/v/pipupgrade.svg?style=flat-square">
	</a>
    <a href="https://pypi.org/project/pipupgrade/">
		<img src="https://img.shields.io/pypi/l/pipupgrade.svg?style=flat-square">
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

### Features
* Updates system packages and local packages.
* Updates packages mentioned within a `requirements.txt` file (Also pins upto-date versions if mentioned).
* Detects semantic version to avoid updates that break changes.
* Zero Dependencies!

#### Installation

```shell
$ pip install pipupgrade
```

### Usage

<div align="center">
    <img src=".github/assets/demo.gif">
</div>

That's basically it! Run the help for more details...

```
$ pipupgrade --help
usage: pipupgrade [-y] [-c] [-l] [-s] [-r REQUIREMENTS] [-u] [--no-color] [-V]
                  [-v] [-h]

UPGRADE ALL THE PIP PACKAGES!

optional arguments:
  -y, --yes             Confirm for all dialogs
  -c, --check           Check for outdated packages
  -l, --latest          Update all packages to latest
  -s, --self            Update self
  -r REQUIREMENTS, --requirements REQUIREMENTS
                        Path to requirements.txt file
  -u, --user            Install to the Python user install directory for
                        environment variables and user configuration.
  --no-color            Avoid colored output
  -V, --verbose         Display verbose output
  -v, --version         show program's version number and exit
  -h, --help            Show this help message and exit
```

### License

This repository has been released under the [MIT License](LICENSE).