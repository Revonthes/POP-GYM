"""
cli.py
--------------------------------------------------------
Main Click-based CLI interface.

Responsibilities:
- Start application loop
- Login/logout
- Display role-specific menus
- Run the appropriate actions (CRUD operations)
"""

import click
from rich.console import Console
from rich.table import Table

from auth import login, is_authorized
from persistence import (
    load_data, save_data, FILES
)
from models import (
    Admin, TrainerManager, FrontDesk,
    Member, MembershipPlan, ClassSession, Booking
)

console = Console()


# -----------------------------------------------------
# LOGIN COMMAND
# -----------------------------------------------------
@click.command()
def start():
    """Launch the GYMTrack CLI system."""

    console.rule("[bold green]GYMTrack Management System[/bold green]")

    # --------------- LOGIN --------------------
    while True:
        username = click.prompt("Enter username")
        password = click.prompt("Enter password", hide_input=True)

        user = login(username, password)

        if user:
            console.print(f"[bold green]Login successful![/] Welcome {user.username}")
            break
        else:
            console.print("[bold red]Invalid credentials. Try again.[/]")

    # ------------- APPLICATION LOOP -----------
    while True:
        console.rule(f"[blue]Dashboard – {user.role}[/blue]")

        menu = user.display_menu()

        # Print menu
        table = Table(title=f"{user.role} Menu")
        table.add_column("Option")
        table.add_column("Description")

        for key, label in menu.items():
            table.add_row(key, label)
        console.print(table)

        choice = click.prompt("Choose an option")

        if choice == "0":
            console.print("[yellow]Logging out...[/]")
            break

        handle_menu_choice(choice, user)


# -----------------------------------------------------
# MENU HANDLER (Simple Demonstration Version)
# -----------------------------------------------------
def handle_menu_choice(choice: str, user):

    # ---------------- ADMIN ACTIONS ----------------
    if user.role == "Admin":
        if choice == "1":
            create_user()
        elif choice == "2":
            edit_user()
        elif choice == "3":
            delete_user()

    # ------------- TRAINER ACTIONS ---------------
    if user.role == "TrainerManager":
        if choice == "1":
            create_class()
        # ... add the other Trainer functions

    # ---------------- FRONT DESK ACTIONS ---------
    if user.role == "FrontDesk":
        if choice == "1":
            register_member()
        # ... add other FrontDesk functions


# -----------------------------------------------------
# ADMIN FUNCTIONS
# -----------------------------------------------------
def create_user():
    """Admin creates a new user."""

    users = load_data(FILES["users"])

    username = click.prompt("New username")

    if username in users:
        console.print("[red]User already exists![/]")
        return

    password = click.prompt("Password", hide_input=True)

    role = click.prompt("Role", type=click.Choice(["Admin", "TrainerManager", "FrontDesk"]))

    # Create the correct subclass object
    if role == "Admin":
        obj = Admin(username, password)
    elif role == "TrainerManager":
        obj = TrainerManager(username, password)
    else:
        obj = FrontDesk(username, password)

    users[username] = obj
    save_data(users, FILES["users"])

    console.print("[green]User created successfully![/]")


def edit_user():
    console.print("[yellow]Edit User — Not implemented fully yet.[/]")


def delete_user():
    console.print("[yellow]Delete User — Not implemented fully yet.[/]")


# -----------------------------------------------------
# FRONT DESK
# -----------------------------------------------------
def register_member():
    """Register a new gym member."""

    members = load_data(FILES["members"])

    m_id = click.prompt("Member ID")
    name = click.prompt("Member Name")
    plan_id = click.prompt("Plan ID")

    member = Member(m_id, name, plan_id)

    members[m_id] = member
    save_data(members, FILES["members"])

    console.print("[green]Member registered successfully![/]")


# -----------------------------------------------------
# TRAINER
# -----------------------------------------------------
def create_class():
    """Create a new class session (trainer only)."""

    classes = load_data(FILES["classes"])

    class_id = click.prompt("Class ID")
    name = click.prompt("Class Name")
    trainer = click.prompt("Trainer Name")
    capacity = click.prompt("Capacity", type=int)
    date_time = click.prompt("DateTime (YYYY-MM-DD HH:MM)")

    class_obj = ClassSession(class_id, name, trainer, capacity, date_time)

    classes[class_id] = class_obj
    save_data(classes, FILES["classes"])

    console.print("[green]Class created successfully![/]")
