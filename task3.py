import random as rnd
import sys
import hashlib
import hmac
import secrets
import math
from tabulate import tabulate as tab
class KeyGen:
    @staticmethod
    def new_key():
        return secrets.token_hex(32)
class HMACGen:
    @staticmethod
    def create(key, msg):
        return hmac.new(key.encode(), msg.encode(), hashlib.sha3_256).hexdigest()
class GameRules:
    def __init__(self, moves):
        self.moves = moves
        self.n = len(moves)
        self.half = self.n // 2

    def decide(self, player, comp):
        p = self.moves.index(player)
        c = self.moves.index(comp)
        if p == c:
            return "Draw"
        elif (c > p and c - p <= self.half) or (p > c and p - c > self.half):
            return "Lose"
        else:
            return "Win"
class HelpMenu:
    def __init__(self, moves):
        self.moves = moves

    def show(self):
        header = ["PC/User"] + self.moves
        game = GameRules(self.moves)
        rows = []
        for pc_move in self.moves:
            row = [pc_move]
            for user_move in self.moves:
                row.append(game.decide(pc_move, user_move))
            rows.append(row)
        print(tab(rows, headers=header, tablefmt="grid"))
def validate(moves):
    if not moves:
        print("Usage: python game.py move1 move2 ...")
        sys.exit()
    if len(moves) < 3:
        print("At least 3 moves required.")
        sys.exit()
    if len(moves) % 2 == 0:
        print("Number of moves must be odd.")
        sys.exit()
    if len(moves) != len(set(moves)):
        print("Moves must be unique.")
        sys.exit()
def main():
    moves = sys.argv[1:]
    validate(moves)
    secret_key = KeyGen.new_key()
    comp_move = rnd.choice(moves)
    hmac_code = HMACGen.create(secret_key, comp_move)
    print(f"HMAC: {hmac_code}")
    move_dict = {i+1: m for i, m in enumerate(moves)}
    for num, mv in move_dict.items():
        print(f"{num} - {mv}")
    print("0 - exit")
    print("? - help")
    choice = input("Your move: ")
    if choice == '0':
        sys.exit("Goodbye!")
    elif choice == '?':
        HelpMenu(moves).show()
        return
    try:
        choice_num = int(choice)
        user_move = move_dict[choice_num]
        print(f"Your move: {user_move}")
        print(f"Computer move: {comp_move}")

        result = GameRules(moves).decide(user_move, comp_move)
        print({"Win": "You win!", "Lose": "Computer wins!", "Draw": "It's a draw!"}[result])
        print(f"HMAC key: {secret_key}")
    except (ValueError, KeyError):
        print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()