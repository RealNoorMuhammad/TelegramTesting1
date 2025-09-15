from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from config import Config

def get_encryption_key():
    """Get or create encryption key."""
    if not Config.ENCRYPTION_KEY:
        raise ValueError("ENCRYPTION_KEY must be set in environment variables")
    
    # Convert the key to bytes and create a Fernet key
    key = Config.ENCRYPTION_KEY.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'polymarket_bot_salt',  # In production, use a random salt per user
        iterations=100000,
    )
    derived_key = base64.urlsafe_b64encode(kdf.derive(key))
    return derived_key

def encrypt_private_key(private_key: str) -> str:
    """Encrypt a private key."""
    f = Fernet(get_encryption_key())
    encrypted_key = f.encrypt(private_key.encode())
    return base64.urlsafe_b64encode(encrypted_key).decode()

def decrypt_private_key(encrypted_key: str) -> str:
    """Decrypt a private key."""
    f = Fernet(get_encryption_key())
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_key.encode())
    decrypted_key = f.decrypt(encrypted_bytes)
    return decrypted_key.decode()
