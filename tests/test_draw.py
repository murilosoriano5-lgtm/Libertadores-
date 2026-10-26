import unittest
from collections import Counter

from libertaforss.draw import generate_fixtures
from libertaforss.teams import EDITIONS


class DrawTest(unittest.TestCase):
    def test_structure(self):
        for edition, teams in EDITIONS.items():
            for seed in range(20):
                ms = generate_fixtures(teams, seed)
                self.assertEqual(len(ms), 144, edition)
                for t in teams:
                    home = [m.away for m in ms if m.home == t]
                    away = [m.home for m in ms if m.away == t]
                    self.assertEqual((len(home), len(away)), (4, 4))
                    self.assertEqual(len(set(home + away)), 8)  # 8 adversários diferentes
                    for pot in (1, 2, 3, 4):
                        self.assertEqual(sum(o.pot == pot for o in home), 1)
                        self.assertEqual(sum(o.pot == pot for o in away), 1)
                    self.assertTrue(all(o.country != t.country for o in home + away))

    def test_deterministic(self):
        teams = EDITIONS["2027"]
        self.assertEqual(generate_fixtures(teams, 7), generate_fixtures(teams, 7))

    def test_data(self):
        for teams in EDITIONS.values():
            self.assertEqual(len(teams), 36)
            self.assertEqual(len({t.name for t in teams}), 36)
            self.assertEqual(Counter(t.pot for t in teams), {1: 9, 2: 9, 3: 9, 4: 9})


if __name__ == "__main__":
    unittest.main()
