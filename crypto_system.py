import os
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

TOKEN_PREFIX = "SM1."

def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("utf-8").rstrip("=")

def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("utf-8"))

def encrypt_message(message: str) -> str:
    key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, message.encode("utf-8"), None)

    package = {
        "v": 1,
        "alg": "AES-256-GCM",
        "k": _b64encode(key),
        "n": _b64encode(nonce),
        "c": _b64encode(ciphertext)
    }

    serialized = json.dumps(package, separators=(",", ":")).encode("utf-8")
    return TOKEN_PREFIX + _b64encode(serialized)

def decrypt_token(token: str):
    try:
        token = token.strip()

        if not token.startswith(TOKEN_PREFIX):
            return False, "Invalid SecureMessage token."

        encoded_package = token[len(TOKEN_PREFIX):]
        package = json.loads(_b64decode(encoded_package).decode("utf-8"))

        if package.get("v") != 1:
            return False, "Unsupported token version."

        if package.get("alg") != "AES-256-GCM":
            return False, "Unsupported encryption algorithm."

        key = _b64decode(package["k"])
        nonce = _b64decode(package["n"])
        ciphertext = _b64decode(package["c"])

        if len(key) != 32 or len(nonce) != 12:
            return False, "Invalid token data."

        plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
        return True, plaintext.decode("utf-8")

    except Exception:
        return False, "Unable to decrypt. The token may be invalid, incomplete, or modified."
