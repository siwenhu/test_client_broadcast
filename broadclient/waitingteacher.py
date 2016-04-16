#coding:utf-8

from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtNetwork import QUdpSocket
from PyQt4.QtGui import QApplication
import sys 

class WaitingTeacher(QObject):

    def __init__(self,parent=None):
        super(WaitingTeacher,self).__init__(parent)
        self.waitingport = 5557
        self.udpSocket = QUdpSocket()
        self.udpSocket.bind(self.waitingport)
        self.connect(self.udpSocket, SIGNAL("readyRead()"),self.dataReceive)

    def dataReceive(self):
        while self.udpSocket.hasPendingDatagrams():
            msglist = self.udpSocket.readDatagram(self.waitingport)
            msg = msglist[0]
            self.emit(SIGNAL("receive_data"),msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wait = WaitingTeacher()
    app.exec_()  
