from PyQt5 import QtCore, QtWidgets, QtWidgets, QtNetwork

class Client(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.mainLayout = QtWidgets.QGridLayout()
        self.messages = QtWidgets.QTextEdit()
        self.messages.setReadOnly(True)
        self.messageLineEdit = QtWidgets.QLineEdit()

        self.sendMessage = QtWidgets.QPushButton("Отправить")
        self.sendMessage.clicked.connect(self.sendClick)

        self.messageLayout = QtWidgets.QHBoxLayout()
        self.messageLayout.addWidget(QtWidgets.QLabel("Сообщение: "))
        self.messageLayout.addWidget(self.messageLineEdit)
        self.messageLayout.addWidget(self.sendMessage)

        self.serverInput = QtWidgets.QLineEdit()
        self.serverInput.setText("localhost")
        self.portInput = QtWidgets.QLineEdit()
        self.portInput.setText("8080")
        self.pseudoInput = QtWidgets.QLineEdit()
        self.pseudoInput.setText("Ваше имя")
        self.connectButton = QtWidgets.QPushButton("Соединиться")
        self.connectButton.clicked.connect(self.connection)
        self.connectButton.setDefault(True)

        self.connectionLayout = QtWidgets.QHBoxLayout()
        self.connectionLayout.addWidget(QtWidgets.QLabel("Адрес:"))
        self.connectionLayout.addWidget(self.serverInput)
        self.connectionLayout.addWidget(QtWidgets.QLabel("Порт: "))
        self.connectionLayout.addWidget(self.portInput)
        self.connectionLayout.addWidget(QtWidgets.QLabel("Имя: "))
        self.connectionLayout.addWidget(self.pseudoInput)
        self.connectionLayout.addWidget(self.connectButton)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.connectionLayout)
        self.mainLayout.addWidget(self.messages)
        self.mainLayout.addLayout(self.messageLayout)

        self.setLayout(self.mainLayout)

        #Network
        self.socket = QtNetwork.QTcpSocket(self)
        self.socket.readyRead.connect(self.readData)
        self.socket.error.connect(self.displayError)

    def closeEvent(self, event):
        self.socket.disconnectFromHost()

    def connection(self):
        self.socket.connectToHost(self.serverInput.text(), int(self.portInput.text()))
        if self.socket.waitForConnected(1000):
            self.pseudo = self.pseudoInput.text()
            self.send("login %s" % self.pseudo)
            self.connectButton.setEnabled(False)
            self.sendMessage.setDefault(True)
            self.messageLineEdit.setFocus()
            #self.setWindowTitle("<%s>" % self.pseudo)

    def readData(self):
        message = self.socket.readLine().data().decode("utf-8")
        self.messages.append(message)

    def send(self, message):
        self.socket.write(message.encode("utf-8"))

    def sendClick(self):
        message = "say %s" % (self.messageLineEdit.text())
        self.send(message)
        self.messageLineEdit.clear()
        self.messageLineEdit.setFocus()

    def displayError(self):
        QtWidgets.QMessageBox.information(self, "Соединение", "Ошибка соединения")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    sys.exit(client.exec_())