import unittest

from libertaforss.history import head_to_head, load_history


class HistoryTest(unittest.TestCase):
    def test_2026(self):
        games = load_history()
        self.assertEqual(len(games), 173)  # 144 da liga + 29 do mata-mata
        played, wins, goals = head_to_head("Palmeiras", "Toluca", games)
        self.assertEqual(len(played), 1)
        self.assertEqual((played[0]["fase"], played[0]["sede"], played[0]["prorrogacao"]),
                         ("Final", "Montevidéu", "sim"))
        self.assertEqual((wins["Palmeiras"], goals["Palmeiras"], goals["Toluca"]), (1, 2, 1))
        # pênaltis são guardados à parte; o placar do jogo continua sendo o dos 90'/120'
        pens = [g for g in games if g["penaltis_m"]]
        self.assertEqual(len(pens), 4)


if __name__ == "__main__":
    unittest.main()
