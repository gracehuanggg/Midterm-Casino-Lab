from typing import Dict
import os
import json
DB_PATH = os.path.join(os.path.dirname(__file__), "database.json")

class Player:
    def __init__(self, username: str, pw: str, balance: float, money_won: float, money_lost: float):
        self.username = username
        self.password = pw
        self.balance = balance
        self.money_won = money_won
        self.money_lost = money_lost

    def update_balance(self, amount: float) -> None:
        self.balance += amount

    def win(self, amount: float) -> None:
        self.money_won += amount
        self.update_balance(amount)
    
    def lose(self, amount: float) -> None:
        self.money_lost += amount
        self.update_balance(-amount)
        
    def get_balance(self) -> float:
        return self.balance

    def update_db(self) -> None:
        with open(DB_PATH, "r") as f:
                data = json.load(f)

        # Update this player's info
        data[self.username] = {
            "pw": self.password,
            "balance": self.balance,
            "money_won": self.money_won,
            "money_lost": self.money_lost
        }

        # Save back to JSON
        with open(DB_PATH, "w") as f:
            json.dump(data, f, indent=4)
