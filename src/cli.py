# src/cli.py
from rich.console import Console
from rich.table import Table
from .persistence import Persistence
from .auth import AuthManager
from .models import Admin, TrainerManager, FrontDesk, Member, ClassSession, Booking, MembershipPlan
from .utils import parse_datetime
from datetime import datetime

console = Console()
persistence = Persistence()
auth = AuthManager(persistence)

def pause():
    input("\nPress Enter to continue...")

def print_header():
    console.rule("[bold blue]POP-GYM Management System[/bold blue]")

def main_menu():
    while True:
        print_header()
        print("1) Login")
        print("2) Create user (Admin only)")
        print("3) Register member (FrontDesk)")
        print("4) Create class (Trainer)")
        print("5) Book class (FrontDesk)")
        print("6) View members")
        print("7) View classes")
        print("8) Logout")
        print("9) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            auth.login()
            pause()
        elif choice == "2":
            create_user_flow()
        elif choice == "3":
            register_member_flow()
        elif choice == "4":
            create_class_flow()
        elif choice == "5":
            book_class_flow()
        elif choice == "6":
            view_members()
            pause()
        elif choice == "7":
            view_classes()
            pause()
        elif choice == "8":
            auth.logout()
            pause()
        elif choice == "9":
            console.print("[bold green]Goodbye![/bold green]")
            break
        else:
            print("Invalid choice.")
            pause()

def create_user_flow():
    if not auth.require_role("Admin"):
        pause()
        return
    username = input("New username: ").strip()
    role = input("Role (Admin/TrainerManager/FrontDesk): ").strip()
    password = input("Password: ").strip()
    if role == "Admin":
        user = Admin(username, password)
    elif role == "TrainerManager":
        user = TrainerManager(username, password)
    elif role == "FrontDesk":
        user = FrontDesk(username, password)
    else:
        print("Invalid role.")
        pause()
        return
    persistence.save_user(user)
    print(f"[+] Created user {username} ({role})")
    pause()

def register_member_flow():
    if not auth.require_role("FrontDesk"):
        pause()
        return
    members = persistence.get_all("members")
    member_id = input("Member ID: ").strip()
    name = input("Full name: ").strip()
    plans = persistence.get_all("plans")
    console.print("Available Plans:")
    for pid, plan in plans.items():
        console.print(f"- {pid}: {plan.name} (${plan.price}) {plan.duration_days}d")
    plan_id = input("Plan ID: ").strip()
    plan = plans.get(plan_id)
    if not plan:
        print("Plan not found.")
        pause()
        return
    m = Member(member_id, name)
    m.renew(plan, datetime.now())
    members[member_id] = m
    persistence.save_all("members", members)
    print("[+] Member registered.")
    pause()

def create_class_flow():
    if not auth.require_role("TrainerManager"):
        pause()
        return
    classes = persistence.get_all("classes")
    class_id = input("Class ID: ").strip()
    name = input("Class name: ").strip()
    trainer = auth.current_user.username
    capacity = int(input("Capacity: ").strip())
    dt_str = input("DateTime (YYYY-MM-DD HH:MM): ").strip()
    try:
        dt = parse_datetime(dt_str)
    except Exception:
        print("Invalid datetime format.")
        pause()
        return
    c = ClassSession(class_id, name, trainer, capacity, dt)
    classes[class_id] = c
    persistence.save_all("classes", classes)
    print("[+] Class created.")
    pause()

def book_class_flow():
    if not auth.require_role("FrontDesk"):
        pause()
        return
    members = persistence.get_all("members")
    classes = persistence.get_all("classes")
    bookings = persistence.get_all("bookings")
    member_id = input("Member ID: ").strip()
    if member_id not in members:
        print("Member not found.")
        pause()
        return
    class_id = input("Class ID: ").strip()
    c = classes.get(class_id)
    if not c:
        print("Class not found.")
        pause()
        return
    try:
        c.add_booking(member_id)
    except Exception as e:
        print(f"Error: {e}")
        pause()
        return
    classes[class_id] = c
    bid = f"B{len(bookings)+1}"
    bookings[bid] = Booking(bid, member_id, class_id, attended=False)
    persistence.save_all("classes", classes)
    persistence.save_all("bookings", bookings)
    print("[+] Booking created.")
    pause()

def view_members():
    members = persistence.get_all("members")
    t = Table("Member ID", "Name", "Plan", "Status")
    for m in members.values():
        t.add_row(m.member_id, m.name, str(m.plan_id), m.status)
    console.print(t)

def view_classes():
    classes = persistence.get_all("classes")
    t = Table("Class ID", "Name", "Trainer", "DateTime", "Capacity", "Booked")
    for c in classes.values():
        t.add_row(c.class_id, c.name, c.trainer, str(c.date_time), str(c.capacity), str(len(c.booked_members)))
    console.print(t)

if __name__ == "__main__":
    main_menu()
