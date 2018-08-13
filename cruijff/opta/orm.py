from cruijff.constants import RED, YEAR


class Competition:
    def __init__(self, id, full, short=None, abbr=None, season=YEAR):
        self.id = id
        self.full = full
        self.short = short
        self.abbr = abbr
        self.season = season

    def __repr__(self):
        if self.short:
            return f"{self.short} ({self.id})"
        else:
            return f"{self.full} ({self.id})"

    def _repr_html_(self):
        g = lambda x, y: f"<b><span style='color: {RED}'>{x}</span></b> ({y})"
        if self.short:
            return g(self.short, self.id)
        else:
            return g(self.full, self.id)

    def teams(self):
        from .blvd import teams
        return teams(self.id, self.season)

    def tab(self, **kwargs):
        from .blvd import tab
        return tab(self.id, self.season, **kwargs)

    def games(self, **kwargs):
        from .blvd import games
        return games(self.id, self.season, **kwargs)

    def scorers(self, **kwargs):
        from .blvd import scorers
        return scorers(self.id, self.season, **kwargs)
