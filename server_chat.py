import random
from PyQt5 import QtCore, QtNetwork

class Server(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)
        self.newConnection.connect(self.newClient)

        self.clients = {}

    def newClient(self):
        client = self.nextPendingConnection()
        client.readyRead.connect(self.readData)
        client.disconnected.connect(self.disconnectClient)
        self.clients[client] = {}
        self.clients[client]["pseudo"] = u"guest-%d" % random.randint(1, 1000)

    def disconnectClient(self):
        socket = self.sender()
        self.sendAll("<em>Déconnexion de %s</em>" % self.clients[socket]["pseudo"])
        self.clients.pop(socket)

    def readData(self):
        socket = self.sender()
        line = socket.readLine().data().decode("utf-8")
        cmd, value = line.split(" ", 1)
        if cmd == "login":
            if self.pseudoExist(value):
                pseudo = self.clients[socket]["pseudo"]
                self.send(socket, "<em>Pseudo déja pris. Assignement automatique...</em>")
            else:
                pseudo = value
                self.clients[socket]["pseudo"] = pseudo
            self.sendAll("<em>Connexion de %s</em>" % pseudo)
        elif cmd == "say":
            message = "<%s> : %s" % (self.clients[socket]["pseudo"], value)
            self.sendAll(message)

    def send(self, socket, message):
        socket.write(message.encode("utf-8"))

    def sendAll(self, message):
        for c in self.clients:
            self.send(c, message)

    def pseudoExist(self, pseudo):
        for c in self.clients:
            if pseudo == self.clients[c]["pseudo"]:
                return True

if __name__ == '__main__':

    import sys, signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtCore.QCoreApplication(sys.argv)
    serv = Server()
    port = 8080
    serv.listen(port=port)
    print("Сервер запущен на порту %d" % port)
    sys.exit(app.exec_())