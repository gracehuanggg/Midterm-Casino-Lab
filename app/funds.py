import json
import os

#Call JSON players, pending on others' completion


#Routes for funds
DB_PATH=os.path.join(os.pathdirname(_file_), database.json)
def_ensure_db() -> None:

def get_balance(username: str)->Tuple [bool, str, float]:
    if not username:
        return False, "No user specified."
    player = _get_player (username)
    if not player:
        return False, f"User '{username}'not found."
    return True, "Balance fetched.", float(getattr(player, "balance", 0.0))

def deposit_funds(username: str, amount: float) -> Tuple[bool, str]:
    if not username:
        return False, "please login first"
    player = _get_player (username)
    if not player:
        return False, f""User '{username}'not found."
    if not player.deposit(amount):
        return False, f"deposit must be a positive number."
    _upsert_player(player)
    return True, f"Deposited ${float(amount):.2f}. New balance: ${player.balance:.2f}"
