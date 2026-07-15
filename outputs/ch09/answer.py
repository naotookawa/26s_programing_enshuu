"""Chapter 9 submission.

Problem selected by the user: showaddress using HTTP + JSON.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path


DEFAULT_URL_TEMPLATE = "https://www.graco.c.u-tokyo.ac.jp/~kaneko/lecture/pl/{zipcode}.json"


def fetch_json(url: str):
    """Fetch JSON from URL and parse it.

    >>> data = fetch_json_from_text('{"address": "Tokyo"}')
    >>> data["address"]
    'Tokyo'
    """
    with urllib.request.urlopen(url) as response:
        return json.load(response)


def fetch_json_from_text(text: str):
    return json.loads(text)


def _candidate_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for key in ("address", "allAddress", "fullAddress", "prefecture", "pref", "city", "town", "addr"):
            value = obj.get(key)
            if isinstance(value, str) and value:
                yield value
        for key in ("data", "results", "addresses", "items"):
            value = obj.get(key)
            if isinstance(value, list):
                for item in value:
                    yield from _candidate_strings(item)
        for value in obj.values():
            yield from _candidate_strings(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from _candidate_strings(item)


def extract_address(data) -> str:
    """Extract a human-readable address string from nested JSON.

    The postal-code APIs used in class are not fully uniform, so this function
    tries common field names and falls back to the first string-like payload.
    """
    seen = []
    for s in _candidate_strings(data):
        if s not in seen:
            seen.append(s)
    if not seen:
        raise ValueError("could not find address text in JSON")

    # Prefer concatenating common address components if available.
    if isinstance(data, dict):
        parts = []
        for key in ("prefecture", "pref", "city", "town", "address"):
            value = data.get(key)
            if isinstance(value, str) and value:
                parts.append(value)
        if parts:
            return "".join(parts)
        for key in ("allAddress", "fullAddress"):
            value = data.get(key)
            if isinstance(value, str) and value:
                return value

    return seen[0]


def showaddress(zipcode: str, url_template: str = DEFAULT_URL_TEMPLATE) -> str:
    """Fetch a postal-code JSON and return the address string.

    >>> sample = {"prefecture": "東京都", "city": "目黒区", "town": "大橋"}
    >>> extract_address(sample)
    '東京都目黒区大橋'
    """
    url = url_template.format(zipcode=zipcode)
    data = fetch_json(url)
    address = extract_address(data)
    print(address)
    return address


def showaddress_from_file(filename: str) -> str:
    """Read a local JSON file and display the address.

    This is useful for offline testing.
    """
    with open(filename, encoding="utf-8") as file:
        data = json.load(file)
    address = extract_address(data)
    print(address)
    return address


def _test_extract_address() -> None:
    assert extract_address({"prefecture": "東京都", "city": "目黒区", "town": "大橋"}) == "東京都目黒区大橋"
    assert extract_address({"allAddress": "東京都目黒区大橋"}) == "東京都目黒区大橋"
    assert extract_address({"results": [{"address": "東京都目黒区"}]}) == "東京都目黒区"


def _test_showaddress_from_file() -> None:
    path = Path("outputs/ch09/sample_postal.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"prefecture": "東京都", "city": "目黒区", "town": "大橋"}), encoding="utf-8")
    assert showaddress_from_file(str(path)) == "東京都目黒区大橋"


if __name__ == "__main__":
    _test_extract_address()
    _test_showaddress_from_file()

    if len(sys.argv) == 2:
        showaddress(sys.argv[1])
    elif len(sys.argv) == 3:
        # Allow a local file path for offline verification.
        showaddress_from_file(sys.argv[2])
    else:
        print("usage: python outputs/ch09/answer.py ZIPCODE [LOCAL_JSON_FILE]")
