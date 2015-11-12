#!/usr/bin/env python3

import sys
from requests import get

CRIME_CODE = 821  # = bribery

# make HTTP GET request for areas, parse them as JSON and access a list under a key "areas"
areas = get("http://mapakriminality.cz/api/areas", params={"level": 2}).json()["areas"]

# print each area's code and name
for area in areas:
    print(area["Code"], area["Name"])
print("-" * 80)

# load desired area code from user
desired_area_code = input("Which area are you interested in (enter code): ")

# make HTTP GET request for crimes with more params, parse the response as
# JSON and access a first item in a list under a key "crimes"
params = {
    "areacode": desired_area_code,
    "crimetypes": CRIME_CODE,
    "groupby": "area",  # ensures that there will be only one item in the list
}
crimes = get("http://mapakriminality.cz/api/crimes", params=params).json()["crimes"]

if len(crimes) == 1:  # if there are some results
    crimes = crimes[0]
    print("{} crimes found in this area, {} of them solved".format(crimes["Found"], crimes["Solved"]))

else:  # no results means (most probably) that user entered invalid area code
    print("Invalid area code entered")
    sys.exit(1)
