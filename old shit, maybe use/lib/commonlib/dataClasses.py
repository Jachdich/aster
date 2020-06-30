class Contact:
    def __init__(self, name, uuid, public):
        self.name = name
        self.uuid = uuid
        self.public = public

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Contact(name={}, uuid={}, pubkey={})".format(self.name, self.uuid, self.public)

class Message:
    def __init__(self, content, messageID):
        self.messageID = messageID
        self.content = content

class User:
    def __init__(self, publickey, uuid):
        self.key = publickey
        self.uuid = uuid
        
