from passlib.context import CryptContext

# -------------------------------------------------------
# 🔐 Password hashing context using bcrypt
# -------------------------------------------------------
# Passlib handles secure password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------
# 🔐 Hash a plain text password
# -----------------------------
def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.
    Returns the hashed string for secure storage.
    """
    return pwd_context.hash(password)

# -----------------------------
# ✅ Verify password correctness
# -----------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a plain-text password matches the hashed version.
    Returns True if valid, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
