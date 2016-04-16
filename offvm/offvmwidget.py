# -*- coding: utf-8 -*-  

from PyQt4.QtCore import Qt, QSize, SIGNAL, QString, QTimer, QThread, QTranslator, QCoreApplication
from PyQt4.QtGui  import QWidget, QIcon, QFont, QHBoxLayout, QSlider, QVBoxLayout, QScrollArea, QAbstractItemView, QTableWidget, QFrame
from vminfomanager import VMInfoManager
from vmoperation import VMOperation
from customvmbutton import CustomVMButton
from windowMonitor import WindowMonitor

from offvm.downloadthread import DownloadThread
from offvm.progressthread import ProgressThread
from offvm.myprogress import WidgetProgress
#from offvm.customvmbutton import CustomVMButton
from offvm.domtest import DomainManager
from offvm import domtest
from offvm.localimgmanager import LocalImgManager

import common
import globalvariable
import globalfunc
from logrecord import LogRecord
from storeinfoparser import StoreInfoParser
import time
import os
import commands
from networkmanager import NetworkManager
import thread

class VMWidget(QWidget):
        
    def __init__(self,parent = None):
        super(VMWidget,self).__init__(parent)
        
        #self.setStyleSheet("QToolTip{background-color:white;color:black;font-size:12px;}")
        #self.setFont(QFont(u"微软雅黑",12))
        self.vmInfoList = []
        self.oldVmInfoList = [] 
        self.vmOffInfoList = []
        self.threadMap = {}
        self.processMap = {}
        self.parent = parent
        self.domainManager = DomainManager()
        self.progressMonitor = ProgressThread()
        self.vmstatusTimer = QTimer()
        #self.vmstatusTimer.start(7000)
        self.connect(self.vmstatusTimer, SIGNAL("timeout()"),self.postStatusToServer)
        self.startVmInfo = None
        if common.SCROLL_TYPE != "slider":
            self.scrollArea = QScrollArea(self)
            self.scrollArea.setStyleSheet("background-color:transparent;border:0px")
            self.vmButtonList = []
            self.vmTableWidget = QTableWidget()
            self.setTableWidgetStyle()
            
            self.mainLayout = QVBoxLayout()
            self.mainLayout.setMargin(0)
            self.mainLayout.setSpacing(0)
            self.mainLayout.addWidget(self.scrollArea)
            self.mainLayout.addSpacing(10)
        
            self.setLayout(self.mainLayout)
        
        
            self.downloadingList = []
        
            
            
        if common.SCROLL_TYPE == "slider":
            #三个自定义button，用于显示相应的虚拟机
            self.firstVM   = CustomVMButton(self)
            self.secondVM  = CustomVMButton(self)
            self.thirdVM   = CustomVMButton(self)
             
            self.vmButtonList = [self.firstVM, self.secondVM, self.thirdVM]
             
            for i in range(len(self.vmButtonList)):
                self.vmButtonList[i].setIcon(QIcon("images/windows.png"))
                self.vmButtonList[i].setIconSize(QSize(100,100))
                self.vmButtonList[i].setFlat(True)
                self.vmButtonList[i].setFont(QFont("Times", 15, QFont.Bold))
            
            #设置滑动条的样式
            self.slider = QSlider(Qt.Vertical,self)
            self.slider.setStyleSheet( "QSlider::groove:vertical {  "
                                        "border: 1px solid #4A708B;  "
                                        "background: #C0C0C0;  "
                                        "width: 5px;  "
                                        "border-radius: 1px;  "
                                        "padding-left:-1px;  "
                                        "padding-right:-1px;  "
                                        "padding-top:-1px;  "
                                        "padding-bottom:-1px;  "
                                        "}"
                                        "QSlider::handle:vertical {"
                                        "height: 100px;"
                                        "background: white;"
                                        "margin: 0 -4px;"
                                        "}" )
             
            self.btnLayout = QHBoxLayout(self)
            self.btnLayout.addStretch()
            self.btnLayout.addWidget(self.firstVM)
            self.btnLayout.addWidget(self.secondVM)
            self.btnLayout.addWidget(self.thirdVM)
            self.btnLayout.addStretch()
            self.btnLayout.addSpacing(10)
            self.btnLayout.addWidget(self.slider)
            self.btnLayout.setSpacing(10)
            self.btnLayout.setMargin(10)
             
            self.setLayout(self.btnLayout)
            
    def setTableWidgetStyle(self):
        
        #self.vmTableWidget.setColumnCount(3)
        #self.vmTableWidget.setRowCount(1)
        self.vmTableWidget.setFrameShape(QFrame.NoFrame)
        self.vmTableWidget.setEditTriggers(QTableWidget.NoEditTriggers)#不能编辑
        self.vmTableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.vmTableWidget.verticalHeader().setVisible(False)#设置垂直头不可见
        self.vmTableWidget.horizontalHeader().setVisible(False)#设置垂直头不可见
        self.vmTableWidget.setShowGrid(False)
        self.vmTableWidget.setFocusPolicy(Qt.NoFocus)
        
        self.vmTableWidget.setStyleSheet("QTableWidget{background-color: rgb(235, 235, 235,0);}")    
    
    def getVmList(self):
        vmList = []
        vmInfo = {}
        vmInfo["name"] = "15615123021654541"
        vmInfo["status"] = "offline"
        vmInfo["name"] = "offline"
        vmInfo["os_distro"] = "windows_7"
        
        
        vmInfo1 = {}
        vmInfo1["name"] = "1561545421654541"
        vmInfo1["status"] = "offline"
        vmInfo1["name"] = "offline"
        
        vmInfo2 = {}
        vmInfo2["name"] = "1561afew21654541"
        vmInfo2["status"] = "offline"
        vmInfo2["name"] = "windows_7"
        
        vmInfo3 = {}
        vmInfo3["name"] = "afewfdsafewfa"
        vmInfo3["status"] = "offline"
        vmInfo3["name"] = "windows_7"
        
        vmList.append(vmInfo)
        vmList.append(vmInfo1)
        vmList.append(vmInfo2)
        vmList.append(vmInfo3)
        vmList.append(vmInfo1)
        vmList.append(vmInfo2)
        vmList.append(vmInfo3)
        
        return vmList
    def postStatusToServer(self):
        '''serverState = VMInfoManager.instance().getCurCloudServerState()
        if serverState != "enable":
            return'''
        postInfo = {}
        state = self.domainManager.getStatus()
        if self.vmOffInfoList == [] or len(self.downloadingList) != 0:
            #self.processMap.clear()
            #self.threadMap.clear()
            return
        if len(state) == 0:
            postInfo["state"] = "shutdown"
            postInfo["vmname"] = self.vmOffInfoList[0]["vmname"]
        else:
            for item in state:
                postInfo["state"] = "running"
                if state[item].has_key("disk_io"):
                    postInfo["io_throughput"] = state[item]["disk_io"]
                if state[item].has_key("max_disk_io"):
                    postInfo["io_throughput_peak"] = state[item]["max_disk_io"]
                if state[item].has_key("net_io"):
                    postInfo["net_throughput"] = state[item]["net_io"]
                if state[item].has_key("max_net_io"):
                    postInfo["net_throughput_peak"] = state[item]["max_net_io"]
                if state[item].has_key("memory_size"):
                    postInfo["memory"] = state[item]["memory_size"]*1024
                if state[item].has_key("vmname"):
                    postInfo["vmname"] = state[item]["vmname"]
                if state[item].has_key("name"):
                    postInfo["coursename"] = state[item]["name"]
                if state[item].has_key("cpu"):
                    postInfo["cpu_utilization"] = state[item]["cpu"]     
        self.emit(SIGNAL("vmstateinfo"),postInfo)
        
    def showVmList(self):
        subWidget = QWidget()
        if self.vmstatusTimer.isActive():
            pass
        else:
            #if globalvariable.CLASS_STATUS:
            self.vmstatusTimer.start(7000)
            #self.connect(self.vmstatusTimer, SIGNAL("timeout()"),self.postStatusToServer)
        
        if self.scrollArea.widget():
            self.scrollArea.takeWidget()
            
        self.vmTableWidget = QTableWidget()
        self.setTableWidgetStyle()
        #if self.vmTableWidget
        self.vmTableWidget.clear()
    
        #self.vmInfoList = self.getVmList()
        num = len(self.vmInfoList)
        columnCount = 1
        rowCount = 1
        if num == 0:
            return
        if num <=3:
            #self.scrollArea.verticalScrollBar().hide()
            rowCount = 1
            if num == 1:
                columnCount = 1
            elif num == 2:
                columnCount = 2
            elif num == 3:
                columnCount = 3
        else:
            rowCount = num/3
            rest = num%3
            if (rowCount == 2 and rest == 0)  or rowCount == 1 :
                pass
            if rest > 0:
                rowCount+=1
                
            columnCount = 3
        
        
        parentWidth = self.parent.width()
        resolutionValue = StoreInfoParser.instance().getResolutionValue()
        if resolutionValue:
            if len(resolutionValue.split("x")) >= 2:
                parentWidth = int(resolutionValue.split("x")[0])*5/9.0
        ratio = parentWidth/800.0
        tableWidth = (parentWidth - 20*2 -50*2*ratio)/3 + 5
        if len(self.vmInfoList) > 3:
            tableWidth = (parentWidth - 20*2 -50*2*ratio)/3 - 20*(1 - ratio) + 5
                
        self.vmTableWidget.setColumnCount(columnCount)
        self.vmTableWidget.setRowCount(rowCount)
        self.vmTableWidget.setFixedWidth(parentWidth-100)
        self.vmTableWidget.setFixedHeight((tableWidth+10)*rowCount)
        self.vmTableWidget.verticalHeader().setDefaultSectionSize(tableWidth+10)
        self.vmTableWidget.horizontalHeader().setDefaultSectionSize((parentWidth-100)/columnCount)
        #self.setWidget("status")
        if columnCount <= 3 and rowCount == 1:
            for i in range(columnCount):
                self.setRowColumnWidget(0,i,self.vmInfoList[i]["name"])
        else:
            for i in range(rowCount):
                for j in range(3):
                    if i*3 + j <= num-1:
                        self.setRowColumnWidget(i, j, self.vmInfoList[i*3+j]["name"])  
        
        mainLayout = QHBoxLayout()
        mainLayout.setMargin(0)
        mainLayout.addWidget(self.vmTableWidget)
        subWidget.setLayout(mainLayout)
        #if self.scrollArea.widget():
            #self.scrollArea.takeWidget()
        self.scrollArea.setWidget(subWidget) 
        self.scrollArea.setWidgetResizable(True) 
        #self.scrollArea.horizontalScrollBar().hide()   
    def setRowColumnWidget(self,row,column,vmid):
        status = "sfw"
        #self.vmTableWidget.clear()
        mainWidget = QWidget()
        #self.vmTableWidget.hideColumn()
        #vmRowButtonList = []
        parentWidth = self.parent.width()
        resolutionValue = StoreInfoParser.instance().getResolutionValue()
        if resolutionValue:
            if len(resolutionValue.split("x")) >= 2:
                parentWidth = int(resolutionValue.split("x")[0])*5/9.0
        ratio = parentWidth/800.0
        vmWidth = (parentWidth - 20*2 -50*2*ratio)/3
        if len(self.vmInfoList) > 3:
            vmWidth = (parentWidth - 20*2 -50*2*ratio)/3 - 20*(1 - ratio)
        
        vmButton = CustomVMButton()
        vmButton.setFixedSize(QSize(vmWidth, vmWidth + 5))
        vmButton.setIconSize(QSize(vmWidth - 60*ratio,vmWidth - 30*ratio))
        vmButton.setText(self.vmInfoList[row*3 + column]["name"])
        vmButton.setFlat(True)
        vmButton.setFont(QFont("Times", 15, QFont.Bold))
        vmInfo = self.vmInfoList[row*3 + column]
        vmButton.setVMInfo(vmInfo)
        imageName = "other.png"
        if self.vmInfoList[row*3 + column].has_key("os_distro"):
            if common.imageMap.has_key(self.vmInfoList[row*3 + column]["os_distro"]):
                imageName = common.imageMap[self.vmInfoList[row*3 + column]["os_distro"]]
            else:
                LogRecord.instance().logger.info(u'common.imageMap中未找到键值%s' % self.vmInfoList[row*3 + column]["os_distro"])
                        
        vmButton.setIcon(QIcon("images/systemImage/%s" % imageName))
                
#         if globalvariable.CLASS_STATUS and not globalvariable.TICHU_STATUS:
#             self.connect(vmButton, SIGNAL("clicked()"),self.slotOpenVMLesson)
#             self.connect(vmButton, SIGNAL("controlvm"),self.slotControlVM)
#         else:
#             self.connect(vmButton, SIGNAL("clicked()"),self.slotCreateVMLesson)
                    
        #vmRowButtonList.append(vmButton)
        self.vmButtonList.append(vmButton)
        #firMybutton.setStatus("undownload")
        vmButton.setObjectName(vmid + ":" + QString.number(row) + ":" + QString.number(column))
        self.connect(vmButton, SIGNAL("clicked()"),self.startDomain)
        
            
        progressBar = WidgetProgress()
        progressBar.setFixedSize(vmWidth, vmWidth + 5)
        #progressBar.progressBar.setValue(0)
        progressBar.setVmName(self.vmInfoList[row*3 + column]["name"])
        progressBar.setObjectName(vmid + ":" + QString.number(row) + ":" + QString.number(column))
        #progressBar.objectName()
        
        #self.firMybutton.setText(self.tr("确萨"))
        
        #progressBar = QProgressBar()
        
        myLayout = QHBoxLayout()
        myLayout.setMargin(0)
        myLayout.addStretch()
        myLayout.addWidget(vmButton)
        myLayout.addWidget(progressBar)
        myLayout.addStretch()
        
        if vmid in self.downloadingList:
            vmButton.hide()
        else:
            progressBar.hide()
             
        #firMybutton.hide()
        mainWidget.setLayout(myLayout)
        
        
        self.vmTableWidget.setCellWidget(row, column, mainWidget)
        #self.mainLayout.addWidget(mainWidget)  
    
    def setVMInfoList(self, vmInfoList, vmOffInfoList):
        
        self.oldVmInfoList = LocalImgManager.instance().getCompleteList()
        self.vmInfoList = vmInfoList
        self.vmOffInfoList = vmOffInfoList
        self.domainManager.deleteImgList(vmOffInfoList)
        
#         needDeleteList = self.compareDelete(self.oldVmInfoList, vmOffInfoList)
        if self.vmOffInfoList == []:
            #self.progressMonitor.stop()
            #self.threadMap.clear()
            for item in self.processMap:
                self.processMap[item].stop()
                if self.processMap[item].isRunning():
                    self.processMap[item].exit()
            for item in self.threadMap:
                if self.threadMap[item].isRunning():
                    self.threadMap[item].exit()
                
            self.processMap.clear()
            self.threadMap.clear()
            #self.killRsyncThread()
            
#         if len(needDeleteList) == 0:
#             return
#         else:
#             self.domainManager.deleteImgList(needDeleteList)
    def stopAllDownload(self):
        for item in self.processMap:
            self.processMap[item].stop()
            if self.processMap[item].isRunning():
                self.processMap[item].exit()
                
        self.killScpThread()
        for item in self.threadMap:
            #self.threadMap[item].stop()
            if self.threadMap[item].isRunning():
                self.threadMap[item].exit()
        
        self.downloadingList = []
        self.processMap.clear()
        self.threadMap.clear()
    def killScpThread(self):
        pidList = self.getScpsProcessId()
        #sshPidList = self.getSshProcessId()
        for item in pidList:
            self.killVmId(item)
        '''for mtem in sshPidList:
            self.killVmId(mtem)'''
        
    def killVmId(self,killid):
        cmd = "kill -9 " + killid
        os.system(str(cmd))
        
    def getScpsProcessId(self):#得到运行虚拟机的进程号序列，可用于关闭某个虚拟机
        
        idList = []
        cmd = "ps aux | grep scp"
        output = ""
        statusOutput = []
        statusOutput = commands.getstatusoutput(cmd)
        if statusOutput[0] == 0:
                output = statusOutput[1]
        else:
            output = ""
        result = output.split("\n")
        for i in range(len(result)):
            if QString(result[i]).contains("scp"):
                idList.append(QString(result[i]).simplified().split(" ")[1])
    
        return idList
    
    def getSshProcessId(self):#得到运行虚拟机的进程号序列，可用于关闭某个虚拟机
        
        idList = []
        cmd = "ps aux | grep /usr/bin/ssh"
        output = ""
        statusOutput = []
        statusOutput = commands.getstatusoutput(cmd)
        if statusOutput[0] == 0:
                output = statusOutput[1]
        else:
            output = ""
        result = output.split("\n")
        for i in range(len(result)):
            if QString(result[i]).contains("/usr/bin/ssh"):
                idList.append(QString(result[i]).simplified().split(" ")[1])
    
        return idList
    
    def compareDelete(self,oldList,newList):
        nameList = []
        deleteList = []
        for item in newList:
            nameList.append(item["name"])
            
        for name in oldList:
            if name not in nameList:
                deleteList.append(name)
        return deleteList
    
    def autoStartDownload(self):
        #return
        num = len(self.vmInfoList)
        if num == 0:
            return
        else:
            #self.progressMonitor.setVmInfoList(self.vmInfoList)
            #self.progressMonitor.start()
            #self.connect(self.progressMonitor, SIGNAL("downloadover"),self.slotDownloadOver)
            imgMap = LocalImgManager.instance().getCompliteListSize()
            for i in range(len(self.vmInfoList)):
                mark = 0
                for item in imgMap:
                    if item == self.vmInfoList[i]["name"] and imgMap[item] == self.vmInfoList[i]["img_file_size"]:
                        mark = 1
                if mark == 1:
                    continue
                row = i/3
                column = i%3
                self.downloadingList.append(self.vmInfoList[i]["name"])
#                 self.downloadThread = DownloadThread()
#                 self.progressThread = ProgressThread()
                threadid = self.vmInfoList[i]["name"] + ":" + QString.number(row) + ":" + QString.number(column)
#                 self.downloadThread.setProcessId(threadid + ":" + QString.number(self.vmInfoList[i]["img_file_size"]))
#                 self.progressThread.setProcessId(threadid + ":" + QString.number(self.vmInfoList[i]["img_file_size"]))
#                 self.connect(self.progressThread, SIGNAL("currentprogress"),self.updateProgressBar)
#                 self.connect(self.progressThread, SIGNAL("downloadover"),self.slotDownloadOver)
#                 self.downloadThread.start()
#                 self.progressThread.start()
                self.setRowColumnWidget(int(row), int(column), self.vmInfoList[i]["name"])
                self.createThread(threadid,self.vmInfoList[i])
                
                #time.sleep(1)
                #return
            self.startFirstThread()
    def startFirstThread(self):
        for item in self.threadMap:
            self.threadMap[item].start()
            self.processMap[item].start()
            self.connect(self.processMap[item], SIGNAL("currentprogress"),self.updateProgressBar)
            #self.connect(self.processMap[item], SIGNAL("downloadover"),self.slotDownloadOver)
            self.connect(self.threadMap[item], SIGNAL("downloadover"),self.slotDownloadOver)
            self.connect(self.threadMap[item], SIGNAL("downloaderror"),self.slotDownloadError)
            return
        
    def slotDownloadError(self,signalid):
        pass 
    
    def createThread(self,threadid,vmInfo):
        if self.threadMap.has_key(threadid):
            if self.threadMap[threadid].isRunning():
                self.threadMap[threadid].exit()
            self.threadMap.pop(threadid)
        if self.processMap.has_key(threadid):
            if self.processMap[threadid].isRunning():
                self.processMap[threadid].exit()
            self.processMap.pop(threadid)
        
        downloadThread = DownloadThread()
        progressThread = ProgressThread()
        self.threadMap[threadid] = downloadThread
        self.processMap[threadid] = progressThread
        self.threadMap[threadid].setProcessId(threadid + ":" + str(vmInfo["img_file_size"]))
        self.processMap[threadid].setProcessId(threadid + ":" + str(vmInfo["img_file_size"]))
        #self.threadMap[threadid].start()
        #self.processMap[threadid].start()
        #self.connect(self.processMap[threadid], SIGNAL("currentprogress"),self.updateProgressBar)
        #self.connect(self.processMap[threadid], SIGNAL("downloadover"),self.slotDownloadOver)
        
        
    def checkAddDownload(self):
        #return
        
        num = len(self.vmInfoList)
        #existImgList = LocalImgManager.instance().getCompleteList()
        existImgList = LocalImgManager.instance().getCompliteListSize()
        if num == 0:
            return
        else:
            count = 0
            for i in range(len(self.vmInfoList)):
                row = i/3
                column = i%3
                if existImgList.has_key(self.vmInfoList[i]["name"]) and existImgList.get(self.vmInfoList[i]["name"]) == self.vmInfoList[i]["img_file_size"]:
                    pass
                elif self.vmInfoList[i]["name"] in self.downloadingList:
                    pass
                elif existImgList.has_key(self.vmInfoList[i]["name"]) and self.domainManager.getDom() != None and self.startVmInfo != None and self.startVmInfo == self.domainManager.getDomainInfo():
                    pass
                else:
                    if self.vmInfoList[i]["name"] not in self.downloadingList:
                        self.downloadingList.append(self.vmInfoList[i]["name"])
                    threadid = self.vmInfoList[i]["name"] + ":" + QString.number(row) + ":" + QString.number(column)
                    self.createThread(threadid, self.vmInfoList[i])
                    self.setRowColumnWidget(int(row), int(column), self.vmInfoList[i]["name"])
                    count+= 1
                    
            if len(self.threadMap) == count:
                self.startFirstThread()
                if count > 0:
                    self.emit(SIGNAL("startadddownload"))
                
    def startDomain(self): 
        pbp = CustomVMButton().sender()
        buttonName = pbp.objectName()
        vmInfo = pbp.vmInfo
        for item in self.vmOffInfoList:
            if item["name"] == vmInfo["name"]:
                self.startVmInfo = item
        #return
    
        vmid = buttonName.split(":")[0]
        row = buttonName.split(":")[1]
        column = buttonName.split(":")[2]
        
        self.domainManager.setDomainInfo(self.startVmInfo)
        
        LogRecord.instance().logger.info(u"开始开启虚拟机-----------------------------------------------00")
        self.domainManager.startDomainByName()
        LogRecord.instance().logger.info(u"结束开启虚拟机-----------------------------------------------11")
        

    def updateProgressBar(self,count,objectname):
        #if self.threadMap[objectname].isRunning():
#         for i in range(len(self.downloadingList)):
#             if objectname == self.downloadingList[i]:
#                 progress=self.vmTableWidget.findChild((WidgetProgress, ),objectname)
#                 progress.progressBar.setValue(count) 
        progress=self.vmTableWidget.findChild((WidgetProgress, ),objectname)
        if not progress:
            return
        progress.progressBar.setValue(count) 
        
    def slotDownloadOver(self,count,name):
        serverState = VMInfoManager.instance().getCurCloudServerState()
        if serverState != "enable":
            return
        if self.processMap.has_key(name):
            self.processMap[name].stop()
        #self.processMap.pop(name)
        #self.threadMap.pop(name)
        vmid = name.split(":")[0]
        row = name.split(":")[1]
        column = name.split(":")[2]
        self.downloadingList = []
        self.setRowColumnWidget(int(row), int(column), vmid)
        time.sleep(4)
        if self.processMap.has_key(name) and self.processMap[name].isRunning:
            self.processMap[name].exit()
        if self.threadMap.has_key(name) and self.threadMap[name].isRunning:
            self.threadMap[name].exit()
        self.processMap.pop(name)
        self.threadMap.pop(name)
        self.emit(SIGNAL("avmdownloadover"))
#         for item in self.threadMap:
#             self.threadMap[item].start()
#             self.processMap[item].start()
#             self.connect(self.processMap[item], SIGNAL("currentprogress"),self.updateProgressBar)
#             self.connect(self.processMap[item], SIGNAL("downloadover"),self.slotDownloadOver)
#             return
    def getDownloadingList(self):
        return self.downloadingList
            
    def updateVMList(self):
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
            StoreInfoParser.instance().setLanguage("chinese")
        else:
            QmName = "en_US.qm"
            
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
        
        if self.vmstatusTimer.isActive():
            self.vmstatusTimer.stop()
        else:
            pass
        subWidget = QWidget()
        vmNum = len(self.vmInfoList)
        rowNum = 0
        subMainLayout = QVBoxLayout()
        subMainLayout.setMargin(0)
        #subMainLayout.addStretch()
        #subMainLayout.addSpacing(10)
        #subMainLayout.setSpacing(10)
        
        self.vmButtonList = []
        
        if vmNum % 3 != 0:
            rowNum = vmNum / 3 + 1
        else:
            rowNum = vmNum / 3
             
        for i in range(rowNum):
            indexEnd = 3
            if i == rowNum - 1:
                indexEnd = vmNum - (i*3)
                 
            parentWidth = self.parent.width()
            resolutionValue = StoreInfoParser.instance().getResolutionValue()
            if resolutionValue:
                if len(resolutionValue.split("x")) >= 2:
                    parentWidth = int(resolutionValue.split("x")[0])*5/9.0
            
            ratio = parentWidth/800.0
            vmWidth = (parentWidth - 20*2 -50*2*ratio)/3
            if vmNum > 3:
                vmWidth = (parentWidth - 20*2 -50*2*ratio)/3 - 20*(1 - ratio)
            vmRowButtonList = []
            for j in range(indexEnd):
                vmButton = CustomVMButton(self)
                vmButton.setFixedSize(QSize(vmWidth, vmWidth + 5))
                vmButton.setIconSize(QSize(vmWidth - 60*ratio,vmWidth - 30*ratio))
                vmButton.setText(self.vmInfoList[i*3 + j]["name"])
                vmButton.setToolTip(self.tr("course: ") + self.vmInfoList[i*3 + j]["name"])
                vmButton.setStyleSheet(u"QToolTip{border-radius:5px;background-color:white;color:black;font-size:20px;font-family:微软雅黑;}")
                vmButton.setFlat(True)
                vmButton.setFont(QFont("Times", 15, QFont.Bold))
                vmInfo = self.vmInfoList[i*3 + j]
                vmButton.setVMInfo(vmInfo)
                imageName = "other.png"
                if self.vmInfoList[i*3 + j].has_key("os_distro"):
                    if common.imageMap.has_key(self.vmInfoList[i*3 + j]["os_distro"]):
                        imageName = common.imageMap[self.vmInfoList[i*3 + j]["os_distro"]]
                    else:
                        LogRecord.instance().logger.info(u'common.imageMap中未找到键值%s' % self.vmInfoList[i*3 + j]["os_distro"])
                        
                vmButton.setIcon(QIcon("images/systemImage/%s" % imageName))
                if globalvariable.CLASS_STATUS and not globalvariable.TICHU_STATUS:
                    self.connect(vmButton, SIGNAL("clicked()"),self.slotOpenVMLesson)
                    self.connect(vmButton, SIGNAL("controlvm"),self.slotControlVM)
                else:
                    self.connect(vmButton, SIGNAL("clicked()"),self.slotCreateVMLesson)
                    
                vmRowButtonList.append(vmButton)
                self.vmButtonList.append(vmButton)
              
            btnLayout = QHBoxLayout()
            if vmNum > 3:
                btnLayout.setSpacing(10)
                #btnLayout.setMargin(10)
                btnLayout.addSpacing(30)
            for vmbtn in vmRowButtonList:
                btnLayout.addWidget(vmbtn)
            btnLayout.addStretch()
            subMainLayout.addLayout(btnLayout) 
             
        #subMainLayout.addStretch()
        subWidget.setLayout(subMainLayout)
        if self.scrollArea.widget():
            self.scrollArea.takeWidget()
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setWidget(subWidget)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def startVM(self):
        return  
        
    def autoOpenVMLesson(self, vmName, allflag = False):
        LogRecord.instance().logger.info(u'自动打开相应的虚拟机')
        if self.vmButtonList:
            vmInfo = self.vmButtonList[0].getVMInfo()
            VMOperation.instance().setCurrentVMInfo(vmInfo)
            #thread.start_new_thread(VMOperation.instance().openVM,())
            if allflag == True:                      
                if VMOperation.instance().openVM():
                    LogRecord.instance().logger.info(u'start the lesson')  
            else:
                if VMOperation.instance().openVM():
                    LogRecord.instance().logger.info(u'start the lesson')  
        else:
            LogRecord.instance().logger.info(u'未监测到虚拟机%s的信息' % vmName)  
    
    def autoOpenOffVMLesson(self):
        LogRecord.instance().logger.info(u'自动打开相应的虚拟机')
        
        if len(self.vmInfoList) == 1:
            if self.vmInfoList[0]["name"] in self.downloadingList:
                return
            else:
                self.startVmInfo = self.vmInfoList[0]
                self.domainManager.setDomainInfo(self.startVmInfo)
                self.domainManager.startDomainByName()
        
        else:
            return
    def checkDownloadOver(self):
        if self.autoCourse in self.downloadingList:
            pass    
        else:
            self.courseTimer.stop()
            #self.autoCourse = ""
            for item in self.vmOffInfoList:
                if self.autoCourse == item["name"]:
                    vmInfo = item
                    self.domainManager.setDomainInfo(vmInfo)
                    self.domainManager.startDomainByName()
                    return
            
    def autoOpenCourse(self,name,classid = None):
        LogRecord.instance().logger.info(u'自动打开相应的虚拟机')
        self.autoCourse = name
        if name in self.downloadingList:
            self.courseTimer = QTimer()
            self.courseTimer.start(1000)
            self.connect(self.courseTimer, SIGNAL("timeout()"),self.checkDownloadOver)
        
        else:
            for item in self.vmOffInfoList:
                if name == item["name"]:
                    vmInfo = item
                    if classid != None:
                        vmInfo["classid"] = classid
                
                    self.domainManager.setDomainInfo(vmInfo)
                    self.domainManager.startDomainByName()
                    
                    return
                
    def slotCreateVMLesson(self):
        vmBtn = self.sender()
        if vmBtn:
            LogRecord.instance().logger.info(u'开始创建虚拟机')
            if globalvariable.VM_IS_CREATE_STATUS:
                LogRecord.instance().logger.info(u'重复点击！')
                return
            else:
                globalvariable.VM_IS_CREATE_STATUS = True

            LogRecord.instance().logger.info(u'准备获取虚拟机信息！')
            paramInfo = vmBtn.getVMInfo()
            LogRecord.instance().logger.info(u'准备获取虚拟机信息完成！')
            try:
                vmName = VMOperation.instance().createVMLesson(paramInfo)
            except:
                LogRecord.instance().logger.info(u'创建虚拟机异常.........！')
            LogRecord.instance().logger.info(u'得到创建的虚拟机信息！')
            if vmName:
                LogRecord.instance().logger.info(u'创建虚拟机%s成功' % vmName)
                vmInfo = NetworkManager.instance().getVMInfo(vmName)
                if vmInfo == None:
                    globalvariable.VM_IS_CREATE_STATUS = False
                    return
                if len(vmInfo) == 0:
                    globalvariable.VM_IS_CREATE_STATUS = False
                    return
                vmInfo[0]["vmname"] = vmInfo[0]["name"]
                if vmInfo:
                    VMOperation.instance().setCurrentVMInfo(vmInfo[0])
                    if VMOperation.instance().openVM(True):
                        #保存开启虚拟机的名称
                        #globalvariable.VM_IS_CREATE_STATUS = False
                        WindowMonitor.instance().insertVmId(vmName)
                    else:
                        globalvariable.VM_IS_CREATE_STATUS = False
                        #删除没有成功运行的虚拟机
                        if VMOperation.instance().removeVMLesson(vmName):
                            LogRecord.instance().logger.info(u"删除后台相应的虚拟机成功")
                else:
                    LogRecord.instance().logger.info(u'未查询到相应的虚拟机：%s' % vmName)
                    globalvariable.VM_IS_CREATE_STATUS = False
            else:
                LogRecord.instance().logger.info(u'创建虚拟机失败')
                globalvariable.VM_IS_CREATE_STATUS = False


            #刷新虚拟机界面
            self.emit(SIGNAL("refreshVMS"))


    def slotControlVM(self, action):
        vmBtn = self.sender()
        if vmBtn:
            vmInfo = vmBtn.getVMInfo()
            VMOperation.instance().setCurrentVMInfo(vmInfo)
            VMOperation.instance().controlVM(action)
            
            vmInfos = globalvariable.VM_INFO
            self.setVMInfoList(vmInfos,[])
            self.updateVMList()

        
    def slotOpenVMLesson(self):
        #vmInfo = []
        vmBtn = self.sender()
        if vmBtn:
            btnVMInfo = vmBtn.getVMInfo()
            VMOperation.instance().setCurrentVMInfo(btnVMInfo)
            VMOperation.instance().openVM(True)
            
#         if globalvariable.CLASS_STATUS:
#             vmInfo = globalvariable.VM_INFO
#         else:
#             vmInfo = VMInfoManager.instance().getLessonListInfo()
#             
        #self.setVMInfoList(vmInfo,[])
        #self.updateVMList()
    #slider        
    def setSliderMaxValue(self, value):
        """设在滑动条的最大值"""
        maxValue = 1
        if value % 3 == 0:
            maxValue = (value / 3)
        else:
            maxValue = (value / 3 + 1)
         
        maxValue = maxValue - 1
         
        self.slider.setMinimum(1)
        self.slider.setMaximum(maxValue*3)
        self.slider.setValue(self.slider.maximum())
        self.currentIndex = maxValue
        self.maxValue = maxValue
        self.updateVMList()
        
    def paintEvent(self,event):
        if common.SCROLL_TYPE == "slider":
            self.setNodeSize(QSize(self.geometry().width()*4/15,self.geometry().height()*4/9))
        elif len(self.vmInfoList) <= 6:
            subWidget = self.scrollArea.widget()
            if subWidget != None:
                if len(self.vmInfoList) <= 3:
                    subWidget.move((self.geometry().width() - subWidget.width())/2, (self.geometry().height() - subWidget.height())/2 - 20)
                else:
                    subWidget.move((self.geometry().width() - subWidget.width())/2 - 15, (self.geometry().height() - subWidget.height())/2)
        QWidget.paintEvent(self, event)
    
    #slider               
    def setNodeSize(self,size):
        self.btnLayout.setSpacing(size.width()/20)
        self.btnLayout.setMargin(size.width()*3/20)
        
        self.firstVM.setIconSize(size)
        self.secondVM.setIconSize(size)
        self.thirdVM.setIconSize(size)
        
        self.slider.resize(QSize(self.slider.frameGeometry().width(),self.height()-100))
        
    def wheelEvent(self,event):
        """鼠标滚轮滚动事件，显示对应的虚拟机"""
        if common.SCROLL_TYPE == "slider":
            if event.delta() < 0 and self.currentIndex > 0:
                self.currentIndex -= 1
                self.updateVMListSlider()
            elif event.delta() > 0 and self.currentIndex < self.maxValue:
                self.currentIndex += 1
                self.updateVMListSlider()
   
            self.slider.wheelEvent(event)
        else:
            maxValue = self.scrollArea.verticalScrollBar().maximum()
            minValue = self.scrollArea.verticalScrollBar().minimum()
            currentValue = self.scrollArea.verticalScrollBar().value()
            if event.delta() < 0 and currentValue < maxValue:
                self.scrollArea.wheelEvent(event)
            elif event.delta() > 0 and currentValue > minValue:
                self.scrollArea.wheelEvent(event)
        
    #slider     
    def updateVMListSlider(self):
        """更新虚拟机列表"""
        for i in range(len(self.vmButtonList)):
            self.vmButtonList[i].hide()
 
        vmsInfoList = VMInfoManager.instance().getVMSInfo()
        if vmsInfoList:
            self.slider.show()
            startIndex = (self.maxValue - self.currentIndex) * 3
             
            if startIndex/3 == (self.maxValue):
                endIndex = len(vmsInfoList)
            else:
                endIndex = startIndex + 3
                 
            for i in range(startIndex, endIndex):
                self.vmButtonList[i - startIndex].setText(vmsInfoList[i])
                self.vmButtonList[i - startIndex].show()  
        else:
            self.slider.hide()
         
            
            
    """      echo <graphics type='sdl display='$DISPLAY' xauth='$XAUTHORITY'/>
    <graphics type='sdl display=':0.0' xauth='/home/cole/.Xauthority'/>  """
            
            
