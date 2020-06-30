
import stylesheets
from PyQt5 import QtCore, QtWidgets, QtGui
import sys


class User:
    def __init__(self):
        self.picture = QtGui.QPixmap("test.png").scaledToWidth(48)
        self.name = "Test User"

class Message(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QtWidgets.QGridLayout()

        self.user = User()
        self.frame = QtWidgets.QFrame()
        self.fLayout = QtWidgets.QGridLayout()

        self.pfp = QtWidgets.QLabel(self)
        self.pfp.setFixedWidth(48)
        self.pfp.setPixmap(self.user.picture)

        self.uname = QtWidgets.QLabel("KingJellyfish")

        self.text = QtWidgets.QLabel("This is a test m9\nSecond line\nThird line m10 this is cool")
        
        self.layout.addWidget(self.pfp, 0, 0, 2, 1)#, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.frame, 0, 1, 2, 1)
        self.fLayout.addWidget(self.uname, 0, 0, 1, 2)
        self.fLayout.addWidget(self.text, 1, 0, 1, 2)

        self.frame.setLayout(self.fLayout)
        self.setLayout(self.layout)
        self.layout.setRowStretch(1, 1)
        
    def sizeHint(self):
        return self.layout.sizeHint()
        
class MessageView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ssManager = stylesheets.StyleSheetManager()
        self.ssManager.loadSheets()
        
        self.textbox = Message(self)

        height = self.textbox.sizeHint().height()
        width = self.textbox.sizeHint().width()
        xpos, ypos = 5, 5
        self.textbox.setGeometry(QtCore.QRect(xpos, ypos, width, height))

        self.setStyleSheet(self.ssManager.StyleSheet)
        
        self.show()

QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
app = QtWidgets.QApplication(sys.argv)
win = App()
status = app.exec_()
sys.exit(status)
