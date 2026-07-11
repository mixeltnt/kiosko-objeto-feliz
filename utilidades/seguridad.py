import bcrypt

def hash_password(password_plano: str) -> bytes:
    return bcrypt.hashpw(password_plano.encode("utf-8"), bcrypt.gensalt())

def verificar_password(password_plano: str, password_hash: bytes) -> bool:
    return bcrypt.checkpw(password_plano.encode("utf-8"), password_hash)
