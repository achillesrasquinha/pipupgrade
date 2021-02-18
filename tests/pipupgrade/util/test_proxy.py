from pipupgrade.util.proxy import (
    to_dict as proxy_to_dict,
    to_addr as proxy_to_addr
)

def test_to_addr():
    assert proxy_to_addr({ "ip": "41.65.146.38",   "port": "8080", "secure": False }) == "http://41.65.146.38:8080"
    assert proxy_to_addr({ "ip": "118.99.74.10",   "port": "8080", "secure": True  }) == "https://118.99.74.10:8080"
    assert proxy_to_addr({ "ip": "177.73.170.165", "port": "8080", "secure": False }) == "http://177.73.170.165:8080"
    assert proxy_to_addr({ "ip": "165.16.96.93",   "port": "8080", "secure": False }) == "http://165.16.96.93:8080"

def test_to_dict():
    assert proxy_to_dict("41.65.146.38:8080 EG-A +") == { "ip": "41.65.146.38",
        "port": "8080", "country_code": "EG", "anonymity": "A", "secure": False,
        "google_passed": True, "one_way": False }
    assert proxy_to_dict("118.99.74.10:8080 ID-N-S -") == { "ip": "118.99.74.10",
        "port": "8080", "country_code": "ID", "anonymity": "N", "secure": True,
        "google_passed": False, "one_way": False }
    assert proxy_to_dict("177.73.170.165:8080 BR-N +") == { "ip": "177.73.170.165",
        "port": "8080", "country_code": "BR", "anonymity": "N", "secure": False,
        "google_passed": True, "one_way": False }
    assert proxy_to_dict("165.16.96.93:8080 LY-N! -") == { "ip": "165.16.96.93",
        "port": "8080", "country_code": "LY", "anonymity": "N", "secure": False,
        "google_passed": False, "one_way": True }