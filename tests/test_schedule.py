import unittest

from libertaforss.draw import generate_fixtures
from libertaforss.schedule import split_rounds
from libertaforss.teams import TEAMS


class ScheduleTest(unittest.TestCase):
    def test_rounds(self):
        ms = generate_fixtures(TEAMS, 1)
        rounds = split_rounds(ms, 1, colorings=3)
        self.assertEqual([len(r) for r in rounds], [18] * 8)
        self.assertEqual(sorted(map(id, (m for r in rounds for m in r))), sorted(map(id, ms)))
        for rd in rounds:  # cada time joga exatamente 1x por rodada
            playing = [t for m in rd for t in (m.home, m.away)]
            self.assertEqual(len(set(playing)), 36)


if __name__ == "__main__":
    unittest.main()
