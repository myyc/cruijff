from .metadata import types as mt, qual as mq
from .blvd import mc, player, glog


mconn = mc()


def _pn(v):
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


def jevs(gs, fev=None):
    ls = {"Involved", "Jersey number", "Player position", "Resume",
          "Team player formation"}
    evs = []
    i = 0
    qm = {}
    for g in gs:
        ga = g["@attributes"]
        comp = ga["compObj"]
        cname = comp["short"] or comp["full"]
        cid = int(ga["competition_id"])

        gatt = {"season": ga["season_id"], "gid": ga["id"],
                "comp": cname, "cid": cid}

        for e in g["Event"]:
            d = {}
            ea = e["@attributes"]
            pid = int(ea["player_id"])
            if fev is not None and fev(e) is False:
                continue
            if ea["type_id"] == "43":
                continue

            pn = player(int(e["@attributes"]["player_id"]), mconn=mconn)

            if pn is not None:
                pn = pn.get("known") or pn["last"]
                d["player"] = pn
            et = int(ea["type_id"])

            et = mt[et]["name"] if et in mt else str(et)

            d.update(pid=pid, event=et, x=ea["x"], y=ea["y"],
                     tid=int(ea["team_id"]), p=int(ea["period_id"]),
                     m=int(ea["min"]), s=int(ea["sec"]), eid=int(ea["id"]))
            d.update(**gatt)

            qs = {}
            for q in e["Q"]:
                qid = int(q["@attributes"]["qualifier_id"])
                qname = str(qid) if qid not in mq else mq.get(qid)["name"]
                val = q["@attributes"]["value"]
                val = _pn(val)
                if et == 34 and qname in ls:
                    val = [int(v) for v in val.split(", ")]
                if qid not in mq:
                    if qid not in qm:
                        qm[qid] = set()
                    qm[qid].add(q["@attributes"]["value"])
                qs[qname] = val
            d["q"] = qs

            evs.append(d)
        i += 1
    return evs


def mimport_events(df):
    """
    :param df: A dataframe from `games()`
    :return:
    """
    gs = df.index
    coll = mc().get_collection("events_proc")

    for i, g in enumerate(gs, 1):
        g = int(g)
        d = coll.find_one({"gid": g})
        if d is None:
            coll.insert_many(jevs([glog(g)]))
            print(f"Processed {i}/{len(gs)}")
