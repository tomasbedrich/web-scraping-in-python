#!/usr/bin/env python3

import requests

# normal request
requests.get("http://numbersapi.com/42").text

# GET params
params = {"json": ""}
requests.get("http://numbersapi.com/42", params=params).json()

# catching errors
try:
    res = requests.get("http://numbersapi.com/42")
    print(res.status_code, res.reason)
except requests.ConnectionError as e:
    print(e)
