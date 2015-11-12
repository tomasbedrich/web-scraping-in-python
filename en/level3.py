#!/usr/bin/env python3

import requests
from urllib.parse import urljoin
import sys

BASE_URL = "https://coolors.co/"

_username, _password = "python_scraper", "secure_password"


def add_user_palette(name, c1, c2, c3, c4, c5):
    """Add user palette on Coolors.co created from colors c1..c5."""
    sess = requests.Session()  # session stores PHPSESSID between requests

    # make login request
    login_data = {
        "e": _username,
        "p": _password
    }
    res = sess.post(urljoin(BASE_URL, "ajax/login"), data=login_data)
    assert res.json()["result"] == 0, "login failed"

    # add palette
    palette_data = {
        "c1": "#" + c1,
        "c2": "#" + c2,
        "c3": "#" + c3,
        "c4": "#" + c4,
        "c5": "#" + c5,
        "name": name,
        "tags": "",
        "key": "Coolors_Simple_KEY",
    }
    sess.post(urljoin(BASE_URL, "ajax/add_user_palette"), data=palette_data)


if __name__ == "__main__":
    sys.argv.pop(0)  # remove script name
    add_user_palette(*sys.argv)
    print("done")
