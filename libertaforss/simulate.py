"""Simulação de resultados (gols por Poisson) e tabela de classificação."""
import math
import random
from dataclasses import dataclass

POT_RATING = {1: 1900, 2: 1750, 3: 1650, 4: 1550}
HOME_ADV = 60


def _poisson(lam, rng):
    limit, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1


def play(match, rng):
    diff = (POT_RATING[match.home.pot] - POT_RATING[match.away.pot] + HOME_ADV) / 800
    return _poisson(1.45 * math.exp(diff), rng), _poisson(1.15 * math.exp(-diff), rng)


@dataclass
class Row:
    team: object
    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    gf: int = 0
    ga: int = 0

    @property
    def points(self):
        return 3 * self.wins + self.draws

    @property
    def gd(self):
        return self.gf - self.ga


def simulate(matches, teams, seed=None):
    rng = random.Random(seed)
    table = {t: Row(t) for t in teams}
    for m in matches:
        hg, ag = play(m, rng)
        for team, gf, ga in ((m.home, hg, ag), (m.away, ag, hg)):
            r = table[team]
            r.played += 1
            r.gf += gf
            r.ga += ga
            if gf > ga:
                r.wins += 1
            elif gf == ga:
                r.draws += 1
            else:
                r.losses += 1
    return sorted(table.values(), key=lambda r: (-r.points, -r.gd, -r.gf, r.team.name))
