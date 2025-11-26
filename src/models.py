"""
models.py
-----------------------
Contains all object-oriented models used in the GYMTrack system:
- User hierarchy (Admin, TrainerManager, FrontDesk)
- Member and MembershipPlan
- ClassSession and Booking
Includes:
- Inheritance
- Encapsulation (password hashing)
- Polymorphism (role-specific menu behavior)
"""

from datetime import datetime


# ================================================================
# Utility: simple password hashing (not real security)
# ================================================================
def simple_hash(value: str) -> str:
    """A simple reversible transformation for demonstration purposes."""
    return "".join(chr(ord(c) + 3) for c in value)  # Caesar shift


# ================================================================
# USER HIERARCHY (OOP: Inheritance + Polymorphism + Encapsulation)
# ================================================================
class User:
    """
    Base User class (Parent class)
    Inherited by: Admin, TrainerManager, FrontDesk
    """

    def __init__(self, username: str, password_hash: str, role: str):
        self.username = username
        self._password_hash = password_hash     # Encapsulated attribute
        self.role = role

    # Encapsulation: password never exposed
    def check_password(self, pw: str) -> bool:
        return self._password_hash == simple_hash(pw)

    def set_password(self, pw: str):
        self._password_hash = simple_hash(pw)

    # Polymorphism: overridden by subclasses
    def display_menu(self) -> dict:
        raise NotImplementedError("Subclasses must override display_menu().")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


# --------------------------- ADMIN ------------------------------
class Admin(User):
    """Admin user — manages system, users, and reports."""

    def __init__(self, username: str, password_hash: str):
        super().__init__(username, password_hash, role="Admin")

    def display_menu(self):
        return {
            "1": "Create User",
            "2": "Edit User",
            "3": "Delete User",
            "4": "View Reports",
            "0": "Logout"
        }


# ---------------------- TRAINER / MANAGER -----------------------
class TrainerManager(User):
    """Trainer/Manager — manages classes and attendance."""

    def __init__(self, username: str, password_hash: str):
        super().__init__(username, password_hash, role="TrainerManager")

    def display_menu(self):
        return {
            "1": "Create Class",
            "2": "Update Class",
            "3": "Delete Class",
            "4": "Mark Attendance",
            "5": "View Attendance",
            "0": "Logout"
        }


# --------------------------- FRONT DESK -------------------------
class FrontDesk(User):
    """Front Desk — handles members, bookings, payments."""

    def __init__(self, username: str, password_hash: str):
        super().__init__(username, password_hash, role="FrontDesk")

    def display_menu(self):
        return {
            "1": "Register Member",
            "2": "Renew Membership",
            "3": "Book Class",
            "4": "Cancel Booking",
            "5": "View Payments",
            "0": "Logout"
        }


# ================================================================
# DOMAIN CLASSES
# ================================================================

# ---------------------------- MEMBER ----------------------------
class Member:
    """
    Represents a gym member.
    """

    def __init__(self, member_id: str, name: str, plan_id: str,
                 status: str = "Active", start_date=None, end_date=None):
        self.member_id = member_id
        self.name = name
        self.plan_id = plan_id
        self.status = status
        self.start_date = start_date
        self.end_date = end_date

    def renew_membership(self, plan, start_date: datetime):
        """Renew membership using a plan's duration."""
        self.start_date = start_date
        self.end_date = start_date + plan.duration
        self.status = "Active"

    def expire_membership(self):
        self.status = "Expired"

    def __repr__(self):
        return f"<Member {self.member_id} - {self.name} ({self.status})>"


# ----------------------- MEMBERSHIP PLAN ------------------------
class MembershipPlan:
    """
    Represents a gym membership plan.
    """

    def __init__(self, plan_id: str, name: str, price: float, duration_days: int):
        self.plan_id = plan_id
        self.name = name
        self.price = price
        self.duration_days = duration_days

    @property
    def duration(self):
        from datetime import timedelta
        return timedelta(days=self.duration_days)

    def __repr__(self):
        return f"<Plan {self.plan_id}: {self.name}>"


# ----------------------- CLASS SESSION --------------------------
class ClassSession:
    """
    Represents a group class / training session.
    """

    def __init__(self, class_id: str, name: str, trainer: str,
                 capacity: int, date_time: datetime):
        self.class_id = class_id
        self.name = name
        self.trainer = trainer
        self.capacity = capacity
        self.date_time = date_time
        self.booked_members = []   # list of member_id strings

    def is_full(self) -> bool:
        return len(self.booked_members) >= self.capacity

    def add_booking(self, member_id: str):
        if not self.is_full():
            self.booked_members.append(member_id)
        else:
            raise ValueError("Class is full")

    def remove_booking(self, member_id: str):
        if member_id in self.booked_members:
            self.booked_members.remove(member_id)

    def __repr__(self):
        return f"<ClassSession {self.class_id}: {self.name}>"


# ----------------------------- BOOKING ---------------------------
class Booking:
    """
    Represents a class booking by a member.
    """

    def __init__(self, booking_id: str, member_id: str,
                 class_id: str, attended: bool = False):
        self.booking_id = booking_id
        self.member_id = member_id
        self.class_id = class_id
        self.attended = attended

    def mark_attended(self):
        self.attended = True

    def __repr__(self):
        return (f"<Booking {self.booking_id} - Member {self.member_id}"
                f" -> Class {self.class_id} | Attended: {self.attended}>")
