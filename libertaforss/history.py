"""Histórico de confrontos entre os times, lido de data/historico.csv."""
import csv
from pathlib import Path

HISTORY = Path(__file__).resolve().parent.parent / "data" / "historico.csv"


def load_history(path=HISTORY):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def head_to_head(a, b, games):
    """Jogos entre a e b e o resumo (vitórias de cada um, empates e gols)."""
    played = [g for g in games if {g["mandante"], g["visitante"]} == {a, b}]
    wins = {a: 0, b: 0, "empates": 0}
    goals = {a: 0, b: 0}
    for g in played:
        hg, ag = int(g["gols_m"]), int(g["gols_v"])
        goals[g["mandante"]] += hg
        goals[g["visitante"]] += ag
        if hg == ag:
            wins["empates"] += 1
        else:
            wins[g["mandante"] if hg > ag else g["visitante"]] += 1
    return played, wins, goals


def describe(g):
    pens = f" (pên. {g['penaltis_m']}-{g['penaltis_v']})" if g["penaltis_m"] else ""
    extra = " [prorrogação]" if g["prorrogacao"] else ""
    sede = f" - sede: {g['sede']}" if g["sede"] else ""
    where = g["fase"] + (f", rodada {g['rodada']}" if g["rodada"] else "")
    return f"{g['edicao']} {where}: {g['mandante']} {g['gols_m']}x{g['gols_v']} {g['visitante']}{pens}{extra}{sede}"
