import re

import bs4
import requests

from cruijff.constants import YEAR
from .utils import cache, legit_header


def _check_fmt(fmt):
    if fmt not in {"sql", "pandas"}:
        raise ValueError("'fmt' must be 'pandas' or 'sql'")


@cache
def get_comps(which="leagues", fmt="pandas"):
    if which not in {"leagues", "cups"}:
        raise ValueError("'which' must be 'cups' or 'leagues'")
    _check_fmt(fmt)

    if which == "cups":
        which = "tournaments"

    h = ""

    j = requests.get("http://www.espnfc.us/api/navigation?xhr=1",
                     headers=legit_header()).json()

    for k in j["navigationItems"]:
        if k["key"] == ".desktop-nav-item.{}".format(which):
            h = k["html"]
            break

    b = bs4.BeautifulSoup(h, "html.parser")
    attr = ":wc:leagues:" if which == "leagues" else ":wc:competitions:"

    ls = (a for a in b.find_all("a") if
          "name" in a.attrs and attr in a["name"])

    l = None

    if fmt == "pandas":
        l = []

        for k in ls:
            d = {"id": int(k["href"].split("/")[-2]),
                 "tid": k["name"].split(":")[-1],
                 "name": k.text,
                 "href": k["href"],
                 "league": which == "leagues"
                 }
            l.append(d)
    elif fmt == "sql":
        l = {"cols": ["id", "tid", "name", "league", "href"], "data": []}

        for k in ls:
            l["data"].append((int(k["href"].split("/")[-2]),
                              k["name"].split(":")[-1],
                              k.text,
                              which == "leagues",
                              k["href"],
                              ))

    return l


@cache
def get_clubs(league, year=YEAR, fmt="pandas"):
    _check_fmt(fmt)
    h = requests.get((
                         "http://www.espnfc.us/lols/{league}/table?"
                         "season={year}&seasonType=1"
                     ).format(league=league, year=year),
                     headers=legit_header()).text
    b = bs4.BeautifulSoup(h, "html.parser")

    ls = b.find_all("td", attrs={"class": "team"})

    l = None

    if fmt == "pandas":
        l = []

        for k in ls:
            k = k.find("a")
            d = {"id": int(k["href"].split("/")[-2]),
                 "tid": k["href"].split("/")[-3],
                 "name": k.text,
                 "href": k["href"]}
            l.append(d)
    elif fmt == "sql":
        l = {"cols": ["id", "tid", "name", "href"], "data": []}

        for k in ls:
            k = k.find("a")
            l["data"].append((int(k["href"].split("/")[-2]),
                              k["href"].split("/")[-3],
                              k.text,
                              k["href"]))

    return l


@cache
def get_games(cid, lid, year=YEAR, upc=True, fmt="pandas"):
    _check_fmt(fmt)

    url = ("http://www.espnfc.us/club/j/{cid}/"
           "fixtures?leagueId={lid}&season={year}").format(cid=cid,
                                                           lid=lid,
                                                           year=year)

    h = requests.get(url, headers=legit_header()).text
    b = bs4.BeautifulSoup(h, "html.parser")

    rx = re.compile("([0-9]*)\.png")
    rix = re.compile("default-team-logo-(500)")

    srx = re.compile(r"^[0-9]+|[0-9]+$")
    prx = re.compile("\(([0-9]*)\)")

    l = []

    lgs = get_comps("leagues") + get_comps("cups")
    lgs = {k["name"]: {"id": k["id"], "tid": k["tid"]} for k in lgs}

    for m in b.find_all("a", class_="score-list"):
        if "upcoming" in m["class"] and not upc:
            continue

        g = {"id": int(m["data-gameid"]),
             "year": year}

        try:
            time = m.find("div", class_="gmt-time").get("data-time")
        except AttributeError:
            print("No time found for game {}".format(g["id"]))
            time = None

        g["time"] = time
        s = m.find("div", class_="status")
        if s is not None:
            g["status"] = s.text

        cname = m.find("div", class_="score-competition")["title"]
        comp = lgs.get(cname) or {}

        g["comp_name"] = cname
        g["comp_tid"] = comp.get("tid")
        g["comp_id"] = comp.get("id") or -1

        for k in {"home", "away"}:
            ht = m.find("div", class_="score-{}-team".format(k))
            g["{}_name".format(k)] = ht.find("img")["alt"]
            if len(rix.findall(ht.find("img")["src"])) == 0:
                g["{}_id".format(k)] = int(rx.findall(ht.find("img")["src"])[0])
            else:
                g["{}_id".format(k)] = -1
            if "upcoming" not in m["class"]:
                score = m.find("span", class_="{}-score".format(k)).text
                p = prx.findall(score)

                if p:
                    g["{}_score".format(k)] = int(srx.findall(score)[0])
                    g["{}_score_pens".format(k)] = int(p[0])
                else:
                    g["{}_score".format(k)] = int(score)

        l.append(g)

    if fmt == "pandas":
        return l
    elif fmt == "sql":
        cols = ["id", "time", "status", "year", "comp_id", "comp_tid",
                "comp_name", "home_id", "home_name", "away_id", "away_name",
                "home_score", "away_score", "home_score_pens",
                "away_score_pens"]

        r = {"cols": cols,
             "data": [tuple(d.get(k) for k in cols) for d in l]}

        return r
