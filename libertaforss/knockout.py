"""Mata-mata: os 16 primeiros da tabela, jogos de ida e volta (final em jogo único)."""
from dataclasses import dataclass

# Confrontos das oitavas por posição na tabela; a ordem define a chave (lado A = 4 primeiros, lado B = 4 últimos)
ROUND_OF_16 = [(1, 16), (8, 9), (3, 14), (5, 12), (2, 15), (7, 10), (4, 13), (6, 11)]


@dataclass(frozen=True)
class Tie:
    first_leg_home: object   # time pior colocado na tabela
    second_leg_home: object  # time melhor colocado: decide em casa


def make_tie(a, b, position):
    low, high = sorted((a, b), key=lambda t: -position[t])
    return Tie(first_leg_home=low, second_leg_home=high)


def round_of_16(ranking):
    """`ranking`: times ordenados da tabela final (1º primeiro). Retorna as 8 séries das oitavas."""
    position = {t: i for i, t in enumerate(ranking, 1)}
    return [make_tie(ranking[a - 1], ranking[b - 1], position) for a, b in ROUND_OF_16]


def next_round(winners, ranking):
    """Recebe os vencedores na ordem da chave e cruza 1º x 2º, 3º x 4º...; com 2 times é a final."""
    position = {t: i for i, t in enumerate(ranking, 1)}
    return [make_tie(winners[i], winners[i + 1], position) for i in range(0, len(winners), 2)]
