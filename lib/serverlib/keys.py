from sys import path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
path.append("../..")
from lib.serverlib import config
from lib.commonlib import errors, encryption
import os, base64


def generateNewUUID():
    rand = base64.urlsafe_b64encode(os.urandom(512))
    print(rand)
    return rand


if not os.path.isdir(config.CONFIG_DIR):
    errors.info("Creating config dir")
    os.makedirs(config.CONFIG_DIR)
    
if not os.path.isfile(config.PUBLIC_KEY) or not os.path.isfile(config.PRIVATE_KEY):
    errors.info("Creating keys")
    private, public = encryption.generate_keys(config.KEY_LEN)

    pem = private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(config.PRIVATE_KEY, "wb") as f:
        f.write(pem)

    pem = public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(config.PUBLIC_KEY, "wb") as f:
        f.write(pem)
                
with open(config.PRIVATE_KEY, "rb") as key_file:
    private = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )
with open(config.PUBLIC_KEY, "rb") as key_file:
    public = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

if not os.path.isfile("/home/sage/temp-uuid.txt"):
    with open("/home/sage/temp-uuid.txt", "wb") as f:
        f.write(generateNewUUID())

with open("/home/sage/temp-uuid.txt", "rb") as f:
    TEMP_UUID = f.read()
