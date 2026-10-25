import unittest
from collections import Counter

from libertaforss.draw import generate_fixtures
from libertaforss.teams import TEAMS


class DrawTest(unittest.TestCase):
    def test_structure(self):
        for seed in range(20):
            ms = generate_fixtures(TEAMS, seed)
            self.assertEqual(len(ms), 144)
            for t in TEAMS:
                home = [m.away for m in ms if m.home == t]
                away = [m.home for m in ms if m.away == t]
                self.assertEqual((len(home), len(away)), (4, 4))
                self.assertEqual(len(set(home + away)), 8)  # 8 adversários diferentes
                for pot in (1, 2, 3, 4):
                    self.assertEqual(sum(o.pot == pot for o in home), 1)
                    self.assertEqual(sum(o.pot == pot for o in away), 1)
                self.assertTrue(all(o.country != t.country for o in home + away))

    def test_deterministic(self):
        self.assertEqual(generate_fixtures(TEAMS, 7), generate_fixtures(TEAMS, 7))

    def test_data(self):
        self.assertEqual(len(TEAMS), 36)
        self.assertEqual(Counter(t.pot for t in TEAMS), {1: 9, 2: 9, 3: 9, 4: 9})


if __name__ == "__main__":
    unittest.main()
