import re

import requests
import bs4

from .utils import cache, legit_header


@cache
def get_comps(which="leagues", force=False):
    if which not in {"leagues", "cups"}:
        raise ValueError("'which' must be 'cups' or 'leagues'")

    if which == "cups":
        which = "tournaments"

    l = []
    h = ""

    j = requests.get("http://www.espnfc.us/api/navigation?xhr=1",
                     headers=legit_header()).json()

    for k in j["navigationItems"]:
        if k["key"] == ".desktop-nav-item.{}".format(which):
            h = k["html"]
            break

    b = bs4.BeautifulSoup(h, "html.parser")
    attr = ":wc:leagues:" if which == "leagues" else ":wc:competitions:"

    for k in (a for a in b.find_all("a") if
              "name" in a.attrs and attr in a["name"]):
        d = {"tid": k["name"].split(":")[-1],
             "name": k.text,
             "href": k["href"],
             "id": int(k["href"].split("/")[-2])}
        l.append(d)

    return l


@cache
def get_clubs(league, year=2016, force=False):
    h = requests.get((
                         "http://www.espnfc.us/{league}/12/table?"
                         "season={year}&seasonType=1"
                     ).format(league=league, year=year),
                     headers=legit_header()).text
    b = bs4.BeautifulSoup(h, "html.parser")

    l = []
    for k in b.find("li", attrs={"data-section": "clubs"}).find("ul").children:
        if k.name != "li":
            continue
        k = k.find("a")
        d = {"tid": k["name"].split(":")[-1],
             "name": k.text,
             "href": k["href"],
             "id": int(k["href"].split("/")[-2])}
        l.append(d)

    return l


@cache
def get_games(cid, year=2016, upc=True, force=False):
    which = "ft" if not upc else "all"
    key = "ESPN|club|{cid}|{year}|{which}".format(cid=cid, year=year,
                                                  which=which)

    url = ("http://www.espnfc.us/club/j/{cid}/"
           "fixtures?leagueId=0&season={year}").format(cid=cid, year=year)

    h = requests.get(url, headers=legit_header()).text
    b = bs4.BeautifulSoup(h, "html.parser")

    rx = re.compile("([0-9]*)\.png")

    l = []

    lgs = get_comps("leagues") + get_comps("cups")
    lgs = {k["name"]: {"id": k["id"], "tid": k["tid"]} for k in lgs}

    for m in b.find_all("a", class_="score-list"):
        if "upcoming" in m["class"] and not upc:
            continue

        g = {"id": int(m["data-gameid"]),
             "time": m.find("div", class_="gmt-time")["data-time"]}

        s = m.find("div", class_="status")
        if s is not None:
            g["status"] = s.text

        cname = m.find("div", class_="score-competition")["title"]
        comp = lgs.get(cname) or {}

        g["comp_name"] = cname
        g["comp_tid"] = comp.get("tid")
        g["comp_id"] = comp.get("id")

        for k in {"home", "away"}:
            ht = m.find("div", class_="score-{}-team".format(k))
            g["{}_name".format(k)] = ht.find("img")["alt"]
            g["{}_id".format(k)] = int(rx.findall(ht.find("img")["src"])[0])
            if not upc:
                g["{}_score".format(k)] = m.find("span",
                                                 class_="{}-score".format(
                                                     k)).text

        l.append(g)

    return l
