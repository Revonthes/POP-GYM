# src/auth.py
import sys
from .persistence import Persistence
from .models import User

IS_WINDOWS = sys.platform.startswith("win")
if IS_WINDOWS:
    import msvcrt
else:
    import tty, termios

def masked_input(prompt="Password: "):
    """Read password from terminal while printing '*' for each character."""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    pwd = ""
    if IS_WINDOWS:
        while True:
            ch = msvcrt.getch()
            if ch in (b'\r', b'\n'):
                sys.stdout.write("\n")
                break
            if ch == b'\x03':
                raise KeyboardInterrupt
            if ch == b'\x08':  # backspace
                if len(pwd) > 0:
                    pwd = pwd[:-1]
                    sys.stdout.write("\b \b")
                continue
            try:
                ch_dec = ch.decode()
            except:
                continue
            pwd += ch_dec
            sys.stdout.write("*")
            sys.stdout.flush()
    else:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ("\r", "\n"):
                    sys.stdout.write("\n")
                    break
                if ch == "\x03":
                    raise KeyboardInterrupt
                if ch in ("\x7f", "\b"):
                    if len(pwd) > 0:
                        pwd = pwd[:-1]
                        sys.stdout.write("\b \b")
                    continue
                pwd += ch
                sys.stdout.write("*")
                sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return pwd

class AuthManager:
    def __init__(self, persistence: Persistence):
        self.persistence = persistence
        self.current_user: User | None = None

    def login(self) -> User | None:
        print("=== LOGIN ===")
        username = input("Username: ").strip()
        password = masked_input("Password: ")
        user = self.persistence.get_user(username)
        if user is None:
            print("[!] User not found.")
            return None
        if not user.check_password(password):
            print("[!] Incorrect password.")
            return None
        self.current_user = user
        print(f"[+] Logged in as {user.username} ({user.role})")
        return user

    def logout(self):
        if self.current_user:
            print(f"[+] Logged out: {self.current_user.username}")
        self.current_user = None

    def require_role(self, role: str) -> bool:
        if self.current_user is None:
            print("[!] Not logged in.")
            return False
        if self.current_user.role != role:
            print(f"[!] Access denied. Requires role: {role}")
            return False
        return True
