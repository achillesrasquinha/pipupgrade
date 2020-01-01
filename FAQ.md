### Frequently Asked Questions

* [How do I upgrade `pip` itself?](#how-do-i-upgrade-pip-itself)
* [How do I upgrade `pipupgrade` itself?](#how-do-i-upgrade-pipupgrade-itself)

#### * How do I upgrade `pip` itself?
---

```
$ pipupgrade --pip
```

Use the `--pip` flag to ensure your `pip` is up-to-date. If you wish to
upgrade a specific `pip` executable, use the `--pip-path` flag. For example, if
you'd like to upgrade `pip3` executable only, the command then would be

```
$ pipupgrade --pip --pip-path pip3
```

The `--pip` flag enures to upgrade pip before it attempts to upgrade all other 
packages.

#### * How do I upgrade `pipupgrade` itself?
---

```
$ pipupgrade --self
```

Use the `--self` flag to ensure your `pipupgrade` is up-to-date. `pipupgrade`
 will then attempt to upgrade itself and exit execution.