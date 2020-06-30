from sys import path
path.append("..")
from lib import net, keys, user, encryption

s = net.ClientSocket()

def onUserMessage(message, targetUUID):
    s.setUser(users.server)
    s.sendEncrypted("put")
    s.setUser(users.getUserByUUID(targetUUID))
    s.sendEncrypted(

#encrypted = encryption.encrypt("testasd", keys.public)
#print(encrypted)
#original  = encryption.decrypt(encrypted, keys.private)
#print(original)
