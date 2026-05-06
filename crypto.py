from cryptography.fernet import Fernet
from config import FERNET_KEY

fernet = Fernet(FERNET_KEY)

def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode("utf-8")).decode("utf-8")

def decrypt_password(password_enc: str) -> str:
    return fernet.decrypt(password_enc.encode("utf-8")).decode("utf-8")