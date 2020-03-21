### Frequently Asked Questions

* [What does each color symbolize?](#what-does-each-color-symbolize)
* [How do I upgrade `pip` itself?](#how-do-i-upgrade-pip-itself)
* [How do I upgrade `pipupgrade` itself?](#how-do-i-upgrade-pipupgrade-itself)
* [How do I upgrade a Python Project?](#how-do-i-upgrade-a-python-project)
* [How do I update a requirements.txt file?](#how-do-i-update-a-requirementstxt-file)
* [How do I perform a dry run?](#how-do-i-perform-a-dry-run)
* [How do I view a dependency graph?](#how-do-i-view-a-dependency-graph)
* [How do I upgrade only selected packages?](#how-do-i-upgrade-only-selected-packages)

### What does each color symbolize?
---

`pipupgrade` uses **[Semantic Versioning](https://semver.org/)** to detect packages 
that require an upgrade. When you run `pipupgrade`, it displays the list of packages 
that requires an upgrade in the following format:

<div align="center">
  <img src="docs/source/assets/demos/pipupgrade-list.png">
</div>

Each color denotes the following information:

* ***Red*** - Packages highlighted in red are upgrades that can potentially be a breaking change.
This means that upgrading this package could most likely cause packages dependent on it to break as well.
By default, `pipupgrade` does not upgrade these packages unless you pass in the `--latest` flag or
`--upgrade-type major`.
* ***Yellow*** - Packages highlighted in yellow are upgrades that don't necessarily break a change but 
provides a novel feature upgrade. Upgrading such packages could provide new features. By default,
`pipupgrade` upgrades these packages. You can also selectively upgrade such packages by passing the flag  
`--upgrade-type minor`.
* ***Green*** - Packages highlighted in green are patched upgrades. Upgrading such packages will most likely not break any changes and are safe to update. By default,
`pipupgrade` upgrades these packages. You can also selectively upgrade such packages by passing the flag  
`--upgrade-type patch`.

### How do I upgrade `pip` itself?
---

```
$ pipupgrade --pip
```

Use the `--pip` flag to ensure your `pip` is up-to-date. You can also set the 
environment variable `PIPUPGRADE_PIP` to `true`. `pipupgrade` would then 
attempt to upgrade all pip executables it's able to discover and upgrade 
them parallely. If you wish to upgrade a specific `pip` executable, use the 
`--pip-path` flag. For example, if you'd like to upgrade `pip3` executable only, 
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

The `--project` flag attempts to discover and update `requirements*.txt` files 
within the entire project directory. It also discovers `Pipfile` 
and if found, attempts to updates `Pipfile` and `Pipfile.lock`.

In order to discover requirement files recursively, use the `--force` flag
 or set the environment variable `PIPUPGRADE_FORCE` to `true`.

```
$ pipupgrade --project "<PATH_TO_PYTHON_PROJECT>" --force
```

### How do I update a requirements.txt file?
---

```
$ pipupgrade --requirements "<PATH_TO_REQUIREMENTS_FILE>"
```

### How do I perform a dry run?
---

```
$ pipupgrade --check
```

Use the `--check` flag to perform a dry run. You can also set the 
environment variable `PIPUPGRADE_DRY_RUN` to `true`.

### How do I view a dependency graph?
---

```
$ pipupgrade --format tree
```

<div align="center">
  <img src="docs/source/assets/demos/pipupgrade-format-tree.gif">
</div>

The dependency graph also highlights any conflicting dependencies. 
You can also set the environment variable `PIPUPGRADE_DISPLAY_FORMAT` to `tree`.
 If you avoid using the `--latest` flag, the tree format ensures to avoid
 child dependencies that break changes.

### How do I upgrade only selected packages?
---

```
$ pipupgrade "<PACKAGE_1>" "<PACKAGE_2>"
```