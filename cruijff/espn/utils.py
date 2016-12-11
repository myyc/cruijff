from hashlib import sha256
import json
from functools import wraps

from redis import StrictRedis


def cache(f):
    @wraps(f)
    def g(*args, **kwargs):
        r = StrictRedis()
        force = kwargs.pop("force") if "force" in kwargs else False

        key = json.dumps({"func": f.__name__,
                          "args": repr(args),
                          "kwargs": repr(kwargs)})
        key = sha256(key.encode("utf-8")).hexdigest()

        if force and key in r:
            del r[key]
        if key in r:
            return json.loads(r[key].decode("utf-8"))

        l = f(*args, **kwargs)

        r[key] = json.dumps(l)
        r.expire(key, 86400)

        return l

    return g


def legit_header():
    ua = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246")
    return {"User-Agent": ua}
