import socket, json
from sys import path
path.append("../..")
from lib.commonlib import encryption

class EncryptedSocket:
    def __init__(self, public, private, addr=None, conn=None):
        if addr:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((addr, port))
        elif conn:
            self.s = conn
        else:
            errors.fatal("Neither a socket object or an address was supplied to EncryptedSocket")
        self.public = public
        self.private = private

    def sendEncrypted(self, data):
        plain = json.dumps(data)
        encrypted = encryption.encrypt(plain, self.user.key)
        length = str(len(encrypted))
        print(encrypted)
        self.s.send((length + " " * (1024 - len(length))).encode("utf-8"))
        self.s.send(encrypted)

    def recvEncrypted(self):
        length = int(self.s.recv(1024).strip(" "))
        out = ""
        while len(out) < length:
            out += self.s.recv(1024)

        plain = encryption.decrypt(out, keys.private)
        return json.loads(plain)
