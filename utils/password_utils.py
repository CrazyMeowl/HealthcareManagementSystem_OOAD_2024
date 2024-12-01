import bcrypt
import base64


# Hash a password with a salt
def hash_password(password: str) -> str:
    # Generate a random salt and hash the password with it
    salt = bcrypt.gensalt()  # Generates a random salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Encode the hashed password to a base64 string to store it as text
    return base64.b64encode(hashed_password).decode('utf-8')

# Verify a password
def verify_password(stored_hash: str, password: str) -> bool:
    # Decode the base64 encoded hash back to bytes
    stored_hash_bytes = base64.b64decode(stored_hash.encode('utf-8'))
    
    # Verify the password using bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash_bytes)
