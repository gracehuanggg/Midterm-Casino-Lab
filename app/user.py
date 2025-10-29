import json
import os
import secrets
import hashlib
from typing import Dict, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "database.json")

class UserManager:

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DB_PATH

    def _load_db(self) -> Dict:
        with open(self.db_path, "r") as f:
            return json.load(f)

    def _save_db(self, data: Dict) -> None:
        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=2)

    def register(self, username: str, password: str, preferred_name: Optional[str] = None) -> bool:


        username = username.strip()
        if not username or not password:
            return False

        db = self._load_db()
        users = db.setdefault("users", {})
        if username in users:
            return False

        users[username] = {
            "pw": password,
            "preferred_name": preferred_name,
            "balance": 100,
            "money_won": 0,
            "money_lost": 0
        }

        self._save_db(db)
        return True

    def authenticate(self, username: str, password: str) -> bool:
        db = self._load_db()
        users = db.get("users", {})

        if username in users and users[username]["pw"] == password:
            return True
        return False

def get_user(self, username: str) -> Optional[Dict]:
    db = self._load_db()
    return db.get("users", {}).get(username)
