#!/usr/bin/env python3

import json
from requests import get
from bs4 import BeautifulSoup


# make HTTP GET request for people and access HTML by .text attribute of response
html = get("https://www.linuxdays.cz/2015/lide").text
soup = BeautifulSoup(html, "html.parser")

# prepare dict for results
people = {}

# find all elements with class="karta" (contains info about people)
# note the _ after class, this prevents `class` to be interpreted as a keyword
for person in soup.find_all(class_="karta"):
    # note that the base element for finding details is `person`
    name = person.find("h3").text
    description = person.find("p").text
    people[name] = description


# print people in CSV format (separated by TAB) to opened file
with open("people.csv", "w") as csv_file:
    for name, description in people.items():
        print(name, end="\t", file=csv_file)
        print(description, file=csv_file)


# write people info in JSON
with open("people.json", "w") as json_file:
    json.dump(people, json_file, ensure_ascii=False, indent=2)
