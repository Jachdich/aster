import threading, socket
from sys import path
path.append("../..")
from lib.serverlib import net, keys
from lib.commonlib import encryption, errors
from lib.serverlib.config import PORT

def clean():
    try:
        conn.close()
    except:
        pass
    s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", PORT))
s.listen(20)

class ServerMessage:
    def __init__(self, messageID, content):
        self.content = content
        self.messageID = messageID
        self.readBy = []
        
    def setRead(self, fingerprint):
        self.readBy.append(fingerprint)

class ServerHandler(threading.Thread):
    def __init__(self, conn):
        super().__init__(target=self.run)
        self.conn = conn
        self.start()

    def run(self):
        request = self.conn.recvEncrtypted()
        if request["request"] == "mark_read":
            errors.debug("Got mark_read request for ID {} from device fingerprint {}".format(request["value"], request["fingerprint"]))
            msg = self.getMessageByID(request["value"])
            msg.setRead(request["fingerprint"])
            self.conn.sendEncrypted({"result": 0})

        if request["request"] == "get_unread":
            uuid = request["uuid"]
            public = request["public"]
            errors.debug("Got get_unread request from UUID {}".format(uuid))
            messages = self.getMessagesByDestination(uuid)

    def getMessageByID(self, ID):
        return None

    def getMessagesByDestination(self, uuid):
        return None
            
            

threads = []

try:
    while True:
        conn, addr = s.accept()
        errors.info("Connected by {}".format(addr))
        threads.append(ServerHandler(EncryptedSocket(public, private, conn=conn)))

except Exception as e:
    errors.fatal(str(e), False)
    clean()

except KeyboardInterrupt:
    errors.fatal("Keyboard interrupt!", False)
    clean()
finally:
    clean()
