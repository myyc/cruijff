import fnmatch
import re
from datetime import datetime

import pandas as pd

from cruijff.constants import YEAR
from .dbutils import eq


class League:
    def __init__(self, id_, name, tid):
        self.id = id_
        self.name = name
        self.tid = tid

    def __repr__(self):
        return "{} ({}) – {}".format(self.name, self.id, self.tid)

    def _repr_html_(self):
        return "{} <b style='color: #de143d'>{}</b><br/><em>{}</em>".format(
            self.id, self.name, self.tid)

    def games(self, year=YEAR):
        return eq("select * from games where comp_id = {} "
                  "and year = {}".format(self.id, year))


class Club:
    def __init__(self, id_, name, tid, lid=None):
        self.id = id_
        self.name = name
        self.tid = tid

        if lid is not None:
            self.league = leagues(lid)
        else:
            self.league = None

    def __repr__(self):
        return "{} ({}) – {}".format(self.name, self.id, self.tid)

    def _repr_html_(self):
        return ("{} <b style='color: #de143d'>{}</b>"
                "<br/><em>{}</em>{}"
                ).format(self.id, self.name, self.tid,
                         "<br/>" + self.league.name if self.league else "")

    def games(self, year=YEAR):
        return eq("select * from games where (away_id = {} or home_id = {}) "
                  "and year = {}".format(self.id, self.id, year))


class Game:
    def __init__(self, id_=None, time=None, status=None, year=None,
                 comp_id=None,
                 comp_name=None, home_id=None, home_name=None,
                 away_id=None, away_name=None,
                 home_score=None, away_score=None,
                 home_score_pens=None, away_score_pens=None,
                 **kwargs):
        self.id = id_ or kwargs.get("id")

        if type(time) is pd.tslib.Timestamp:
            self.time = time.to_pydatetime()
        elif type(time) is str:
            self.time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        else:
            raise TypeError(type(time))

        self.status = "Upcoming" if status is None else status
        self.year = int(year)

        if comp_id == -1:
            self.league = League(0, comp_name, "unidentified")
        else:
            self.league = leagues(int(comp_id))

        if home_id == -1:
            self.home = Club(0, home_name, "unidentified")
        else:
            self.home = clubs(int(home_id))

        if away_id == -1:
            self.away = Club(0, away_name, "unidentified")
        else:
            self.away = clubs(int(away_id))

        if home_score is not None:
            self.score = {"h": int(home_score), "a": int(away_score)}
            if home_score_pens is not None:
                self.score["hp"] = int(home_score_pens)
                self.score["ap"] = int(away_score_pens)
        else:
            self.score = None

    @staticmethod
    def from_db(g):
        if type(g) is not int:
            raise TypeError(type(g))
        game = eq("select * from games where id = {} limit 1".format(g))
        if len(game) != 1:
            raise ValueError(game)
        return Game(**game.iloc[0])

    def __repr__(self):
        if self.score and not "hp" in self.score:
            return "{} {} - {} {}".format(self.home.name, self.score["h"],
                                          self.score["a"], self.away.name)
        elif "hp" in self.score:
            return "{} {} ({}) - ({}) {} {}".format(self.home.name,
                                                    self.score["h"],
                                                    self.score["hp"],
                                                    self.score["ap"],
                                                    self.score["a"],
                                                    self.away.name)

        else:
            return "{} _ - _ {}".format(self.home.name, self.away.name)


def _matchdf(df, p, cols=None):
    p = re.compile(fnmatch.translate(p), re.IGNORECASE)
    df = df.groupby(level=0).first()
    idxs = (df[cols] if cols else df).apply(lambda x: x.str.match(p)).sum(
        axis=1).astype("bool")
    return df[idxs]


def clubs(p, year=YEAR):
    if type(p) is Club:
        return p
    elif type(p) is int:
        cbs = eq("select c.id, c.tid, c.name, cy.lid from clubs c "
                 "join comps_year cy on c.id = cy.id "
                 "join comps cs on cs.id = cy.lid "
                 "where c.id = {} and cy.year = {} "
                 "and league = 1".format(p, year)).set_index("id")
    elif type(p) is str:
        cbs = _matchdf(eq("select c.id, c.tid, c.name, cy.lid from clubs c "
                          "join comps_year cy on c.id = cy.id "
                          "join comps cs on cs.id = cy.lid "
                          "where year = {} "
                          "and league = 1".format(year)).set_index("id"),
                       p,
                       cols=["tid", "name"])
    else:
        raise TypeError(type(p))

    if len(cbs) == 1:
        cbs = cbs.iloc[0]
        return Club(int(cbs.name), cbs["name"], cbs["tid"], int(cbs["lid"]))
    elif len(cbs) == 0:
        return None

    return cbs


def leagues(p=None):
    if type(p) is League:
        return p
    elif type(p) is int:
        cps = eq("select id, tid, name from comps where id = {}".format(
            p)).set_index("id").groupby(level=0).first()
    elif type(p) is str or p is None:
        cps = eq("select id, tid, name from comps").set_index("id")
        if p is not None:
            cps = _matchdf(cps, p)
    else:
        raise TypeError(type(p))

    if len(cps) == 1:
        cps = cps.iloc[0]
        return League(int(cps.name), cps["name"], cps["tid"])
    elif len(cps) == 0:
        return None

    return cps
