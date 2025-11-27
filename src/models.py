# src/models.py
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import hashlib
from typing import List

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

@dataclass
class User:
    username: str
    _password_hash: str = field(repr=False)
    role: str = "User"

    def set_password(self, pw: str):
        self._password_hash = hash_password(pw)

    def check_password(self, pw: str) -> bool:
        return self._password_hash == hash_password(pw)

    def display_menu(self) -> dict:
        raise NotImplementedError

@dataclass
class Admin(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, hash_password(password), role="Admin")

    def display_menu(self):
        return {"1": "Create user", "2": "View reports", "0": "Logout"}

@dataclass
class TrainerManager(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, hash_password(password), role="TrainerManager")

    def display_menu(self):
        return {"1": "Create class", "2": "Mark attendance", "0": "Logout"}

@dataclass
class FrontDesk(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, hash_password(password), role="FrontDesk")

    def display_menu(self):
        return {"1": "Register member", "2": "Book class", "0": "Logout"}

@dataclass
class Member:
    member_id: str
    name: str
    plan_id: str | None = None
    status: str = "Active"
    start_date: datetime | None = None
    end_date: datetime | None = None

    def renew(self, plan: "MembershipPlan", start: datetime):
        self.plan_id = plan.plan_id
        self.start_date = start
        self.end_date = start + plan.duration
        self.status = "Active"

@dataclass
class MembershipPlan:
    plan_id: str
    name: str
    price: float
    duration_days: int

    @property
    def duration(self) -> timedelta:
        return timedelta(days=self.duration_days)

@dataclass
class ClassSession:
    class_id: str
    name: str
    trainer: str
    capacity: int
    date_time: datetime
    booked_members: List[str] = field(default_factory=list)

    def is_full(self) -> bool:
        return len(self.booked_members) >= self.capacity

    def add_booking(self, member_id: str):
        if self.is_full():
            raise ValueError("Class is full")
        if member_id in self.booked_members:
            raise ValueError("Member already booked")
        self.booked_members.append(member_id)

    def remove_booking(self, member_id: str):
        if member_id in self.booked_members:
            self.booked_members.remove(member_id)

@dataclass
class Booking:
    booking_id: str
    member_id: str
    class_id: str
    attended: bool = False
