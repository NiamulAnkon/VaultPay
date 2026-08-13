from __future__ import annotations

from database.db_manager import get_connection
from security.security import hash_password, hash_pin, validate_password, validate_pin, verify_password, verify_pin


class AccountService:
    def __init__(self, connection_factory=get_connection):
        self.connection_factory = connection_factory

    def register_user(self, full_name, username, email, password, confirm_password, pin, confirm_pin):
        full_name = (full_name or "").strip()
        username = (username or "").strip()
        email = (email or "").strip().lower()

        if not full_name:
            raise ValueError("Full name is required.")
        if not username:
            raise ValueError("Username is required.")
        if not email:
            raise ValueError("Email is required.")
        if password != confirm_password:
            raise ValueError("Passwords do not match.")
        if pin != confirm_pin:
            raise ValueError("PINs do not match.")

        password_error = validate_password(password)
        if password_error:
            raise ValueError(password_error)

        pin_error = validate_pin(pin)
        if pin_error:
            raise ValueError(pin_error)

        with self.connection_factory() as conn:
            existing = conn.execute(
                "SELECT id FROM users WHERE username = ? OR email = ?",
                (username, email),
            ).fetchone()
            if existing:
                raise ValueError("Username or email is already registered.")

            user_id = conn.execute(
                """
                INSERT INTO users (full_name, username, email, password_hash, pin_hash)
                VALUES (?, ?, ?, ?, ?)
                """,
                (full_name, username, email, hash_password(password), hash_pin(pin)),
            ).lastrowid

            conn.execute(
                "INSERT INTO wallets (user_id, balance, currency) VALUES (?, 0.0, 'BDT')",
                (user_id,),
            )
            conn.execute(
                "INSERT INTO settings (user_id, currency) VALUES (?, 'BDT')",
                (user_id,),
            )
            conn.commit()
            return user_id

    def login_user(self, username_or_email, password):
        username_or_email = (username_or_email or "").strip()
        if not username_or_email or not password:
            raise ValueError("Username/email and password are required.")

        with self.connection_factory() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE username = ? OR email = ?",
                (username_or_email, username_or_email),
            ).fetchone()
            if not user:
                raise ValueError("Account not found.")
            if not verify_password(password, user["password_hash"]):
                raise ValueError("Incorrect password.")
            return dict(user)

    def get_user_by_id(self, user_id):
        with self.connection_factory() as conn:
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(user) if user else None

    def get_profile(self, user_id):
        with self.connection_factory() as conn:
            user = conn.execute(
                "SELECT u.id, u.full_name, u.username, u.email, u.created_at, w.balance, s.currency FROM users u "
                "LEFT JOIN wallets w ON w.user_id = u.id "
                "LEFT JOIN settings s ON s.user_id = u.id "
                "WHERE u.id = ?",
                (user_id,),
            ).fetchone()
            return dict(user) if user else None

    def change_name(self, user_id, full_name):
        full_name = (full_name or "").strip()
        if not full_name:
            raise ValueError("Full name cannot be empty.")
        with self.connection_factory() as conn:
            conn.execute("UPDATE users SET full_name = ? WHERE id = ?", (full_name, user_id))
            conn.commit()

    def change_password(self, user_id, current_password, new_password, confirm_password):
        if not current_password or not new_password:
            raise ValueError("Current and new passwords are required.")
        if new_password != confirm_password:
            raise ValueError("New passwords do not match.")

        with self.connection_factory() as conn:
            user = conn.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,)).fetchone()
            if not user or not verify_password(current_password, user["password_hash"]):
                raise ValueError("Current password is incorrect.")

            password_error = validate_password(new_password)
            if password_error:
                raise ValueError(password_error)

            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (hash_password(new_password), user_id),
            )
            conn.commit()

    def change_pin(self, user_id, current_pin, new_pin, confirm_pin):
        if not current_pin or not new_pin:
            raise ValueError("Current and new PINs are required.")
        if new_pin != confirm_pin:
            raise ValueError("New PINs do not match.")

        pin_error = validate_pin(new_pin)
        if pin_error:
            raise ValueError(pin_error)

        with self.connection_factory() as conn:
            user = conn.execute("SELECT pin_hash FROM users WHERE id = ?", (user_id,)).fetchone()
            if not user or not verify_pin(current_pin, user["pin_hash"]):
                raise ValueError("Current PIN is incorrect.")

            conn.execute("UPDATE users SET pin_hash = ? WHERE id = ?", (hash_pin(new_pin), user_id))
            conn.commit()

    def verify_pin_for_user(self, user_id, pin):
        with self.connection_factory() as conn:
            row = conn.execute("SELECT pin_hash FROM users WHERE id = ?", (user_id,)).fetchone()
            if not row:
                return False
            return verify_pin(pin, row["pin_hash"])
