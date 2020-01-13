from pipupgrade.config  import Settings
from pipupgrade         import __version__

def test_settings():
    settings = Settings()
    settings.get("version") == __version__