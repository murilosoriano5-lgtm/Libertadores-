"""Sorteio dos jogos: cada time joga 2x contra cada pote (1 em casa, 1 fora)."""
import random
from dataclasses import dataclass
from itertools import combinations

from .teams import Team


@dataclass(frozen=True)
class Match:
    home: Team
    away: Team


def _find_permutation(sources, targets, forbidden, rng):
    """Backtracking aleatório: liga cada source a um target distinto sem violar `forbidden`."""
    sources = list(sources)
    result = {}
    used = set()

    def solve(i):
        if i == len(sources):
            return True
        s = sources[i]
        options = [t for t in targets if t not in used and not forbidden(s, t)]
        rng.shuffle(options)
        for t in options:
            result[s] = t
            used.add(t)
            if solve(i + 1):
                return True
            used.discard(t)
            del result[s]
        return False

    return result if solve(0) else None


def _draw_once(teams, rng):
    pots = {p: [t for t in teams if t.pot == p] for p in sorted({t.pot for t in teams})}
    matches = []
    same_country = lambda a, b: a.country == b.country

    # Mesmo pote: cada time recebe 1 e visita 1 (adversários diferentes, sem confronto de ida e volta)
    for pot in pots.values():
        perm = _find_permutation(
            pot, pot, lambda a, b: a == b or same_country(a, b), rng)
        if perm is None:
            return None
        if any(perm[perm[a]] == a for a in pot):  # evita pares de 2 ciclos (A x B e B x A)
            return None
        matches += [Match(h, a) for h, a in perm.items()]

    # Potes diferentes: duas permutações (mandante / visitante) com adversários distintos
    for i, j in combinations(pots, 2):
        host = _find_permutation(pots[i], pots[j], same_country, rng)
        if host is None:
            return None
        visit = _find_permutation(
            pots[i], pots[j], lambda a, b: same_country(a, b) or host[a] == b, rng)
        if visit is None:
            return None
        matches += [Match(a, b) for a, b in host.items()]    # time do pote i joga em casa
        matches += [Match(b, a) for a, b in visit.items()]   # time do pote i joga fora
    return matches


def generate_fixtures(teams, seed=None, max_tries=1000):
    """Gera os 144 jogos da fase de liga. Mesmo `seed` => mesmo sorteio."""
    rng = random.Random(seed)
    for _ in range(max_tries):
        matches = _draw_once(teams, rng)
        if matches:
            return matches
    raise RuntimeError("Não foi possível gerar um sorteio válido")
