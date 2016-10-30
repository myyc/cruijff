import re
import fnmatch

from .constants import YEAR
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
    def __init__(self, id_, name, tid, lid):
        self.id = id_
        self.name = name
        self.tid = tid

        self.league = leagues(lid)

    def __repr__(self):
        return "{} ({}) – {}".format(self.name, self.id, self.tid)

    def _repr_html_(self):
        return ("{} <b style='color: #de143d'>{}</b>"
                "<br/><em>{}</em><br/>"
                "{}"
                ).format(self.id, self.name, self.tid, self.league.name)

    def games(self, year=YEAR):
        return eq("select * from games where (away_id = {} or home_id = {}) "
                  "and year = {}".format(self.id, self.id, year))


def _matchdf(df, p, cols=None):
    p = re.compile(fnmatch.translate(p), re.IGNORECASE)
    df = df.groupby(level=0).first()
    idxs = (df[cols] if cols else df).apply(lambda x: x.str.match(p)).sum(
        axis=1).astype("bool")
    return df[idxs]


def clubs(p, year=YEAR):
    if type(p) is int:
        cbs = eq("select c.id, c.tid, c.name, cy.lid from clubs c "
                 "join comps_year cy on c.id = cy.id "
                 "join comps cs on cs.id = cy.lid "
                 "where c.id = {} and cy.year = {} and league = 1".format(p,
                                                                          year)).set_index(
            "id")
    elif type(p) is str:
        cbs = _matchdf(eq("select c.id, c.tid, c.name, cy.lid from clubs c "
                          "join comps_year cy on c.id = cy.id "
                          "join comps cs on cs.id = cy.lid "
                          "where year = {} and league = 1".format(
            year)).set_index("id"), p,
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
    if type(p) is int:
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
