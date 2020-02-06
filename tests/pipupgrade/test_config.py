from pipupgrade.config  import Settings, environment
from pipupgrade         import __version__

def test_settings():
    settings = Settings()
    settings.get("version") == __version__

def test_environment():
    details = environment()

    assert all((k in details for k in ("version", "python_version", "os",
        "config", "pip_executables")))

    return details