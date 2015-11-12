#!/usr/bin/env python3

import click
from requests import get
from bs4 import BeautifulSoup
from datetime import date


@click.command()
@click.argument("frm")
@click.argument("to")
@click.option("--date", default="{0:%Y%m%d}".format(date.today()))
@click.option("--tarif", default="REGULAR")
@click.option("--credit/--no-credit", default=False)
def studentagency_lines(frm, to, tarif, date, credit):

    # assemble URL
    url = "https://jizdenky.studentagency.cz/m/Booking/from/{frm}/to/{to}/tarif/{tarif}/departure/{date}/retdep/{date}/return/false/credit/{credit}".format(
        frm=frm.upper(), to=to.upper(), tarif=tarif.upper(), date=date, credit=str(credit).lower())

    # create request and HTML parser
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # prepare list for results
    lines = []

    # parse all lines
    for line in soup.find_all(class_="show-detail"):

        try:
            # try to interpret transfer as int
            transfer = int(line.find(class_="transfer").text)
        except ValueError:
            transfer = 0

        # add a line to result list
        lines.append({
            "vehicle": line.find(class_="type-img").find("img")["title"],
            "departure": line.find(class_="departure").text,
            "arrival": line.find(class_="arrival").text,
            "transfer": transfer,
            "free": int(line.find(class_="free").text),
            "price": int(line.find(class_="price").text)
        })

    # print result
    for line in lines:
        print("{departure:>8} {arrival:>8} {free:>5} {price:>7} Kc".format(**line))


# if running from console
if __name__ == "__main__":
    studentagency_lines()  # click handles the rest
