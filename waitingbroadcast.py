# -*- coding: utf-8 -*-  
from PyQt4.QtCore  import QObject, SIGNAL, QByteArray, QString
from PyQt4.QtGui import QMessageBox
from PyQt4.QtNetwork import QUdpSocket, QHostAddress
from logrecord import LogRecord
import common
        
class WaitingBroadCast(QObject):  
    def __init__(self,parent=None):  
        super(WaitingBroadCast,self).__init__(parent)  

        self.port = common.BROAD_CAST_PORT  
        self.udpSocket = QUdpSocket(self)  
        self.connect(self.udpSocket,SIGNAL("readyRead()"),self.dataReceived)  
          
        self.result = self.udpSocket.bind(self.port)  
        if not self.result:  
            LogRecord.instance().logger.info(u'udpserver create error!')
            return  

    def dataReceived(self):
        while self.udpSocket.hasPendingDatagrams():
            msglist = self.udpSocket.readDatagram(self.port)  
            msg = msglist[0]  
            self.emit(SIGNAL("operaterCmd"), msg)
        
    def bindUdpPort(self):
        if not self.result:
            self.result = self.udpSocket.bind(self.port)
    
from PyQt4.QtGui import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WaitingBroadCast()
    app.exec_()
            
