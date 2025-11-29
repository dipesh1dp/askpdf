from passlib.context import CryptContext

# Create a password hashing context using the "bcrypt" algorithm.
# "deprecated='auto'" tells passlib to automatically mark old or weak schemes as deprecated.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 


def hash(password: str): 
    """
    Hash a plain-text password.

    1. Receive the user's raw password.p
    2. Use pwd_context to hash it using bcrypt.
    3. Return the safely hashed password (stored in the database).
    """
    return pwd_context.hash(password)

def verify(plain_password, hashed_password): 
    return pwd_context.verify(plain_password, hashed_password)