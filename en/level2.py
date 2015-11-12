#!/usr/bin/env python3

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from collections import defaultdict

BASE_URL = "http://m.imdb.com"


def get_movie_links():
    """Get list of links to top movies on IMDB."""
    res = requests.get(urljoin(BASE_URL, "chart/top"))
    soup = BeautifulSoup(res.text, "html.parser")
    media = soup.find_all(class_="media")
    return [i.find("a")["href"] for i in media]


def get_actors(movie_url):
    """Get list of actors starring in a movie by its URL."""
    res = requests.get(urljoin(BASE_URL, movie_url))
    soup = BeautifulSoup(res.text, "html.parser")
    actors = soup.find(id="cast-and-crew").find_all("li")
    return [actor.find("strong").text for actor in actors]


actors = defaultdict(lambda: 0)

# count actors appearance in top 20 movies
for i, movie_link in enumerate(get_movie_links()):
    for name in get_actors(movie_link):
        actors[name] += 1
    print("processed movie #{}".format(i + 1))
    if i >= 19:
        break
print("end")


# print actors starring in 3 or more movies
for actor, count in actors.items():
    if count >= 3:
        print(actor, count)
