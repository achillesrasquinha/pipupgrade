### Installation

#### Installation via pip

The recommended way to install **pipupgrade** is via `pip`.

```shell
$ pip install pipupgrade
```

For instructions on installing python and pip see “The Hitchhiker’s Guide to Python” 
[Installation Guides](https://docs.python-guide.org/starting/installation/).

#### Building from source

`pipupgrade` is actively developed on [GitHub](https://github.com/achillesrasquinha/pipupgrade)
and is always avaliable.

You can clone the base repository with git as follows:

```shell
$ git clone git@github.com:achillesrasquinha/pipupgrade.git
```

Optionally, you could download the tarball or zipball as follows:

##### For Linux Users

```shell
$ curl -OL https://github.com/achillesrasquinha/tarball/ccapi
```

##### For Windows Users

```shell
$ curl -OL https://github.com/achillesrasquinha/zipball/ccapi
```

Install necessary dependencies

```shell
$ cd ccapi
$ pip install -r requirements.txt
```

Then, go ahead and install pipupgrade in your site-packages as follows:

```shell
$ python setup.py install
```

Check to see if you’ve installed pipupgrade correctly.

```shell
$ pipupgrade --help
```