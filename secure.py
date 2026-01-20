from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from argon2.low_level import hash_secret_raw, Type
import os, sys

MAGIC = b"SEC"
VERSION = b"\x01"

def kdf(password, salt):
    return hash_secret_raw(
        password, salt,
        time_cost=3, memory_cost=64*1024, parallelism=2,
        hash_len=32, type=Type.ID
    )

# password = sys.stdin.read().rstrip(b"\n")
password = sys.stdin.read().rstrip("\n").encode()
mode = sys.argv[1]

if mode == "encrypt":
    data = open("secrets.md", "rb").read()
    salt, nonce = os.urandom(16), os.urandom(12)
    ct = AESGCM(kdf(password, salt)).encrypt(nonce, data, None)
    open("secrets.enc", "wb").write(MAGIC + VERSION + salt + nonce + ct)

elif mode == "decrypt":
    blob = open("secrets.enc", "rb").read()
    assert blob[:3] == MAGIC
    salt, nonce, ct = blob[4:20], blob[20:32], blob[32:]

    try:
        data = AESGCM(kdf(password, salt)).decrypt(nonce, ct, None)
    except InvalidTag:
        print('wrong password idiot')
    except Exception as e:
        print(e)
    else:
        open("secrets.dec.md", "wb").write(data)
