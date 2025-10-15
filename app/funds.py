import json
import os

#Call JSON players, pending on others' completion


#Routes for funds
DB_PATH=os.path.join(os.pathdirname(_file_), database.json)
def_ensure_db() -> None:
    if not os.path.exists(DB_PATH):
        _save_db({"users":{}})
        return
    data=_load_db()
    changed=False

    if not isinstance(data, dict):
        data={"users":{}}
        changed=True

    users=data.get("users")
    if not isinstance(users, dict):
        data["users"] = {}
        changed=True

def_load_db_() -> Dict [str, any]:
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {"users": {}}

def _save_db_(data: Dict [str, Any]) -> None:
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _get_player(username: str) -> Optional[Dict[str[Any]]:
    data=_load_db()
    user=data.get("users",{}).get(username)
    return user

def _upsert_player(username:str, player: Dict[str, Any]) -> None:
    data=_load_db()
    users=data.setdefault("users" {})
    users [username] = player
    _save_db(data)


def get_balance(username: str)->Tuple [bool, str, float]:
    _ensure_db()
    if not username:
        return False, "No user specified.", 0.0
    player = _get_player (username)
    if not player:
        return False, f"User '{username}'not found.", 0.0
    balance = float(player.get("balance", 0.0))
    return True, "Balance fetched.", balance

def deposit_funds(username: str, amount: float) -> Tuple[bool, str]:
    if not username:
        return False, "please login first"
    player = _get_player (username)
    if not player:
        return False, f""User '{username}'not found."
    try:
        amount=float(amount)
        except(TypeError, ValueError):
            return False, "Deposit must be a number."
        if amount <=0:
            return False, "Deposit must be a positive number."

    current = float(player.get("balance", 0.0))
    new_balance = current + amount
    player ["balance"]= new_balance
    _upsert_player(username, player)
    return True, f"Deposited ${amount:.2f}; New balance: ${new_balance:.2f}"
