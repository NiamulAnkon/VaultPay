import hashlib
import secrets


def hash_secret(secret: str, salt: str | None = None) -> str:
    if secret is None:
        raise ValueError("Secret cannot be empty.")
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", secret.encode("utf-8"), salt.encode("utf-8"), 200_000)
    return f"{salt}${digest.hex()}"


def verify_secret(secret: str, hashed_value: str) -> bool:
    if not secret or not hashed_value:
        return False
    try:
        salt, digest_hex = hashed_value.split("$", 1)
    except ValueError:
        return False
    expected = hash_secret(secret, salt)
    return secrets.compare_digest(expected, hashed_value)


def hash_password(password: str) -> str:
    return hash_secret(password)


def verify_password(password: str, password_hash: str) -> bool:
    return verify_secret(password, password_hash)


def hash_pin(pin: str) -> str:
    return hash_secret(pin)


def verify_pin(pin: str, pin_hash: str) -> bool:
    return verify_secret(pin, pin_hash)


def validate_password(password: str) -> str | None:
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    return None


def validate_pin(pin: str) -> str | None:
    if not pin.isdigit():
        return "PIN must contain only digits."
    if len(pin) not in (4, 6):
        return "PIN must be 4 or 6 digits long."
    return None
