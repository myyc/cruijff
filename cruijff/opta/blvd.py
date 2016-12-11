import zlib
import base64
import json
import re
import fnmatch
from datetime import datetime, timezone, timedelta

import requests
from redis import Redis
import pandas as pd

from ..constants import YEAR


def _val(v, s=None):
    if s is None:
        s = {"raw", "proc", "df"}
    if v not in s:
        raise ValueError(v)


def _dec(s):
    return zlib.decompress(base64.b64decode(s)).decode("utf-8")


def _get(url):
    r = Redis()
    if url in r:
        return json.loads(r[url].decode("utf-8"))

    j = requests.get("http://127.0.0.1:9080" + url).text
    if j:
        j = _dec(j)
        r[url] = j
        exp = 3600 if "err" not in j else 5
        r.expire(url, exp)

    return json.loads(j)


def _add_team(r, teams):
    s = r["Standing"]
    s["Team"] = teams[r["@attributes"]["TeamRef"]]
    return s


def rget(feed, season=YEAR, cid="null", team="null", gid="null",
         player="null"):
    url = "/f/{}/{}/{}/{}/{}".format(feed, season, cid, team, gid, player)

    return _get(url)


def comps(match=None, season=YEAR, raw=False):
    url = "/comps/{}".format(season)
    j = _get(url)

    if match is not None:
        rxp = re.compile(fnmatch.translate(match),
                         flags=re.IGNORECASE)
        j = [c for c in j if rxp.match(c.get("full"))]

    if raw:
        return j
    else:
        return (
            pd.DataFrame(j, columns=["id", "full", "short", "abbr"])
            .set_index("id").sort_index()
        )


def clubs(cid, season=YEAR):
    url = "/clubs/{}/{}".format(cid, season)

    j = _get(url)
    return {int(d["id"]): {k: d[k] for k in d if k != "id"} for d in j}


def stats(cid, team, season=YEAR):
    url = "/stats/{}/{}/{}".format(cid, team, season)

    return _get(url)


def parse_game(g, teams=None):
    mi = g["MatchInfo"]

    fmt1 = "%Y-%m-%dT%H:%M:%S.%fZ"
    fmt2 = "%Y-%m-%d %H:%M:%S"

    gid = int(g["@attributes"]["uID"][1:])

    dt = datetime.strptime(mi["dateObj"]["utc"], fmt1) + timedelta(hours=1)
    # noinspection PyTypeChecker
    dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime(fmt2)

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

    gms = _get(f"/games/{cid}/{season}")["OptaFeed"]["OptaDocument"]

    if how == "raw":
        return gms

    gms = gms["MatchData"]
    gms = [k for k in gms if
           ft and k["MatchInfo"]["@attributes"]["Period"] == "FullTime"]

    if how == "proc":
        return gms

    teams = clubs(cid, season)
    columns = ["gid", "day", "dt", "home", "home_score",
               "away_score", "away", "home_id", "away_id"]

    return pd.DataFrame([parse_game(k, teams) for k in gms],
                        columns=columns).set_index("gid")


def tab(cid=21, season=YEAR, how="df"):
    _val(how)

    f = _get(f"/table/{cid}/{season}")

    if how == "raw":
        return f

    f = f["OptaFeed"]["OptaDocument"]

    t = {k["@attributes"]["uID"]: k.get("short") or k["Name"] for k in
         f["Team"]}
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

    rfs = _get(f"/refs/{cid}/{season}")["OptaFeed"]["OptaDocument"][0]
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

    lup = _get(f"/lineup/{gid}/")["Lineup"]

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
    p = _get(f"/passes/{gid}/{team}")["OptaFeed"]["Player"]
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
        # uncomment to get the actual passes
        d["passes"] = pl["Player"]
        l.append(d)

    return l


def poss(gid, kind="ball", frame=5):
    kd = {"ball": "BallPossession", "terr": "Territorial",
          "thirds": "TerritorialThird"}

    ps = _get(f"/poss/{gid}")
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
