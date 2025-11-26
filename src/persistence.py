"""
persistence.py
----------------------------------------
Handles all data loading/saving using Pickle.

Files stored in /data:
- users.pkl
- members.pkl
- plans.pkl
- classes.pkl
- bookings.pkl

This file is the SINGLE SOURCE of truth for:
- Reading database
- Writing database
- Initializing seed data
"""

import os
import pickle
from pathlib import Path
from models import Admin, simple_hash, MembershipPlan


# -----------------------------------------------------
# Paths
# -----------------------------------------------------
DATA_DIR = Path("data")

FILES = {
    "users": DATA_DIR / "users.pkl",
    "members": DATA_DIR / "members.pkl",
    "plans": DATA_DIR / "plans.pkl",
    "classes": DATA_DIR / "classes.pkl",
    "bookings": DATA_DIR / "bookings.pkl",
}


# -----------------------------------------------------
# Generic LOAD function
# -----------------------------------------------------
def load_data(filename: Path):
    """Load Python objects from a pickle file."""
    if not filename.exists():
        return {}  # return empty dict if file not created yet

    with open(filename, "rb") as f:
        return pickle.load(f)


# -----------------------------------------------------
# Generic SAVE function
# -----------------------------------------------------
def save_data(data, filename: Path):
    """Save Python objects to a pickle file."""
    with open(filename, "wb") as f:
        pickle.dump(data, f)


# -----------------------------------------------------
# Initialize system with default admin + default plans
# -----------------------------------------------------
def initialize_data():
    """Creates empty files OR seeds initial admin/plans if files not present."""
    DATA_DIR.mkdir(exist_ok=True)

    # --- USERS ---
    if not FILES["users"].exists():
        default_admin = Admin("admin", simple_hash("admin123"))
        save_data({"admin": default_admin}, FILES["users"])

    # --- MEMBERS ---
    if not FILES["members"].exists():
        save_data({}, FILES["members"])

    # --- PLANS ---
    if not FILES["plans"].exists():
        p1 = MembershipPlan("P1", "Basic Monthly", 50.0, 30)
        p2 = MembershipPlan("P2", "Quarterly", 120.0, 90)
        save_data({"P1": p1, "P2": p2}, FILES["plans"])

    # --- CLASSES ---
    if not FILES["classes"].exists():
        save_data({}, FILES["classes"])

    # --- BOOKINGS ---
    if not FILES["bookings"].exists():
        save_data({}, FILES["bookings"])
