import hashlib
import json
import os
from base64 import urlsafe_b64encode

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
    )
    return kdf.derive(password.encode())


def encrypt_file(path, password):
    data = open(path, "rb").read()
    salt = os.urandom(16)
    key = derive_key(password, salt)
    nonce = os.urandom(12)
    aes = AESGCM(key)
    ciphertext = aes.encrypt(nonce, data, None)

    sha = hashlib.sha256(data).hexdigest()
    meta = {"salt": salt.hex(), "nonce": nonce.hex(), "hash": sha, "attempts": 0}

    return ciphertext, meta


def decrypt_file(enc_path, password, meta):
    data = open(enc_path, "rb").read()
    salt = bytes.fromhex(meta["salt"])
    nonce = bytes.fromhex(meta["nonce"])
    key = derive_key(password, salt)
    aes = AESGCM(key)
    plain = aes.decrypt(nonce, data, None)
    if hashlib.sha256(plain).hexdigest() != meta["hash"]:
        raise Exception("Integrity failure")
    return plain
