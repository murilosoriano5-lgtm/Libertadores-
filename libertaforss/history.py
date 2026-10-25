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


def _winner(g):
    """Vencedor de um jogo (pênaltis desempatam); None se terminou empatado sem pênaltis."""
    hg, ag = int(g["gols_m"]), int(g["gols_v"])
    if hg == ag and g["penaltis_m"]:
        hg, ag = int(g["penaltis_m"]), int(g["penaltis_v"])
    return g["mandante"] if hg > ag else g["visitante"] if ag > hg else None


def all_time_ranking(games):
    """Ranking histórico: pontos (3/1/0), saldo, gols pró; títulos e vice vêm das finais."""
    rows = {}
    stat = lambda t: rows.setdefault(t, dict(team=t, j=0, v=0, e=0, d=0, gp=0, gc=0, titulos=0, vices=0))
    for g in games:
        hg, ag = int(g["gols_m"]), int(g["gols_v"])
        for team, gf, ga in ((g["mandante"], hg, ag), (g["visitante"], ag, hg)):
            s = stat(team)
            s["j"] += 1
            s["gp"] += gf
            s["gc"] += ga
            s["v" if gf > ga else "e" if gf == ga else "d"] += 1
        if g["fase"] == "Final" and (champion := _winner(g)):
            runner_up = g["visitante"] if champion == g["mandante"] else g["mandante"]
            stat(champion)["titulos"] += 1
            stat(runner_up)["vices"] += 1
    for s in rows.values():
        s["pts"] = 3 * s["v"] + s["e"]
        s["sg"] = s["gp"] - s["gc"]
    return sorted(rows.values(), key=lambda s: (-s["pts"], -s["sg"], -s["gp"], s["team"]))
