import zlib
import base64
import json
import re
import fnmatch
import pendulum

import requests
from redis import Redis
import pandas as pd
from pymongo import MongoClient
import pymongo.errors as merr
from mnemon import mnd


from ..constants import YEAR
from .orm import Competition


def _val(v, s=None):
    if s is None:
        s = {"raw", "proc", "df"}
    if v not in s:
        raise ValueError(v)


def _dec(s):
    return zlib.decompress(base64.b64decode(s)).decode("utf-8")


def odate(ts):
    dt = pendulum.parse(ts).timezone_("Europe/London")
    dt = pendulum.timezone("Europe/Rome").convert(dt)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def mc(coll=None):
    if coll:
        return MongoClient().get_database("opta").get_collection(coll)
    else:
        return MongoClient().get_database("opta")


def bproc(j, which="teams"):
    l = []
    if which in {"teams", "comps"}:
        a = {"id": "id", "1": "full", "2": "short", "3": "abbr"}
    elif which == "team":
        a = {"id": "id", "1": "first", "2": "last", "3": "known"}
    else:
        raise ValueError(which)

    for d in j:
        l.append({a[k]: d[k] for k in d})

    return l


def bget(url, mongo=None, proc=None):
    r = Redis()
    coll = None
    if url in r:
        j = json.loads(r[url].decode("utf-8"))
        if proc:
            j = proc(j)
        return j
    if mongo:
        coll = mc(mongo["coll"])
        d = coll.find_one(mongo["key"])
        if d:
            return d["data"]

    j = requests.get("http://127.0.0.1:9080" + url).text
    if j:
        j = _dec(j)
        r[url] = j
        jl = json.loads(j)
        if proc:
            jl = proc(jl)

        exp = 3600 if "err" not in jl else 5
        r.expire(url, exp)

        if mongo and "err" not in jl:
            doc = dict(data=jl, **mongo["key"])
            coll.insert(doc)

        return jl
    else:
        raise RuntimeError(j)


def _add_team(r, teams):
    s = r["Standing"]
    s["Team"] = teams[r["@attributes"]["TeamRef"]]
    return s


def rget(feed, season=YEAR, cid="null", team="null", gid="null",
         player="null"):
    url = "/f/{}/{}/{}/{}/{}".format(feed, season, cid, team, gid, player)

    return bget(url)


def comps(match=None, season=YEAR, raw=False):
    url = "/comps/{}".format(season)

    coll = mc("md_comps")

    if coll.find_one({"season": season}) is None:
        j = bget(url, proc=lambda x: bproc(x, "comps"))

        try:
            coll.insert_many(j, ordered=False)
        except merr.BulkWriteError:
            pass
    else:
        j = list(coll.find({"season": season}, {"_id": False}))

    if match is not None:
        if type(match) is int:
            j = [c for c in j if c.get("id") == match]
        else:
            rxp = re.compile(fnmatch.translate(match),
                             flags=re.IGNORECASE)
            j = [c for c in j if rxp.match(c.get("full")) or
                 ("short" in c and rxp.match(c.get("short")))]

    if raw:
        return j
    else:
        if len(j) == 1:
            j = j[0]
            if "_id" in j:
                del j["_id"]
            return Competition(**j, season=season)
        else:
            return (
                pd.DataFrame(j, columns=["id", "full", "short", "abbr"])
                .set_index("id").sort_index()
            )


def teams(cid, season=YEAR):
    url = "/teams/{}/{}".format(cid, season)

    mongo = {"key": {"cid": cid, "season": season}, "coll": "md_clubs"}

    j = bget(url, mongo=mongo, proc=lambda x: bproc(x, "teams"))

    return {int(d["id"]): {k: d[k] for k in d if k != "id"} for d in j}


def team(cid, team, season=YEAR):
    """This needs a custom Mongo importer"""

    url = "/team/{}/{}/{}".format(cid, team, season)

    j = bget(url, proc=lambda x: bproc(x, "team"))

    coll = mc("md_players")

    try:
        coll.insert_many(j, ordered=False)
    except merr.BulkWriteError:
        pass

    return {int(d["id"]): {k: d[k] for k in d if k not in {"id",
                                                           "_id"}} for d in j}


def player(pid, mconn=None):
    mconn = (mconn or mc()).get_collection("md_players")
    if type(pid) in {int, str}:
        pid = int(pid)
        d = mconn.find_one({"id": pid})
        if d is None:
            return None
        del d["_id"]
        return d
    elif hasattr(pid, "__iter__"):
        l = []
        pid = [int(k) for k in pid]
        for d in mconn.find({"id": {"$in": pid}}):
            if d is not None:
                del d["_id"]
                l.append(d)
        if len(l) == 1:
            l = l[0]
        return l


def stats(cid, team, season=YEAR):
    url = "/stats/{}/{}/{}".format(cid, team, season)

    return bget(url)


def parse_game(g, teams=None):
    mi = g["MatchInfo"]

    gid = int(g["@attributes"]["uID"][1:])

    dt = odate(mi["dateObj"]["locale"])

    d = {"gid": gid, "dt": dt, "day": int(mi["@attributes"]["MatchDay"])}

    for sc in g["TeamData"]:
        sc = sc["@attributes"]
        s = sc["Side"].lower()
        team = int(sc["TeamRef"][1:])
        d[s + "_id"] = team

        if teams:
            d[s] = teams[team].get("short") or teams[team]["full"]

        if sc["Score"] is not None:
            d[s + "_score"] = int(sc["Score"])

    return d


def games(cid=21, season=YEAR, ft=True, how="df"):
    _val(how)

    gms = bget(f"/games/{cid}/{season}")["OptaFeed"]["OptaDocument"]

    if how == "raw":
        return gms

    gms = gms["MatchData"]
    gms = [k for k in gms if
           (ft and k["MatchInfo"]["@attributes"]["Period"] == "FullTime")
           or (not ft)]

    if how == "proc":
        return gms

    ts = teams(cid, season)
    columns = ["gid", "day", "dt", "home", "home_score",
               "away_score", "away", "home_id", "away_id"]

    return pd.DataFrame([parse_game(k, ts) for k in gms],
                        columns=columns).set_index("gid")


def scorers(cid=21, season=YEAR, how="df"):
    gs = games(cid, season=season, how="raw")

    ts = {}

    for g in gs["MatchData"]:
        for t in g["TeamData"]:
            a = t["@attributes"]
            team = int(a["TeamRef"][1:])
            side = a["Side"].lower()
            goals = [{"pl": int(gl["@attributes"]["PlayerRef"][1:]),
                      "type": gl["@attributes"]["Type"].lower(),
                      "side": side} for gl in
                     t["Goal"]]

            if team not in ts:
                ts[team] = {}
            for gl in goals:
                if gl["type"] == "own":
                    continue
                if gl["type"] not in {"penalty", "goal"}:
                    print(gl["type"])
                if gl["pl"] not in ts[team]:
                    ts[team][gl["pl"]] = {"p": 0, "g": 0}
                ts[team][gl["pl"]][
                    "p" if gl["type"] == "penalty" else "g"] += 1

    if how == "raw":
        return ts

    l = []
    for t in ts:
        tn = teams(cid, season=season)[t]["full"]
        for p in ts[t]:
            pl = player(p)
            if pl:
                pl = pl.get("known") or pl.get("last")
            else:
                pl = p
            l.append({"team": tn, "player": pl,
                      "g": ts[t][p]["g"] + ts[t][p]["p"],
                      "p": ts[t][p]["p"]})

    return (
        pd.DataFrame(l, columns=["player", "team", "g", "p"])
        .sort_values("g", ascending=False)
        .reset_index(drop=True)
    )


def tab(cid=21, season=YEAR, how="df"):
    _val(how)

    f = bget(f"/table/{cid}/{season}")

    if how == "raw":
        return f

    f = f["OptaFeed"]["OptaDocument"]

    t = {k["@attributes"]["uID"]: k["nameObj"].get("short")
         or k["Name"] for k in f["Team"]}
    f = f["Competition"]["TeamStandings"]

    cols = ["Position", "Team", "Points", "Played",
            "Won", "Drawn", "Lost", "For", "Against",
            "HomeWon", "HomeDrawn", "HomeLost", "HomeFor", "HomeAgainst",
            "AwayWon", "AwayDrawn", "AwayLost", "AwayFor", "AwayAgainst",
            "RelegationAverage"]

    if type(f) is dict:
        f = f["TeamRecord"]

        l = [_add_team(r, t) for r in f]
        if how == "proc":
            return l
        else:
            return pd.DataFrame(l, columns=cols).set_index("Position")
    else:
        l = {}
        for g in f:
            gr = g["Round"]["Name"]["@value"]
            rs = g["TeamRecord"]
            l[gr] = [_add_team(r, t) for r in rs]

        if how == "proc":
            return l
        else:
            # noinspection PyUnresolvedReferences
            return pd.concat([pd.DataFrame(l[k], columns=cols)
                             .assign(Group=k)
                             .set_index(["Group", "Position"]) for k in l]
                             ).sort_index()


def refs(cid=21, season=YEAR, how="df"):
    _val(how)

    rfs = bget(f"/refs/{cid}/{season}")["OptaFeed"]["OptaDocument"][0]
    if how == "raw":
        return rfs

    l = []

    for ref in rfs["Referee"]:
        st = ref[0]["Stat"]
        d = {s["@attributes"]["Type"]: s["@value"] for s in st}
        if "games" not in d:
            continue
        for k in {"games", "fouls", "offsides", "penalties",
                  "yellow_cards", "red_cards"}:
            if k in d:
                d[k] = int(d[k])
        for k in {"cards_per_game", "fouls_per_card", "points"}:
            if k in d:
                d[k] = float(d[k])
        l.append(d)

    if how == "proc":
        return l

    cols = ["last_name", "first_name", "games", "fouls",
            "offsides", "penalties",
            "yellow_cards", "red_cards",
            "cards_per_game", "fouls_per_card",
            "points", "birth_date", "birth_place", "country"]

    return pd.DataFrame(l, columns=cols)


def lineup(gid, how="proc"):
    _val(how, {"raw", "proc"})

    mongo = {"key": {"gid": gid}, "coll": "lineups"}

    lup = bget(f"/lineup/{gid}/", mongo=mongo)["Lineup"]

    if how == "raw":
        return lup

    t = {lup["@attributes"]["away_team_id"]: lup["@attributes"][
        "away_team_name"],
         lup["@attributes"]["home_team_id"]: lup["@attributes"][
             "home_team_name"]}

    lup = lup["Team"]

    for tm in lup:
        tm["@attributes"]["name"] = t[tm["@attributes"]["id"]]

    return lup


def pmap(gid, team):

    mongo = {"key": {"gid": gid, "team": team}, "coll": "passes"}

    p = bget(f"/passes/{gid}/{team}", mongo=mongo)["OptaFeed"]["Player"]
    l = []
    fds = {"cross_lost", "cross_success", "pass_lost",
           "pass_success", "position_id"}

    for pl in p:
        name = pl["nameObj"]["known"] or pl["nameObj"]["last"]
        d = dict(pl["@attributes"], **{"player_name": name})
        for f in fds:
            d[f] = int(d[f])
        d["x"] = float(d["x"])
        d["y"] = float(d["y"])

        passes = pl["Player"]

        if type(passes) == dict:
            passes = [passes]

        d["passes"] = [dict(
            ps["@attributes"],
            **{"passes": int(ps["@value"])}
        ) for ps in passes]

        l.append(d)

    return l


def poss(gid, kind="ball", frame=5):
    kd = {"ball": "BallPossession", "terr": "Territorial",
          "thirds": "TerritorialThird"}

    mongo = {"key": {"gid": gid}, "coll": "poss"}

    ps = bget(f"/poss/{gid}", mongo=mongo)
    attrs = ps["Possession"]["@attributes"]
    teams = {"home": attrs["home_team_name"],
             "away": attrs["away_team_name"]}

    ps = ps["Possession"]["PossessionWave"]
    ps = [p for p in ps if p["@attributes"]["Type"] == kd[kind]][0][
        "Intervals"]["IntervalLength"]
    ps = [p for p in ps if int(p["@attributes"]["Type"]) == frame][0][
        "Interval"]
    l = []

    for p in ps:
        t = int(p["@attributes"]["Type"].split("-")[1])
        d = {"t": t, teams["away"]: float(p["Away"]),
             teams["home"]: float(p["Home"])}
        if kind == "thirds":
            d["Middle"] = float(p["Middle"])
        l.append(d)

    return l


def glog(gid, how="proc"):
    if type(gid) is not int:
        gid = int(gid)

    _val(how, {"raw", "proc"})

    mongo = {"key": {"gid": gid}, "coll": "games"}

    l = bget(f"/game/{gid}", mongo=mongo)

    if how == "raw":
        return l

    return l["Games"]["Game"]


def bstats(cid, season=YEAR, how="df"):
    sob = rget("FEED_F15", cid=cid, season=season)
    if how == "raw":
        return sob

    sob = sob["OptaFeed"]["OptaDocument"]

    if how == "proc":
        return sob

    l = []
    cols = [k["@attributes"]["Type"].replace(" ", "_") for k in
            sob["Team"][0]["Player"][0]["Stat"]]
    idx = ["team", "player", "pos"]

    for t in sob["Team"]:
        for p in t["Player"]:
            d = {"team": t["Name"],
                 "player": p["nameObj"].get("known") or p["Name"],
                 "pos": p["Position"]}
            for s in p["Stat"]:
                d[s["@attributes"]["Type"].replace(" ", "_")] = s["@value"]
            l.append(d)

    return pd.DataFrame(l, columns=(idx + cols)).set_index(idx)
