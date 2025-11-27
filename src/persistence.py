# src/persistence.py
import os
import pickle
from pathlib import Path
from typing import Dict, Any

from .models import Admin, MembershipPlan

DATA_DIR = Path("data")
FILES = {
    "users": DATA_DIR / "users.pkl",
    "members": DATA_DIR / "members.pkl",
    "plans": DATA_DIR / "plans.pkl",
    "classes": DATA_DIR / "classes.pkl",
    "bookings": DATA_DIR / "bookings.pkl",
}

STORAGE_VERSION = 1  # bump if structure changes


class Persistence:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        self.initialize_defaults()

    # -------------------------------------------------------------------
    # SAFE LOADING: NEVER CRASH, ALWAYS RETURN VALID DATA
    # -------------------------------------------------------------------
    def safe_load_raw(self, path: Path):
        """Load raw pickle. If it fails for ANY reason, return None."""
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception:
            return None

    # -------------------------------------------------------------------
    # FILE INITIALIZATION
    # -------------------------------------------------------------------
    def initialize_defaults(self):
        """Create a correct versioned file if missing OR corrupted."""

        # USERS
        raw = self.safe_load_raw(FILES["users"])
        if not isinstance(raw, dict) or raw.get("_version") != STORAGE_VERSION:
            # recreate valid users structure
            admin = Admin("admin", "admin123")
            fixed = {
                "_version": STORAGE_VERSION,
                "payload": {"admin": admin}
            }
            self._save_raw(FILES["users"], fixed)

        # MEMBERS
        raw = self.safe_load_raw(FILES["members"])
        if not isinstance(raw, dict) or raw.get("_version") != STORAGE_VERSION:
            self._save_raw(FILES["members"], {"_version": STORAGE_VERSION, "payload": {}})

        # PLANS
        raw = self.safe_load_raw(FILES["plans"])
        if not isinstance(raw, dict) or raw.get("_version") != STORAGE_VERSION:
            p1 = MembershipPlan("P1", "Basic Monthly", 50.0, 30)
            self._save_raw(FILES["plans"], {"_version": STORAGE_VERSION, "payload": {"P1": p1}})

        # CLASSES
        raw = self.safe_load_raw(FILES["classes"])
        if not isinstance(raw, dict) or raw.get("_version") != STORAGE_VERSION:
            self._save_raw(FILES["classes"], {"_version": STORAGE_VERSION, "payload": {}})

        # BOOKINGS
        raw = self.safe_load_raw(FILES["bookings"])
        if not isinstance(raw, dict) or raw.get("_version") != STORAGE_VERSION:
            self._save_raw(FILES["bookings"], {"_version": STORAGE_VERSION, "payload": {}})

    # -------------------------------------------------------------------
    # RAW SAVE
    # -------------------------------------------------------------------
    def _save_raw(self, path: Path, obj: Any):
        with open(path, "wb") as f:
            pickle.dump(obj, f)

    # -------------------------------------------------------------------
    # PUBLIC API — ALWAYS RETURNS ONLY PAYLOAD
    # -------------------------------------------------------------------
    def load(self, key: str) -> Dict[str, Any]:
        raw = self.safe_load_raw(FILES[key])

        # corrupted or missing
        if not isinstance(raw, dict) or "_version" not in raw or "payload" not in raw:
            print(f"[persistence] Auto-fixing {key}.pkl")
            self.initialize_defaults()
            raw = self.safe_load_raw(FILES[key])

        return raw["payload"]

    def save(self, key: str, payload: Dict[str, Any]):
        obj = {"_version": STORAGE_VERSION, "payload": payload}
        self._save_raw(FILES[key], obj)

    # ---------------- USER HELPERS ----------------
    def get_user(self, username: str):
        return self.load("users").get(username)

    def save_user(self, user_obj):
        users = self.load("users")
        users[user_obj.username] = user_obj
        self.save("users", users)

    # --------------- GENERIC HELPERS --------------
    def get_all(self, key: str):
        return self.load(key)

    def save_all(self, key: str, data: Dict[str, Any]):
        self.save(key, data)
