
import stylesheets
from PyQt5 import QtCore, QtWidgets, QtGui
import sys, random

def genRandomText():
    return "theres this optional work i can do and its been set by the college i wanna go to but should i waste my time doing it? its about science and i dont rlly like science"
    with open("logger.py", "r") as f:
        x = f.read().split("\n")

    num = random.randint(1, 5)
    pos = random.randint(0, len(x) - num - 1)
    lines = x[pos:pos + num]
    return "\n".join(lines)

class User:
    def __init__(self):
        self.picture = QtGui.QPixmap("test.png").scaledToWidth(48)
        self.name = "Test User"

class Message(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QGridLayout()

        self.layout.setSpacing(0);

        self.user = User()
        self.frame = QtWidgets.QFrame()
        self.fLayout = QtWidgets.QGridLayout()

        self.pfp = QtWidgets.QLabel(self)
        self.pfp.setFixedWidth(48)
        self.pfp.setFixedHeight(48)
        self.pfp.setPixmap(self.user.picture)

        self.uname = QtWidgets.QLabel(random.choice(["KingJellyfish", "MasterMysterie"]))

        self.text = QtWidgets.QLabel(genRandomText())
        
        self.layout.addWidget(self.pfp, 0, 0, 1, 1)#, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.frame, 0, 1, 2, 1)
        self.fLayout.addWidget(self.uname, 0, 0, 1, 2)
        self.fLayout.addWidget(self.text, 1, 0, 2, 2)

        self.frame.setLayout(self.fLayout)
        self.setLayout(self.layout)
        self.layout.setRowStretch(2, 1)
        self.layout.setColumnStretch(2, 1)
        
    def sizeHint(self):
        return self.layout.sizeHint()
        
class MessageView(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setLayout(self.layout)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.mainWidget)
        self.messages = []

    def addMessage(self, message):
        self.messages.append(message)
        self.layout.addWidget(message)

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ssManager = stylesheets.StyleSheetManager()
        self.ssManager.loadSheets()
        self.layout = QtWidgets.QHBoxLayout()

        self.messageview = MessageView()
        self.layout.addWidget(self.messageview)
        self.btn = QtWidgets.QPushButton("addmsg")
        self.btn.clicked.connect(self.addNewMessage)
        self.layout.addWidget(self.btn)

        self.setStyleSheet(self.ssManager.StyleSheet)

        self.setLayout(self.layout)        
        self.show()

    def addNewMessage(self):
        self.messageview.addMessage(Message())

QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
app = QtWidgets.QApplication(sys.argv)
win = App()
status = app.exec_()
sys.exit(status)
