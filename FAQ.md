### Frequently Asked Questions

* [How do I update `pip` itself?](#how-do-i-update-pip-itself)

["How do I update `pip` itself?]()
---

```
$ pipupgrade --pip
```

Use the `--pip` flag to ensure your `pip` is up-to-date. If you wish to
update a specific `pip` executable, use the `--pip-path` flag. For example

```
$ pipupgrade --pip --pip-path pip3
```

This updates the pip3 executable only.