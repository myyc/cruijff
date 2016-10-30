import getpass
import logging as log

import pandas as pd
from sqlalchemy import *

from .getters import get_comps, get_clubs, get_games
from .constants import YEAR


def _get_engine():
    u = "mysql+mysqldb://{user}@localhost/espn?charset=utf8"
    return create_engine(u.format(user=getpass.getuser()))


def _get_md():
    return MetaData(_get_engine())


def eq(q):
    return pd.read_sql(q, _get_engine())


def connect():
    return _get_engine().begin()


def any_table(t, action="get"):
    e = _get_engine()
    m = MetaData(e)
    name = t.name

    if action == "drop":
        if e.has_table(name):
            Table(name, m).drop()
        else:
            raise KeyError("Table '{}' not found".format(name))
    if action == "create":
        t.create(e)
    if action == "get" or action == "create":
        if e.has_table(name):
            return Table(name, m)
        else:
            raise KeyError("Table '{}' not found".format(name))


def comps_table(action="get"):
    m = _get_md()
    t = Table("comps", m,
              Column("id", Integer, primary_key=True,
                     nullable=False, autoincrement=False),
              Column("tid", Text),
              Column("name", Text),
              Column("league", Boolean),
              Column("href", Text),
              ) if action == "create" else Table("comps", m)

    if action == "fill":
        with _get_engine().begin() as conn:
            conn.execute("delete from espn.comps")
            leagues = get_comps(fmt="sql")["data"]
            cups = get_comps("cups", fmt="sql")["data"]
            q = "insert into espn.comps values (%s, %s, %s, %s, %s)"
            for r in leagues + cups:
                try:
                    conn.execute(q, r)
                except Exception as e:
                    log.warning(e)
                    pass
    else:
        return any_table(t, action)


def clubs_table(action="get", league=None, year=YEAR):
    m = _get_md()
    t = Table("clubs", m,
              Column("id", Integer, primary_key=True,
                     nullable=False, autoincrement=False),
              Column("tid", Text),
              Column("name", Text),
              Column("href", Text),
              ) if action == "create" else Table("clubs", m)

    t2 = Table("comps_year", m,
               Column("id", Integer, nullable=False, autoincrement=False),
               Column("lid", Integer, nullable=False),
               Column("year", Integer, nullable=False)
               )

    if action == "fill":
        if league is None:
            raise ValueError("'league' can not be empty for 'fill'.")
        with _get_engine().begin() as conn:
            d = get_clubs(fmt="sql", year=year, league=league)
            q = "insert into espn.clubs values (%s, %s, %s, %s)"
            q2 = "insert into espn.comps_year values (%s, %s, %s)"
            for r in d["data"]:
                try:
                    conn.execute(q2, *(r[0], league, year))
                    conn.execute(q, r)
                except Exception as e:
                    log.warning(e)
                    pass
    else:
        return any_table(t, action)


def games_table(action="get", lid=None, cid=None, year=YEAR):
    m = _get_md()
    t = Table("games", m,
              Column("id", Integer, primary_key=True,
                     nullable=False, autoincrement=False),
              Column("time", DateTime),
              Column("status", Text(length=16)),
              Column("year", Integer),
              Column("comp_id", Integer),
              Column("comp_tid", Text),
              Column("comp_name", Text),
              Column("home_id", Integer),
              Column("home_name", Text),
              Column("away_id", Integer),
              Column("away_name", Text),
              Column("home_score", Integer),
              Column("away_score", Integer),
              Column("home_score_pens", Integer),
              Column("away_score_pens", Integer),
              ) if action == "create" else Table("games", m)

    if action == "fill":
        if lid is None and cid is None:
            raise ValueError("I need at least 'lid' or 'cid'.")
        with _get_engine().begin() as conn:
            if cid is None:
                ids = cids(lid=lid, year=year)
            elif lid is None:
                ids = [cid]
                lid = 0

            for cid in ids:
                conn.execute("delete from espn.games where (away_id = %s "
                             "or home_id = %s) and comp_id = %s "
                             "and status is null", cid, cid, lid)

                # micro-optimisation
                ids = gids(cid=cid, lid=lid, year=year)

                d = get_games(fmt="sql", year=year, cid=cid, lid=lid)
                q = ("insert into espn.games values (%s, %s, %s, %s, %s, %s,"
                     " %s, %s, %s, %s, %s, %s, %s, %s, %s)")

                for r in d["data"]:
                    if r[0] in ids:
                        continue
                    try:
                        conn.execute(q, r)
                    except Exception as e:
                        log.warning(e)
                        pass
    else:
        return any_table(t, action)


def gids(lid, cid=None, year=YEAR):
    with _get_engine().begin() as conn:
        if cid is None:
            s = text("select id from espn.games "
                     "where comp_id = :c and status is not null "
                     "and year = :y")
            return {i[0] for i in conn.execute(s, c=lid, y=year).fetchall()}
        else:
            s = text("select id from espn.games "
                     "where (away_id = :p or home_id = :p) and comp_id = :c "
                     "and status is not null and year = :y")
            return {i[0] for i in conn.execute(s, p=cid, c=lid,
                                               y=year).fetchall()}


def cids(lid, year=YEAR):
    with _get_engine().begin() as conn:
        s = text("select id from espn.comps_year "
                 "where year = :y and lid = :c")
        return {i[0] for i in conn.execute(s, c=lid, y=year).fetchall()}
