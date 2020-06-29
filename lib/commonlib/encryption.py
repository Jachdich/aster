from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

def generate_keys(modulus_length):
   private_key = rsa.generate_private_key(
       public_exponent=65537,
       key_size=modulus_length,
       backend=default_backend()
   )
   public_key = private_key.public_key()
   return private_key, public_key

def encrypt(message, publickey):
   encrypted = publickey.encrypt(
      message.encode("utf-8"),
      padding.OAEP(
         mgf=padding.MGF1(algorithm=hashes.SHA256()),
         algorithm=hashes.SHA256(),
         label=None
      )
   )
   return base64.urlsafe_b64encode(encrypted)

def decrypt(msg, privatekey):
   original = privatekey.decrypt(
      base64.urlsafe_b64decode(msg),
      padding.OAEP(
         mgf=padding.MGF1(algorithm=hashes.SHA256()),
         algorithm=hashes.SHA256(),
         label=None
      )
   )
   return original
