#!/usr/bin/env python3

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "http://apod.nasa.gov/apod/"


def get_archive():
    """Get all archive images as a dict of links and titles."""
    res = requests.get(urljoin(BASE_URL, "archivepix.html"))
    soup = BeautifulSoup(res.text, "html.parser")
    archive_links = soup.find("b").find_all("a")
    return {link["href"]: link.text for link in archive_links}


def get_img_src(url):
    """Get single image SRC from its page."""
    res = requests.get(urljoin(BASE_URL, url))
    soup = BeautifulSoup(res.text, "html.parser")
    img = soup.find("img")
    if not img:
        raise ValueError("No <img> found on page")
    return img["src"]


def download_image(img_src, to_filename):
    """Download single image by its SRC and save it to filename."""
    res = requests.get(urljoin(BASE_URL, img_src), stream=True)
    with open(to_filename, "wb") as f:
        for chunk in res:
            f.write(chunk)


archive = get_archive()
for i, (url, title) in enumerate(archive.items()):
    try:
        src = get_img_src(url)  # get img src
        filename = "img/" + src.split("/")[-1]  # assemble target filename
        download_image(src, filename)  # download img
        print("downloaded", title, "to", filename)
    except ValueError:
        print("error, skipping ", title)
    if i >= 9:  # not to download whole NASA
        break
print("end")
