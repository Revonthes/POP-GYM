"""
auth.py
-------------------------------------------------
Handles user authentication, login verification,
and returns the correct User object after login.

Uses:
- persistence.py for loading users.pkl
- models.User.check_password() for authentication
"""

from persistence import FILES, load_data
from models import User


# -----------------------------------------------------
# LOGIN FUNCTION
# -----------------------------------------------------
def login(username: str, password: str) -> User | None:
    """
    Attempts to authenticate the user.
    Returns a User object on success, or None on failure.
    """

    users = load_data(FILES["users"])

    if username not in users:
        return None

    user_obj = users[username]

    if user_obj.check_password(password):
        return user_obj

    return None


# -----------------------------------------------------
# ROLE CHECKING
# -----------------------------------------------------
def is_authorized(user: User, allowed_roles: list[str]) -> bool:
    """Checks if the user has permission for a certain command."""
    return user.role in allowed_roles
