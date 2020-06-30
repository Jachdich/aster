#THING:
#client: "hi send me unread messages"
#server: sure, here u go
#client: now set those messages to read
#server: sure
#client: now wait till u get more messages and send them here, but expires every 10 mins or so
#server:
#server: message 4 u
#client: cool now do it again
#client: and set it as read
#server:
#server:
#server: message 4 u
#client: cool now do it again
#client: and set it as read
#server: sure
#and again and again


Style of messages being displayed?
Own messages: same or opposite side?


from PyQt5 import QtWidgets, QtCore, QtGui
from sys import path
path.append("../..")
from lib.clientlib import gui, listener
from lib.commonlib.dataClasses import Contact, Message

class MessageWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initGUI()
        self.inpText = ""
        self.user = Contact("KingJellyfishII", "1fcf259d0d9", "afhohefh0aef0==")
        self.messages = []
        self.doc = self.mainText.document()
        self.listener = listener.ClientListener()
        self.listener.received.connect(self.messageRecvd)

        self.server = listener.ClientServerInterface("no idea", "wtf")

    def messageRecvd(self, message):
        self.addMessage(message)
        self.server.markAsRead(message)
        
    def constructHTML(self, messages):
        return " <br/>\n".join(messages)

    def addMessage(self, message):
        self.messages.append(message.content.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;").replace("%", "&#37;"))
        self.doc.setHtml(self.constructHTML(self.messages))

    def onTextChanged(self, text):
        self.inpText = text

    def returnPressed(self):
        self.addMessage("<" + self.user.name + "> " + self.inpText)
        self.inp.setText("")

    def initGUI(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        self.topBar = QtWidgets.QHBoxLayout(self)
        self.backButton = QtWidgets.QPushButton(self)
        self.backButton.setText("Back")
        self.backButton.clicked.connect(self.back)
        self.topBar.addWidget(self.backButton)

        self.layout.addLayout(self.topBar)
        
        self.mainText = QtWidgets.QPlainTextEdit(self)
        self.inp = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.mainText)
        self.layout.addWidget(self.inp)
        self.setLayout(self.layout)

        self.inp.returnPressed.connect(self.returnPressed)
        self.inp.textChanged.connect(self.onTextChanged)

    def back(self):
        self.setContact(None)
        self.parent.openContactWindow()

    def cleanUp(self):
        self.doc.setHtml("")

    def setContact(self, contact):
        if contact == None:
            self.listener.stop()
            self.cleanUp()
        else:
            self.listener.setContact(contact)
            self.listener.listen()


class ContactWindow(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QtWidgets.QGridLayout()
        self.list = QtWidgets.QListView()

        model = QtGui.QStandardItemModel(self.list)
        self.contacts = {"James": Contact("James", "1209839801324", "aifsijp3e-93"), "Peter": Contact("Peter", "asf", "awd")}
         
        for key in self.contacts:
            item = QtGui.QStandardItem(key)
            model.appendRow(item)

        self.list.setModel(model)
        
        self.layout.addWidget(self.list)
        self.setLayout(self.layout)
        self.list.clicked.connect(self.clicked)

    def clicked(self, item):
        self.parent.openMessageWindow(self.contacts[item.data()])
        
class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initGUI()

    def initGUI(self):
        self.main = QtWidgets.QWidget(self)
        
        self.layout = QtWidgets.QVBoxLayout(self)

        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.messageWindow = MessageWindow(self)
        self.contactWindow = ContactWindow(self)

        self.stackedWidget.addWidget(self.contactWindow)
        self.stackedWidget.addWidget(self.messageWindow)

        self.layout.addWidget(self.stackedWidget)
        
        self.main.setLayout(self.layout)
        self.setCentralWidget(self.main)
        self.show()

    def openMessageWindow(self, contact):
        self.stackedWidget.setCurrentIndex(1)
        self.messageWindow.setContact(contact)

    def openContactWindow(self):
        self.stackedWidget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mw = MainWindow()
    app.exec_()
