import threading, time
from sys import path
path.append("../..")
from PyQt5 import QtCore
from lib.clientlib import gui
from lib.commonlib.dataClasses import Message
from lib.commonlib import errors, net

class ClientListener(QtCore.QThread):
    received = QtCore.pyqtSignal(Message)

    def run(self):
        self.getExistingMessages()
        self.listenForNewMessages()

    def getExistingMessages(self):
        pass

    def listenForNewMessages(self):
        while True:
            time.sleep(2)

    def setContact(self, contact):
        self.contact = contact

    def stop(self):
        self.running = False
        
    def listen(self):
        self.running = True
        self.start()

class ClientServerInterface:
    def __init__(self, public, private):
        self.RETRIES = 5
        self.fingerprint = "0123456789abcdef"
        self.s = net.EncryptedSocket(public, private, addr=(config.HOST, config.PORT))

    def markAsRead(self, message):
        s = self.getSocket()
        for i in range(self.RETRIES):
            errors.debug("Marking message (ID: {}) as read".format(message.messageID))
            s.sendEncrypted({"request": "mark_read", "value": message.messageID, "fingerprint": self.fingerprint})
            number_check = s.recvEncrypted()
            s.sendEncrypted(number_check)
            result = s.recvEncrypted()
            if result["status"] == 0:
                errors.info("Got success back")
                break
            else:
                errors.warn("Server returned non-zero status {}".format(result["status"]))
                errors.warn("Retrying ({}/{})".format(i, self.RETRIES))

    def getSocket(self):
        return self.s

    def sendMessage(self, recver, message):
        s = self.getSocket()
        s.sendEncrypted({"request": "send_message", "fingerprint": self.fingerprint,
                         "message_content": encription.encrypt(message.content, recver.public),
                         "message_id": message.messageID, "recipient": recver.uuid})
        
