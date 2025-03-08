import socket
import struct
from .config import (HOST, PORT, PLAYERS, BUFFER, ROUNDS)
from .GameState import GameState
from lib.MessagePasser import MessagePasser


class Server:
    def __init__(self):
        self.messenger = MessagePasser()
        self.gamestate = GameState()

        self.players = []

        self.create()

        print("Server starting up....")

    def create(self):
        # Create a TCP socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.server.bind((HOST, PORT))
        self.server.listen(PLAYERS)  # Listen for up to PLAYERS players

    def wait_for_players(self):
        while (len(self.players) < PLAYERS):
            conn, addr = self.server.accept()
            self.players.append(conn)
            print(f"Player {len(self.players)} connected from {addr}")
            conn.sendall(f"You are Player {len(self.players)}\n".encode())

        print(f"All players in session... Game is starting!")

    def wait_for_player_response(self):
        players_responded = set()

        quick_translate = {
            "rock": "rock", 
            "r": "rock",
            "paper": "paper",
            "p": "paper",
            "scissors": "scissors",
            "s": "scissors"
        }

        while self.gamestate.state == "rochambeau": # Players are making their move
            for i, conn in enumerate(self.players):
                try:
                    if conn in players_responded:
                        continue

                    data = self.messenger.receive_message(conn)

                    # Player disconnected
                    if not data:
                        print(f"Player {i+1} disconnected.")
                        conn.close()
                        break
                    
                    print(f"Player {i+1}: {data}")

                    if (data.lower().strip() not in set(["rock", "paper", "scissors", "r", "p", "s"])):
                        message = "Please enter a valid move: rock, paper, scissors\n"
                        self.messenger.send_message(conn, message)
                    
                    else:
                        players_responded.add(conn)
                        move = quick_translate[data.lower().strip()]
                        self.gamestate.set_moves(move, i)
                        if not any(map(lambda x: x == "none", self.gamestate.moves)):
                            self.gamestate.change_state("decide-outcome")
                except: 
                    break

    def decide_outcome(self):
        outcome = self.gamestate.decide_winner()

        if outcome == 0:
            m1 = f"You win! {self.gamestate.moves[0]} beats {self.gamestate.moves[1]}\n"
            m2 = f"You Lose! {self.gamestate.moves[1]} gets beaten by {self.gamestate.moves[0]}\n"
            # Send respective messages
            self.messenger.send_message(self.players[0], m1)
            self.messenger.send_message(self.players[1], m2)
        
        elif outcome == 1:
            m1 = f"You win! {self.gamestate.moves[1]} beats {self.gamestate.moves[0]}\n"
            m2 = f"You Lose! {self.gamestate.moves[0]} gets beaten by {self.gamestate.moves[1]}\n"
            # Send respective messages
            self.messenger.send_message(self.players[1], m1)
            self.messenger.send_message(self.players[0], m2)
        
        else: # Tie
            m = f"It's a draw!\n"
            # Send the same message
            self.messenger.send_message(self.players[0], m)
            self.messenger.send_message(self.players[1], m)
        
        self.gamestate.change_state("rochambeau")


    def game_loop(self):
         while (all(map(lambda x: x < (ROUNDS + 1) / 2, self.gamestate.score))):
            message = "Players! Shoot either rock, paper, or scissors\n"
            for player in self.players:
                self.messenger.send_message(player, message)
            self.wait_for_player_response()
            self.decide_outcome()
            
    def run(self):
        self.gamestate.change_state("waiting-for-players")
        self.wait_for_players()
        self.gamestate.change_state("rochambeau")
        self.game_loop()

        winner = "Player 1 Wins!" if self.gamestate.score[0] > self.gamestate.score[1] else "Player 2 Wins!"

        for player in self.players:
            self.messenger.send_message(player, winner)

        self.server.close()

def main():
    server = Server()

    server.run()

if __name__ == "__main__":
    main()