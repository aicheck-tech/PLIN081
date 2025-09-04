import bcrypt
from pathlib import Path
from fastapi import Request, HTTPException, status

from tasks.config import PATH


def load_passwords(filepath: Path = PATH.parent / "passwords.txt") -> dict:
    """Load user:hashed_password dict from file."""
    passwords = {}
    try:
        with filepath.open("r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    user, pwd = line.strip().split(":", 1)
                    passwords[user] = pwd
    except FileNotFoundError:
        pass
    return passwords


def authenticate_user(username: str, password: str) -> bool:
    """Validate password against stored bcrypt hash."""
    passwords = load_passwords()
    hashed_password = passwords.get(username)
    if hashed_password and bcrypt.checkpw(password.encode(), hashed_password.encode()):
        return True
    return False


def hash_password(plain_password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()


def get_current_user(request: Request) -> str:
    """Return current username from session, or raise HTTP 401."""
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return username
