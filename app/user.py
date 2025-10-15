import json
import os
import secrets
import hashlib
from typing import Dict, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "database.json")

class UserManager:

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DB_PATH
        self._ensure_db()

    def _ensure_db(self) -> None:
        if not os.path.exists(self.db_path):
            self._save_db({"users": {}})
        else:
            data = self._load_db()
            if not isinstance(data, dict) or "users" not in data:
                self._save_db({"users": {}})
                return
            users = data.get("users", {})
            changed = False
            for uname, record in list(users.items()):
                if not isinstance(record, dict) or "pw" not in record:
                    users.pop(uname)
                    changed = True
            if changed:
                data["users"] = users
                self._save_db(data)

    def _load_db(self) -> Dict:
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"users": {}}

    def _save_db(self, data: Dict) -> None:
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _hash_password(self, password: str) -> Dict[str, str]:
        return {"pw": password}

    def _verify_password(self, stored: Dict[str, str], password: str) -> bool:
        return secrets.compare_digest(stored.get("pw", ""), password)

    def register(self, username: str, password: str) -> bool:

        username = username.strip()
        if not username or not password:
            return False

        db = self._load_db()
        users = db.setdefault("users", {})
        if username in users:
            return False

        users[username] = self._hash_password(password)
        self._save_db(db)
        return True

    def authenticate(self, username: str, password: str) -> bool:
        db = self._load_db()
        users = db.get("users", {})
        stored = users.get(username)
        if not stored:
            return False
        return self._verify_password(stored, password)


    def login(self, username: str, password: str) -> bool:
        "Logging in..."
        if self.authenticate(username, password):
            self.current_user = username
            print(f"{username} is now logged in.")
            return True
        else:
            print("Invalid username or password.")
            return False

    def logout(self) -> bool:
        "Logging out..."
        if self.current_user:
            print(f"{self.current_user} has been logged out.")
            self.current_user = None
            return True
        else:
            print("No user is currently logged in.")
            return False

if __name__ == "__main__":
    # Minimal demo
    um = UserManager()
    print("Demo: register user 'demo' with password 'potato'")
    ok = um.register("tomato", "potato")
    print("Registered?", ok)
    print("Authenticate with correct password:", um.authenticate("tomato", "potato"))
