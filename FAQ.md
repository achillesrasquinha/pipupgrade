### Frequently Asked Questions

* [How do I upgrade `pip` itself?](#how-do-i-upgrade-pip-itself)
* [How do I upgrade `pipupgrade` itself?](#how-do-i-upgrade-pipupgrade-itself)
* [How do I upgrade a Python Project?](#how-do-i-upgrade-a-python-project)
* [How do I perform a dry run?](#how-do-i-perform-a-dry-run)

### How do I upgrade `pip` itself?
---

```
$ pipupgrade --pip
```

Use the `--pip` flag to ensure your `pip` is up-to-date. `pipupgrade` would 
then attempt to upgrade all pip executables it's able to discover and upgrade 
them parallely. If you wish to upgrade a specific `pip` executable, use the `--pip-path` flag. For example, if you'd like to upgrade `pip3` executable only, 
the command then would be

```
$ pipupgrade --pip --pip-path pip3
```

The `--pip` flag enures to upgrade pip before it attempts to upgrade all other 
packages.

### How do I upgrade `pipupgrade` itself?
---

```
$ pipupgrade --self
```

Use the `--self` flag to ensure your `pipupgrade` is up-to-date. `pipupgrade`
 will then attempt to upgrade itself and exit execution.

### How do I upgrade a Python Project?
---

```
$ pipupgrade --project "<PATH_TO_PYTHON_PROJECT>"
```

The `--project` flag attempts to discover `requirements*.txt` files, recursively.

### How do I perform a dry run?
---

```
$ pipupgrade --check
```