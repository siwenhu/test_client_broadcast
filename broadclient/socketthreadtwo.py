#coding:utf-8
'''
Created on 2015年5月13日

@author: root
'''
from PyQt4.QtCore import QThread, SIGNAL, QByteArray, QTimer, QTime, QString
from PyQt4.QtNetwork import QUdpSocket, QHostAddress, QAbstractSocket
from PyQt4.QtGui import QMessageBox, QApplication, QCursor
from logrecord import LogRecord
from broadclient.waitingteacher import WaitingTeacher
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
        self.broadFlag = False 
        self.currentStudent = False
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
        
        #self.mouseTimer = QTimer()
        #self.connect(self.mouseTimer, SIGNAL("timeout()"),self.broadTheMousePos)

        self.teacherIp = ""
        #self.slotTimer = QTimer()
        #self.slotTimer.start(3000)
        #self.connect(self.slotTimer, SIGNAL("timeout()"),self.writeDataToSocket)

        self.waitingTimer = QTimer()
        self.waitingTimer.start(10000)
        self.connect(self.waitingTimer, SIGNAL("timeout()"),self.slotStopBroadcastTimeout)
 
        self.waitingTeacher = WaitingTeacher()
        self.connect(self.waitingTeacher, SIGNAL("receive_data"),self.operateTeacherMsg)
        
        self.udpSocket = QUdpSocket(self)
        #self.udpSocket.setReadBufferSize(1024*1024*2)
        self.udpSocket.setReadBufferSize(1024*1024)
        
        self.connect(self.udpSocket,SIGNAL("readyRead()"),self.dataReceive)
        self.results = self.udpSocket.bind(self.port)
        self.mcast_addr = QHostAddress("224.0.0.17")
        
        self.mcast_addr_two = QHostAddress("224.0.0.18")
        self.udpSocketTwo = QUdpSocket(self)
        self.udpSocketTwo.setReadBufferSize(1024)
        self.connect(self.udpSocketTwo,SIGNAL("readyRead()"),self.dataReceiveTwo)
        self.result = self.udpSocketTwo.bind(self.porttwo)
        if self.result:
            self.joinGroup = self.udpSocketTwo.joinMulticastGroup(self.mcast_addr)
            self.joinGroupTwo = self.udpSocketTwo.joinMulticastGroup(self.mcast_addr_two)
            print("joinmulticastGroup %d" % self.joinGroup)
            
        self.mcast_addr_own = QHostAddress("224.0.0.19")
        
        #self.start()
    def bindUdpPort(self):
        if not self.results:
            self.results = self.udpSocket.bind(self.port)
            self.udpSocket.joinMulticastGroup(self.mcast_addr)
        if not self.result:
            self.result = self.udpSocketTwo.bind(self.porttwo)   
            self.udpSocketTwo.joinMulticastGroup(self.mcast_addr_two)
        if not self.joinGroup: 
            self.udpSocket.joinMulticastGroup(self.mcast_addr)
        if not self.joinGroupTwo:
            self.udpSocketTwo.joinMulticastGroup(self.mcast_addr_two)
            
    def dataReceive(self):
        self.datareceivenum+=1
        while self.udpSocket.hasPendingDatagrams():
            datagram = QByteArray()
            datagram.resize(self.udpSocket.pendingDatagramSize())

            msglist = self.udpSocket.readDatagram(datagram.size())
            if self.broadFlag == False:
                continue
            msg = msglist[0]
            timetemp = msg[0:17]
            datanumth = msg[17:19]
            datatotalnum = msg[19:21]
            datacontent = msg[21:]
            
            self.addToLocal(timetemp,datanumth,datatotalnum,datacontent)
            self.datanum+=1
            
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
            
        LogRecord.instance().logger.info(self.joinGroup)
    def sortAddLocalList(self):
        if len(self.dataframelist) > 100:
            self.dataframelist.clear()
            return
        if len(self.framedata) > 100:
            self.framedata.clear()
            return

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
        
    def broadTheMousePos(self):
        currentPosX = QCursor.pos().x()
        currentPosY = QCursor.pos().y()
        msg = "mousepos#" + str(currentPosX) + "#" + str(currentPosY)
        if self.currentPosMsg != msg:
            self.currentPosMsg = msg
            self.udpSocketTwo.writeDatagram(msg, self.mcast_addr_two, self.porttwo)
        else:
            pass

    def operateTeacherMsg(self,msg):

        if self.results and self.result and self.joinGroup and self.joinGroupTwo:
            pass
        else:
            self.bindUdpPort()

        if len(msg.split("#")) == 3 and msg.split("#")[0] == "teacherip":
            self.waitingTimer.stop()
            self.waitingTimer.start(10000)
            if msg.split("#")[2] == "false":
                return 
            else:
                if self.broadFlag:
                    pass
                else:
                    if self.currentStudent:
                        #self.mouseTimer.start(40)
                        pass
                    else:
                        self.slotStartAllBroadcast(msg)
        else:
            pass

    def slotStartAllBroadcast(self,msgs):
#         flag = False
#         iplist = msgs.split("#")
#         localip = globalfunc.get_ip_address()
#         for item in iplist:
#             if item == localip:
#                 flag = True
#                 break
#         if flag:

        self.emit(SIGNAL("startbroadcast"))
        self.datanum = 0
        self.datareceivenum = 0
        self.localframenum = 0
        self.avilableframenum = 0
        self.necnum = 0
        self.broadFlag = True
        self.start()

    def slotStartStuBroadcast(self,msgs):
        stuip = msgs.split("#")[1]
        localip = globalfunc.get_ip_address()
        if stuip == localip:
            pass
        else:
            self.udpSocket.joinMulticastGroup(self.mcast_addr)#加入组
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
            self.udpSocket.joinMulticastGroup(self.mcast_addr_own)
            
            self.emit(SIGNAL("startbroadcast"))
            self.datanum = 0
            self.datareceivenum = 0
            self.localframenum = 0
            self.avilableframenum = 0
            self.necnum = 0
            self.broadFlag = True
            self.start()
    
    def slotStopBroadcast(self):
        self.udpSocket.leaveMulticastGroup(self.mcast_addr_own)
        self.emit(SIGNAL("stopbroadcast"))
        self.broadFlag = False
        self.currentStudent = False
        self.framedata.clear()
        self.dataframelist.clear()
        self.currentframe = None
        #self.mouseTimer.stop()

    def slotStopBroadcastTimeout(self):
        self.udpSocket.leaveMulticastGroup(self.mcast_addr_own)
        self.emit(SIGNAL("stopbroadcast"))
        self.broadFlag = False
        self.framedata.clear()
        self.dataframelist.clear()
        self.currentframe = None
        #self.mouseTimer.stop()


    def slotSetMousePos(self,msg):
        if len(msg.split("#")) == 3:
            mousex = int(msg.split("#")[1])
            mousey = int(msg.split("#")[2])
            self.emit(SIGNAL("mousepos"),mousex,mousey)
            #self.slotStopBroadcast()
        
    def parseMsg(self,msg):
        if len(msg.split("#")) >= 2:
            if msg.split("#")[0] == "teacherip":
                self.teacherIp = msg.split("#")[1]
                self.emit(SIGNAL("receiveteacherip"),self.teacherIp)
            elif msg.split("#")[0] == "mousepos":
                self.slotSetMousePos(msg)
            elif msg.split("#")[0] == "startbroadcast":
                LogRecord.instance().logger.info("startbroadcast")
                self.slotStartAllBroadcast(msg)
                
            elif msg.split("#")[0] == "startstucomputerbroadcast":
                self.slotStartStuBroadcast(msg)
                    
            elif msg.split("#")[0] == "stopbroadcast":
                self.udpSocket.leaveMulticastGroup(self.mcast_addr_own)
                    
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


