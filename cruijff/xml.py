import urllib
import os
import io
import logging as log
import re
import fnmatch
import html
import bz2
import base64

import appdirs
import numpy as np
from lxml import etree as ET

from .dbutils import gids
from .constants import YEAR


def get_cachep(tl=False):
    return "{}/cruijff/xml/{}".format(appdirs.user_cache_dir(),
                                      "timelines" if tl else "gamecasts")


def download_xml(game_id, force=False):
    cachep = appdirs.user_cache_dir() + "/cruijff"
    if not os.path.exists(cachep):
        os.mkdir(cachep)

    cachep += "/xml"
    cpaths = {"gamecast": cachep + "/gamecasts",
              "timeline": cachep + "/timelines"}

    if not os.path.exists(cachep):
        os.mkdir(cachep)
        [os.mkdir(cpaths[k]) for k in cpaths]

    for k in {"gamecast", "timeline"}:
        lpath = cpaths[k] + "/" + str(game_id) + ".xml"
        if os.path.exists(lpath):
            if force:
                os.unlink(lpath)
            else:
                log.warning("File '{}' exists".format(lpath))
                continue
        with io.open(lpath, "wb") as out:
            url = ("http://www.espnfc.us/gamepackage10/data/{k}"
                   "?gameId={game_id}&langId=0&snap=0".format(game_id=game_id,
                                                              k=k))
            with urllib.request.urlopen(url) as xml:
                for l in xml:
                    out.write(l)


def grid_decode(g):
    deg = bz2.decompress(base64.b64decode(g)).decode("utf-8")
    hm = np.zeros((22, 32), dtype="int")
    for i in range(22):
        for k in range(32):
            hm[i][k] = int(deg[32 * i + k])
    return hm


def grid_encode(g):
    return base64.b64encode(bz2.compress(g.encode("utf-8"))).decode("utf-8")


def gfind(p, lid, year=YEAR, tl=True):
    rxp = re.compile(fnmatch.translate(p))
    ids = gids(lid=lid, year=year)

    paths = ["{}/{}.xml".format(get_cachep(tl), gid) for gid in ids]
    a = []

    for x in paths:
        with io.open(x, "r") as f:
            if rxp.match(f.read().lower()) is not None:
                a.append(x)
    return a


def pfind(name, side, ps):
    p = {}
    for x in ps:
        if x["side"] == side and x["name"] == name:
            if p:
                p = {"name": name}
            else:
                p = {"name": name, "id": x["id"], "jersey": x["jersey"]}
    if not p:
        return {"name": name}
    return p


def gparse(gid, pos=False):
    p = "{}/{}.xml".format(get_cachep(tl=False), gid)

    if not os.path.exists(p):
        download_xml(gid)

    tree = ET.parse(p)
    r = tree.getroot()

    tg = {"Goal - Header", "Shot Hit Woodwork", "Goal", "Goal - Free-kick",
          "Shot Blocked", "Shot On Target"}

    srx = re.compile(r"^[0-9]+|[0-9]+$")
    prx = re.compile("\(([0-9]*)\)")

    g = {}
    for c in r:
        if c.tag == "teams":
            for t in c:
                g[t.tag] = {"id": int(t.attrib["id"]),
                            "name": html.unescape(t.text)}
        elif c.tag == "shots":
            g["shots"] = []
            l = g["shots"]
            for k in c:
                at = k.attrib["addedTime"].strip().replace("'", "")
                d = {"clock": int(k.attrib["clock"]) + int(
                    at if at != "" else 0),
                     "period": int(k.attrib["period"]),
                     "x": float(k.attrib["startX"]),
                     "y": float(k.attrib["startY"]),
                     "teamid": int(k.attrib["teamId"]),
                     }
                if k.attrib["goal"] != "f":
                    d["g"] = True
                if k.attrib["ownGoal"] != "f":
                    d["og"] = True
                if k.attrib["shootout"] != "f":
                    d["shootout"] = True

                d["player"] = {}
                for c in k:
                    if c.tag == "player":
                        d["player"]["name"] = html.unescape(c.text).strip()
                    elif c.tag == "part":
                        d["player"]["jersey"] = int(c.attrib["jersey"])
                        d["player"]["id"] = int(c.attrib["pId"])
                        for p in c:
                            if p.tag == "resultText":
                                d["result"] = p.text
                                if "Penalty" in p.text:
                                    d["pen"] = True
                                elif "Free Kick" in p.text or "Free-kick" in p.text:
                                    d["fk"] = True
                                if p.text in tg:
                                    d["sot"] = True

                l.append(d)
        elif c.tag == "gameInfo":
            g["result"] = {}
            for i in c:
                if i.tag in {"homeScore", "awayScore"}:
                    where = "home" if i.tag == "homeScore" else "away"
                    score = i.text
                    if "(" in score:
                        g["result"][where+"_pens"] = int(prx.findall(score)[0])
                        g["result"][where] = int(srx.findall(score)[0])
                    else:
                        g["result"][where] = int(i.text)
        elif c.tag == "attack" and pos:
            p = []
            for x in c:
                d = {}
                pid = x.attrib["playerId"]
                if len(x) == 0:
                    continue
                if pid != "-1":
                    d["player"] = {"id": int(pid),
                                   "jersey": int(x.attrib["jersey"]),
                                   "name": html.unescape(x.text).strip()}
                    d["pos"] = x.attrib["position"]
                d["teamid"] = int(x.attrib["teamId"])
                d["avg"] = {"x": float(x.attrib["avgX"]),
                            "y": float(x.attrib["avgY"])}
                d["p"] = {"x": float(x.attrib["posX"]),
                          "y": float(x.attrib["posY"])}
                d["lmr"] = {"l": float(x.attrib["left"]),
                            "m": float(x.attrib["middle"]),
                            "r": float(x.attrib["right"])}

                grid = x[0].text.replace("~", "")
                d["grid"] = {"max": int(x[0].attrib["max"]),
                             "data": grid_encode(grid)}
                p.append(d)
            g["pos"] = p
    return g


def tparse(gid):
    p = "{}/{}.xml".format(get_cachep(tl=True), gid)

    if not os.path.exists(p):
        download_xml(gid)

    tree = ET.parse(p)
    g = gparse(gid, pos=True)

    r = tree.getroot()
    ts = {g["home"]["id"]: "home", g["away"]["id"]: "away"}
    ps = [dict(x["player"], **{"side": ts[x["teamid"]]}) for x in g["pos"] if
          "player" in x]

    ev = r[5]

    tl = []

    for e in ev:
        at = e.attrib["addedTime"].strip().replace("'", "")
        at = int(at) if len(at) > 0 else 0
        d = {"clock": int(e.attrib["clock"]) + at,
             "type": e.attrib["type"],
             "period": 2 if int(e.attrib["clock"]) > 45 else 1}
        # the great scraping
        t = e[0].text
        data = {}
        if d["type"] in {"yellowCard", "goal", "redCard"}:
            p = html.unescape(re.compile("<b>(.*)<\/b>").findall(t)[0])
            data = {"player": pfind(p, e.attrib["side"], ps)}
        elif d["type"] == "substitution":
            if d["clock"] == 45:  # if it's 45' it's probably the second half
                d["period"] = 2
            p1 = html.unescape(
                re.compile("<b>On: (.*)<\/b>").findall(t)[0])
            p2 = html.unescape(re.compile("<br>Off: (.*)").findall(t)[0])
            data = {"on": pfind(p1, e.attrib["side"], ps),
                    "off": pfind(p2, e.attrib["side"], ps)}
        else:
            print("Warning, unparsed event: " + repr(t))
        d["data"] = data
        tl.append(d)

    g["tl"] = tl
    return g
