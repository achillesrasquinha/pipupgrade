<div align="center">
    <h1>
        <code>pipupgrade</code>
    </h1>
    <h4>The missing command for <code>pip</code></h4>
</div>

<div align="center">
    <img src=".github/assets/meme.jpg">
</div>

### Table of Contents
* [Installation](#installation)
* [Usage](#usage)
* [License](#license)

#### Installation

```shell
$ pip install pipupgrade
```

### Usage

```shell
$ pipupgrade
Do you wish to update 200 packages? [Y/n]: Y
Updating 1 of 200: pipupgrade
...
UPGRADED ALL THE PIP PACKAGES!
```

That's basically it! Run the help for more details...

```shell
$ pipupgrade --help
usage: pipupgrade [-h] [-y] [--no-color] [-V] [-v]

UPGRADE ALL THE PIP PACKAGES!

optional arguments:
  -h, --help     show this help message and exit
  -y, --yes      Confirm for all dialogs
  --no-color     Avoid colored output
  -V, --verbose  Display verbose output
  -v, --version  show program's version number and exit
```

### License

This repository has been released under the [MIT License](LICENSE).