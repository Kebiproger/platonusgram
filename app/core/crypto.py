import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from app.core.config import FERNET_KEY

fernet = Fernet(FERNET_KEY)

def fernet_encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode("utf-8")).decode("utf-8")

def fernet_decrypt_password(password_enc: str) -> str:
    if not password_enc:
        return ""
    # Если данные были случайно сохранены как строка вида "b'token'"
    if isinstance(password_enc, str) and password_enc.startswith("b'") and password_enc.endswith("'"):
        password_enc = password_enc[2:-1]
    return fernet.decrypt(password_enc.encode("utf-8")).decode("utf-8")



# 1. Загружаем твой секретный приватный ключ из файла
with open("private.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )

# Функция для расшифровки
def js_decrypt_password(encrypted_base64_string: str) -> str:
    # Мы НЕ ловим ошибку здесь, чтобы она "всплыла" в хэндлере 
    # и мы не сохранили текст ошибки вместо пароля в базу данных.
    encrypted_bytes = base64.b64decode(encrypted_base64_string)

    # Расшифровываем приватным ключом
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.PKCS1v15() # Стандарт отступов, который использует JSEncrypt
    )
    return decrypted_bytes.decode('utf-8')
