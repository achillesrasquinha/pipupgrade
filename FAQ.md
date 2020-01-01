### Frequently Asked Questions

* [How do I update `pip` itself?](#how-do-i-update-pip-itself)

#### How do I update `pip` itself?
---

```
$ pipupgrade --pip
```

Use the `--pip` flag to ensure your `pip` is up-to-date. If you wish to
update a specific `pip` executable, use the `--pip-path` flag. For example, if
you'd like to update `pip3` executable only, the command then would be

```
$ pipupgrade --pip --pip-path pip3
```