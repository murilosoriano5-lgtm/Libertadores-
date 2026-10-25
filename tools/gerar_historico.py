"""Gera data/historico.csv a partir dos arquivos de uma edição (resultados + mata-mata)."""
import csv
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
ALIASES = {"Penarol": "Peñarol", "Rosário Central": "Rosario Central", "Cerro Porteno": "Cerro Porteño",
           "Independiente Del Valle": "Independiente del Valle",
           "Independiente Rivadávia": "Independiente Rivadavia"}
LEG = re.compile(r"(.+?)\s+(\d+)(?:\((\d+)\))?x(\d+)(?:\((\d+)\))?\s+(.+?)(\s+\(PR\))?$")
FIELDS = ["edicao", "fase", "rodada", "mandante", "gols_m", "gols_v", "visitante",
          "penaltis_m", "penaltis_v", "prorrogacao", "sede"]
FINAL_VENUES = {"2026": "Montevidéu"}  # sede única da final de cada edição


def rows_for(edition):
    rows, phase, rodada = [], "Fase de liga", ""
    for line in (DATA / f"edicao_{edition}_resultados.txt").read_text().splitlines():
        line = line.strip()
        if line.startswith("RODADA"):
            rodada = line.split()[1]
        elif m := LEG.match(line):
            rows.append(row(edition, phase, rodada, m))
    phase = rodada = ""
    for line in (DATA / f"edicao_{edition}_mata_mata.txt").read_text().splitlines():
        line = line.strip()
        if line in ("Oitavas", "Quartas", "Semis", "Final"):
            phase = line
        for leg in line.split(" / "):
            if m := LEG.match(leg.strip()):
                rows.append(row(edition, phase, rodada, m))
    return rows


def row(edition, phase, rodada, m):
    name = lambda n: ALIASES.get(n.strip(), n.strip())
    sede = FINAL_VENUES.get(edition, "") if phase == "Final" else ""
    return dict(edicao=edition, fase=phase, rodada=rodada, mandante=name(m[1]), gols_m=m[2], gols_v=m[4],
                visitante=name(m[6]), penaltis_m=m[3] or "", penaltis_v=m[5] or "",
                prorrogacao="sim" if m[7] else "", sede=sede)


if __name__ == "__main__":
    editions = sys.argv[1:] or ["2026"]
    with open(DATA / "historico.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, FIELDS)
        w.writeheader()
        for e in editions:
            w.writerows(rows_for(e))
