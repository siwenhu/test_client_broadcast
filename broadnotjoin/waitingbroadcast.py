# -*- coding: utf-8 -*-  
from PyQt4.QtCore  import QObject, SIGNAL, QByteArray, QString
from PyQt4.QtGui import QMessageBox
from PyQt4.QtNetwork import QUdpSocket, QHostAddress
from logrecord import LogRecord
import common
        
class WaitingBroadCast(QObject):  
    def __init__(self,parent=None):  
        super(WaitingBroadCast,self).__init__(parent)  

        self.port = 5555 
        self.udpSocket = QUdpSocket(self)  
        self.connect(self.udpSocket,SIGNAL("readyRead()"),self.dataReceived)  
          
        result = self.udpSocket.bind(self.port)  
        if not result:  
            LogRecord.instance().logger.info(u'udpserver create error!')
            return  

    def dataReceived(self):
        try:
            dataValue = self.getDataContent()
            if dataValue:
                LogRecord.instance().logger.info(u'接收到广播信息：%s' % dataValue)
                self.emit(SIGNAL("operaterCmd"), dataValue)
        except:
            LogRecord.instance().logger.info(u'广播信息有误：%s' % dataValue)
        
        
    def getDataContent(self):
        while self.udpSocket.hasPendingDatagrams():
            msglist = self.udpSocket.readDatagram(self.port)  
            msg = msglist[0]  
            return msg
        
        return None
    
    
    
    
    
    
from PyQt4.QtGui import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WaitingBroadCast()
    app.exec_()
            
