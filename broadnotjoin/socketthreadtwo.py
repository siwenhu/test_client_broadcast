#coding:utf-8
'''
Created on 2015年5月13日

@author: root
'''
from PyQt4.QtCore import QThread, SIGNAL, QByteArray, QTimer, QTime, QString
from PyQt4.QtNetwork import QUdpSocket, QHostAddress, QAbstractSocket
from PyQt4.QtGui import QMessageBox, QApplication
import sys
import time
import uuid
import globalfunc
class SocketThread(QThread):
    def __init__(self,parent=None):
        super(SocketThread,self).__init__(parent)
        self.clientuuid = str(uuid.uuid4())
        self.list = []
        self.timetemp = ""
        self.msginfo = QByteArray()
        self.port = 5555
        self.broadFlag = True
        self.startReceive = False
        self.porttwo = 5556
        
        self.datagramcount = 40
        
        self.datanum = 0
        self.datareceivenum = 0
        self.localframenum = 0
        self.avilableframenum = 0
        self.necnum = 0
        
        self.framedata = {}
        self.framelist = {}
        self.framedatalist = []
        self.currentframe = ""
        
        self.dataframelist = {}
        
        self.teacherIp = ""
        #self.slotTimer = QTimer()
        #self.slotTimer.start(3000)
        #self.connect(self.slotTimer, SIGNAL("timeout()"),self.writeDataToSocket)
        
        
        self.udpSocket = QUdpSocket(self)
        #self.udpSocket.setReadBufferSize(1024*1024*2)
        self.udpSocket.setReadBufferSize(1024*1024)
        
        self.connect(self.udpSocket,SIGNAL("readyRead()"),self.dataReceived)
        result = self.udpSocket.bind(self.port)
        
        if not result:
             pass 
        self.mcast_addr_two = QHostAddress("224.0.0.18")
        self.udpSocketTwo = QUdpSocket(self)
        self.udpSocketTwo.setReadBufferSize(1024)
        self.connect(self.udpSocketTwo,SIGNAL("readyRead()"),self.dataReceiveTwo)
        result = self.udpSocketTwo.bind(self.porttwo)
        self.udpSocketTwo.joinMulticastGroup(self.mcast_addr_two)
        if not result:
             pass 
        self.mcast_addr_own = QHostAddress("224.0.0.19")
        
        #self.start()
        
    def dataReceive(self):
        #totalmsg = ""
        self.datareceivenum+=1
        while self.udpSocket.hasPendingDatagrams():
            datagram = QByteArray()
            datagram.resize(self.udpSocket.pendingDatagramSize())
            msglist = self.udpSocket.readDatagram(datagram.size())
            msg = msglist[0]
            timetemp = msg[0:17]
            datanumth = msg[17:19]
            datatotalnum = msg[19:21]
            datacontent = msg[21:]
            
            self.addToLocal(timetemp,datanumth,datatotalnum,datacontent)
            #self.timetemp = msg[0:9]
            #totalmsg = totalmsg+msg
            #self.emit(SIGNAL("imgsignal"),totalmsg)
            self.datanum+=1
            #self.list.append(msg)
            
    def dataReceived(self):
        if self.startReceive == False:
            return
        try:
            msg = self.getDataContent()
            timetemp = msg[0:17]
            datanumth = msg[17:19]
            datatotalnum = msg[19:21]
            datacontent = msg[21:]
            self.addToLocal(timetemp,datanumth,datatotalnum,datacontent)
            self.datanum+=1
        except:
        
    def getDataContent(self):
        while self.udpSocket.hasPendingDatagrams():
            msglist = self.udpSocket.readDatagram(65*1024)  
            
            msg = msglist[0]  
            return msg
        
        return None
    
            
    def addToLocal(self,timetemp,datanumth,datatotalnum,datacontent):
        if self.framedata.has_key(timetemp):
            self.framedata[timetemp][datanumth] = datacontent
            if len(self.framedata[timetemp]) == int(datatotalnum):
                self.localframenum+=1
                self.dataframelist[timetemp] = self.framedata[timetemp]
                self.framedata.pop(timetemp)
        else:
            self.framedata[timetemp] = {}
            self.framedata[timetemp][datanumth] = datacontent
            
            
    def parseLocalData(self):
        framedatas = self.dataframelist
        for key in framedatas.keys():
            if len(framedatas[key]) == self.datagramcount:
                self.localframenum+=1
                dataframe = framedatas[key]
                imgdata = ""
                for i in range(0,self.datagramcount):
                    keys = "%02d"%i
                    imgdata = imgdata + dataframe[keys]
                    #imgdata = dataframe["00"] + dataframe["01"] + dataframe["02"] + dataframe["03"]
                self.framelist[key] = imgdata
                self.framedata.pop(key)
                return
            
    def sortAddLocalList(self):
        if len(self.dataframelist) >= 5:
            keylist = []
            for key in self.dataframelist:
                keylist.append(int(key))
            keylist.sort()
            imgdata = ""
            for i in range(0,len(self.dataframelist[("%017d"%(keylist[0]))])):
                keys = "%02d"%i
                imgdata = imgdata + self.dataframelist[("%017d"%(keylist[0]))][keys]
        
            self.currentframe = imgdata
        
            self.dataframelist.pop(("%017d"%(keylist[0])))
        else:
            self.currentframe = None
            
    def dataReceiveTwo(self):
        while self.udpSocketTwo.hasPendingDatagrams():
            datagram = QByteArray()
            datagram.resize(self.udpSocketTwo.pendingDatagramSize())
            msglist = self.udpSocketTwo.readDatagram(datagram.size())
            msg = str(msglist[0])
            
        self.parseMsg(msg)
        
    def slotStartAllBroadcast(self,msgs):
#         flag = False
#         iplist = msgs.split("#")
#         localip = globalfunc.get_ip_address()
#         for item in iplist:
#             if item == localip:
#                 flag = True
#                 break
#         if flag:
        #self.udpSocket.joinMulticastGroup(self.mcast_addr)#加入组
        self.startReceive = True
        
        self.emit(SIGNAL("startbroadcast"))
        self.datanum = 0
        self.datareceivenum = 0
        self.localframenum = 0
        self.avilableframenum = 0
        self.necnum = 0
        self.broadFlag = True
        self.start()
        
    def slotStartSomeBroadcast(self,fmsgs,smsgs):
        if fmsgs == "somehost" and QString(smsgs).contains(self.clientuuid):
            #self.udpSocket.joinMulticastGroup(self.mcast_addr_own)
            self.startReceive = True
            
            self.emit(SIGNAL("startbroadcast"))
            self.datanum = 0
            self.datareceivenum = 0
            self.localframenum = 0
            self.avilableframenum = 0
            self.necnum = 0
            self.broadFlag = True
            self.start()
    
    def slotStopBroadcast(self):
        pass
    def slotSetMousePos(self,msg):
        if len(msg.split("#")) == 3:
            mousex = int(msg.split("#")[1])
            mousey = int(msg.split("#")[2])
            self.emit(SIGNAL("mousepos"),mousex,mousey)
        
    def parseMsg(self,msg):
        if len(msg.split("#")) >= 2:
            if msg.split("#")[0] == "teacherip":
                self.teacherIp = msg.split("#")[1]
                self.emit(SIGNAL("receiveteacherip"),self.teacherIp)
            elif msg.split("#")[0] == "mousepos":
                self.slotSetMousePos(msg)
            elif msg.split("#")[0] == "startbroadcast":
                self.slotStartAllBroadcast(msg)
                    
            elif msg.split("#")[0] == "stopbroadcast":
                #self.udpSocket.leaveMulticastGroup(self.mcast_addr_own)
                self.startReceive = True
                    
                self.emit(SIGNAL("stopbroadcast"))
                self.broadFlag = False
#                 lent = len(self.framedata)
#                 file = open("frame.txt","w")
#                 file.write(QString.number(self.datanum))
#                 file.write("++")
#                 file.write(QString.number(self.datareceivenum))
#                 file.write("++")
#                 file.write(QString.number(self.localframenum))
#                 file.write("++")
#                 file.write(QString.number(self.necnum))
#                 file.write("++")
#                 file.write(QString.number(self.avilableframenum))
#                 file.write("++")
#                 file.write(QString.number(lent))
#                 file.close()
                
                self.framedata.clear()
                self.dataframelist.clear()
                self.currentframe = None
            

    def writeDataToSocket(self):
        hour = "%02d"%(QTime.currentTime().hour())
        minute = "%02d"%(QTime.currentTime().minute())
        second = "%02d"%(QTime.currentTime().second())
        if self.teacherIp != "":
            ip = self.teacherIp
            name = "client-" + self.clientuuid
            data = name + "#" + hour + minute + second
            self.udpSocket.writeDatagram(data, QHostAddress(ip), self.porttwo)
            
            
    def run(self):
        #return
        while self.broadFlag:
            self.sortAddLocalList()
            if self.currentframe == None:
                time.sleep(0.01)
                continue
            
            msg = self.currentframe
            #if self.msginfo != msg:
            self.necnum+=1
            self.avilableframenum+=1
            self.emit(SIGNAL("imgsignal"),msg)
            self.msginfo = msg
                    
            time.sleep(0.01)
    
    def pickImage(self,list):
        if len(self.list) >=10:
            self.list.remove(self.list[0])
        imglist = []    
        if len(list) <= 2:
            return []
        #timetemp = list[0][0:9]
        for item in list:
            if item[0:9] == self.timetemp:
                imglist.append(item)
        if len(imglist) == 4:
            self.list.remove(imglist[0])
            self.list.remove(imglist[1])
            self.list.remove(imglist[2])
            self.list.remove(imglist[3])
            return imglist
        else:
            return []
        
            
# app = QApplication(sys.argv)
# thread = SocketThread()
# app.exec_()


