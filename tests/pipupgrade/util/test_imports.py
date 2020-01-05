from pipupgrade.util.imports import HandlerRegistry, import_handler

def test_handler_registry():
    registry = HandlerRegistry()

    assert len(registry) == 0

    registry["os"]

    assert "os" in registry and __import__("os") == registry["os"]
    assert len(registry) == 1

def test_import_handler():
    assert import_handler("os")         == __import__("os")
    assert import_handler("pipupgrade") == __import__("pipupgrade")
    
    assert import_handler("pipupgrade.util.imports.import_handler") == import_handler