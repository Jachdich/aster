from PyQt5 import QtWidgets

class MessageArea(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.messages = []
        self.initGUI()
        self.doc = self.mainText.document()

    def initGUI(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.mainText = QtWidgets.QPlainTextEdit(self)
        self.inp = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.mainText)
        self.layout.addWidget(self.inp)
        self.setLayout(self.layout)

    def constructHTML(self, messages):
        return " <br/>\n".join(messages)

    def addMessage(self, message):
        self.messages.append(message)
        self.doc.setHtml(self.constructHTML(self.messages))
