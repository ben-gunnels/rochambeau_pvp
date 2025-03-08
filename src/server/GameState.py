class GameState:
    def __init__(self):
        self.state = "starting"
        self.score = [0, 0]
        self.moves = ["none", "none"]
   
    def change_state(self, state: str):
        self.state = state

    def update_score(self, winner: int):
        """
            Updates the score. If player 1 wins then update score[0], otherwise update score[1]
            Params: winner (int)
        """
        self.score[winner] += 1

    def set_moves(self, move: str, player: int):
        """
            Updates the moves that players have made. 
            Params: player1 (str), player2 (str). Must be checked for valid entry: "rock", "paper", "scissors"
        """
        self.moves[player] = move

    def reset_moves(self):
        """
            Resets the moves to their original state of 'none', 'none'
        """
        self.moves = ["none", "none"]

    def decide_winner(self):
        """
            Decides the winner based on the gameplay of player 1 and player 2. Results in a tie if they choose the same.

            Returns: int, 0 -> player 1, 1 -> player 2, 2 -> draw
        """
        cases = {
            ("rock", "scissors"): 0,
            ("rock", "paper"): 1,
            ("rock", "rock"): 2,
            ("paper", "rock"): 0,
            ("paper", "scissors"): 1,
            ("paper", "paper"): 2,
            ("scissors", "paper"): 0,
            ("scissors", "rock"): 1,
            ("scissors", "scissors"): 2,
        }

        return cases[tuple(self.moves)]