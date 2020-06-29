from sys import path
path.append("../..")
from lib.serverlib import keys
from lib.commonlib.dataClasses import User

server = user.User(keys.public, None)

def getUserByUUID(uuid):
    return User(keys.public, keys.TEMP_UUID)
