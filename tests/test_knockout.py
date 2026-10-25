import re
import unittest
from collections import defaultdict
from pathlib import Path

from libertaforss.knockout import next_round, round_of_16

DATA = Path(__file__).resolve().parent.parent / "data"


def ranking_from_results():
    st = defaultdict(lambda: [0, 0, 0])  # pontos, gols pró, gols contra
    for line in (DATA / "edicao_2026_resultados.txt").read_text().splitlines():
        m = re.match(r"(.+?)\s+(\d+)x(\d+)\s+(.+)", line)
        if not m:
            continue
        for t, gf, ga in ((m[1], int(m[2]), int(m[3])), (m[4], int(m[3]), int(m[2]))):
            st[t][0] += 3 if gf > ga else int(gf == ga)
            st[t][1] += gf
            st[t][2] += ga
    return sorted(st, key=lambda t: (-st[t][0], -(st[t][1] - st[t][2]), -st[t][1], t))


class KnockoutTest(unittest.TestCase):
    def test_edition_2026_bracket(self):
        ranking = ranking_from_results()
        self.assertEqual(ranking[:3], ["Palmeiras", "Toluca", "Flamengo"])
        r16 = round_of_16(ranking)
        # (1ª partida em casa, 2ª partida em casa), na ordem da chave
        self.assertEqual([(t.first_leg_home, t.second_leg_home) for t in r16][:4], [
            ("Peñarol", "Palmeiras"), ("Estudiantes", "Club América"),
            ("Rosario Central", "Flamengo"), ("Universidad Católica", "Boca Juniors")])
        # vencedores reais das oitavas -> quartas -> semis -> final
        qf = next_round(["Palmeiras", "Estudiantes", "Flamengo", "Boca Juniors",
                         "Toluca", "Fluminense", "Cruz Azul", "Cruzeiro"], ranking)
        self.assertEqual([(t.first_leg_home, t.second_leg_home) for t in qf], [
            ("Estudiantes", "Palmeiras"), ("Boca Juniors", "Flamengo"),
            ("Fluminense", "Toluca"), ("Cruzeiro", "Cruz Azul")])
        sf = next_round(["Palmeiras", "Boca Juniors", "Toluca", "Cruz Azul"], ranking)
        self.assertEqual([(t.first_leg_home, t.second_leg_home) for t in sf], [
            ("Boca Juniors", "Palmeiras"), ("Cruz Azul", "Toluca")])


if __name__ == "__main__":
    unittest.main()
