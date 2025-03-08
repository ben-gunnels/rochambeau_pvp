# test_my_module.py
import unittest
from .GameState import GameState

class GameStateTest(unittest.TestCase):
    def setUp(self):
        self.gamestate = GameState()

    def test_change_state(self):
        self.gamestate.change_state("playing")
        self.assertEqual(self.gamestate.state, "playing")

    def test_update_score(self):
        score = self.gamestate.score[0]
        self.gamestate.update_score(0)
        self.assertEqual(self.gamestate.score[0], score + 1)

    def test_decide_winner(self):
        self.assertEqual(self.gamestate.decide_winner(("rock", "scissors")),     0)
        self.assertEqual(self.gamestate.decide_winner(("rock", "paper")),        1)
        self.assertEqual(self.gamestate.decide_winner(("rock", "rock")),         2)
        self.assertEqual(self.gamestate.decide_winner(("paper", "rock")),        0)
        self.assertEqual(self.gamestate.decide_winner(("paper", "scissors")),    1)
        self.assertEqual(self.gamestate.decide_winner(("paper", "paper")),       2)
        self.assertEqual(self.gamestate.decide_winner(("scissors", "paper")),    0)
        self.assertEqual(self.gamestate.decide_winner(("scissors", "rock")),     1)
        self.assertEqual(self.gamestate.decide_winner(("scissors", "scissors")), 2)

if __name__ == '__main__':
    unittest.main()