from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash the password with bcrypt.

    Args:
    -----
    password: str -> The password to be hashed.

    Returns:
    -------
    password: str -> hashed password.
    """
    return pwd_context.hash(password)
