"""Divide os 144 jogos em 8 rodadas de 18 (cada time joga 1x por rodada)."""
import random
from itertools import combinations


def _color_edges(matches, rng, limit=3_000):
    """Coloração de arestas por backtracking (escolhe sempre a aresta com menos cores livres)."""
    n_rounds = 8
    used = {}  # time -> set de rodadas ocupadas
    for m in matches:
        used.setdefault(m.home, set())
        used.setdefault(m.away, set())
    color = {}
    steps = [0]

    def free(m):
        return [c for c in range(n_rounds) if c not in used[m.home] and c not in used[m.away]]

    def solve(pending):
        if not pending:
            return True
        steps[0] += 1
        if steps[0] > limit:
            return False
        m = min(pending, key=lambda x: len(free(x)))
        options = free(m)
        rng.shuffle(options)
        rest = [p for p in pending if p is not m]
        for c in options:
            color[m] = c
            used[m.home].add(c)
            used[m.away].add(c)
            if solve(rest):
                return True
            used[m.home].discard(c)
            used[m.away].discard(c)
            del color[m]
        return False

    return color if solve(list(matches)) else None


def _venue_table(rounds):
    """Para cada time, uma tupla de 8 booleanos: jogou em casa na rodada?"""
    table = {}
    for r, rd in enumerate(rounds):
        for m in rd:
            table.setdefault(m.home, [None] * len(rounds))[r] = True
            table.setdefault(m.away, [None] * len(rounds))[r] = False
    return list(table.values())


def _penalty(table, order):
    """Penaliza 3+ jogos seguidos em casa ou fora (quanto menor, melhor)."""
    penalty = 0
    for venues in table:
        streak, last = 0, None
        for r in order:
            streak = streak + 1 if venues[r] == last else 1
            last = venues[r]
            if streak >= 3:
                penalty += streak - 2
    return penalty


def _best_order(table, rng, restarts=30):
    """Busca local: parte de ordens aleatórias e troca rodadas de lugar enquanto melhorar."""
    best = None
    for _ in range(restarts):
        order = list(range(8))
        rng.shuffle(order)
        score = _penalty(table, order)
        improved = True
        while improved and score:
            improved = False
            for i, j in combinations(range(8), 2):
                order[i], order[j] = order[j], order[i]
                new = _penalty(table, order)
                if new < score:
                    score, improved = new, True
                else:
                    order[i], order[j] = order[j], order[i]
        if best is None or score < best[1]:
            best = (list(order), score)
    return best


def split_rounds(matches, seed=None, colorings=20):
    """Retorna 8 listas de 18 jogos, escolhendo a divisão/ordem com menos sequências longas em casa ou fora."""
    rng = random.Random(seed)
    best = None
    for _ in range(colorings):
        color = None
        while color is None:
            color = _color_edges(matches, rng)
        rounds = [[m for m in matches if color[m] == c] for c in range(8)]
        table = _venue_table(rounds)
        order, score = _best_order(table, rng)
        if best is None or score < best[0]:
            best = (score, [rounds[i] for i in order])
    return best[1]
