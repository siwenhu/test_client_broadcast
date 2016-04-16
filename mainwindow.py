# -*- coding: utf-8 -*-  

from PyQt4.QtGui  import QWidget, QApplication
from PyQt4.QtCore import QSize, SIGNAL, QPoint, QTimer, QTranslator,\
    QCoreApplication, QTime, QEventLoop, QProcess
import os
import time
#import json

#from loadingwidget import LoadingWidget
#from offvm.offvmwidget import VMWidget
from menubar import MenuBar
#from linkserverthread import LinkServerThread
#from vminfomanager import VMInfoManager
from waitingbroadcast import WaitingBroadCast
#from tcpserversocket import CloudsTcpServer
#from windowMonitor import WindowMonitor
#from vmoperation import VMOperation
#from updateStateThread import UpdateThread
#from offvm.localimgmanager import LocalImgManager
import common
import globalvariable
import globalfunc
#from logrecord import LogRecord
from storeinfoparser import StoreInfoParser
from base.infohintdialog import InfoHintDialog
from setting.restartnetworkthread import RestartNetworkThread
import threading

language = 'english'
class MainWindow(QWidget):
       
    def __init__(self,parent = None):
        super(MainWindow,self).__init__(parent)      
        
        self.TYPE_VM = "offline"
        #链接状态
        self.currentLinkState = False
        self.vmListLength = 99
        self.buttonState = True
        self.startLessonFlag = False
        
        self.alllessonstart = False
        
        self.initSubWidget()
        
        #绑定相应的信号和槽函数
        self.bandSignalSlot()

        #self.localMac = globalfunc.get_mac_address()

        #self.waitingTimer = QTimer()
        #self.waitingTimer.start(5000)
        #self.connect(self.waitingTimer, SIGNAL("timeout()"), self.auto_spice)
        #self.flag = True


    def initSubWidget(self):
        # 右上角关闭等最小化按钮
        self.menuBar = MenuBar(self)
        #self.menuBar.hide()
        self.menuBar.show()

        #开启监听，接受云主机发送的信息
        
        #USB
        

        #监视是否有关闭的window进程

        #重启网络信息提示窗口
        self.waitingDlg = InfoHintDialog(None)

        #重启网络线程
        #虚拟机打开可控线程
        

        # 加载窗口

        
        #广播监听
        self.broadcast = WaitingBroadCast()
        
    
    def auto_spice(self):
        serverIp = "192.168.0.29"
        #serverIp = "192.168.1.32"
        argcList = ["smep://%s/?port=%s" % (serverIp, "5901")] 
        if self.flag:
            print "argcList:%s"  % argcList
            self.flag = False
            os.system("killall window")
            QProcess.startDetached("/opt/ccr-student/window/window", argcList)

    def tryRebindPort(self):
        self.broadcast.bindUdpPort()
        #self.tcpServer.bindTcpPort()

    def bandSignalSlot(self):
        
        #点击设置，工具或关于按钮时发送的信号
        self.connect(self.menuBar, SIGNAL("showToolDialog"),self.slotShowToolDialog)
        
        #接收到广播发送的消息，执行相应的操作
        self.connect(self.broadcast, SIGNAL("operaterCmd"),self.slotOperateBroadcastCMD)
        
        
    def slotDownloadError(self,vmname):
        
        self.initLocalVm()
    
    def initLocalVm(self):
        self.TYPE_VM = StoreInfoParser.instance().getVmType()
        if self.TYPE_VM == "offline":# or self.TYPE_VM == None or self.TYPE_VM == "" or self.TYPE_VM == False:
            lessonlist = StoreInfoParser.instance().getLessonList()
            offlessonlist = StoreInfoParser.instance().getOffLessonList()
            if lessonlist == None or offlessonlist == None:
                LogRecord.instance().logger.info(u"local list is none")
                return
            localofflist = []
            locallessonlist = json.loads(lessonlist)
            offlocallessonlist = json.loads(offlessonlist)
            localImgList = LocalImgManager.instance().getCompleteList()
            for item in offlocallessonlist:
                if item["name"] in localImgList:
                    localofflist.append(item)
                    
            StoreInfoParser.instance().setLessonList(json.dumps(localofflist))
            StoreInfoParser.instance().setLessonList(json.dumps(localofflist))
            
            if len(localofflist) == 0:
                LogRecord.instance().logger.info(u"local list is none")
                self.vmWidget.setVMInfoList(localofflist,localofflist)
                self.vmWidget.hide()
                self.loadingWiget.show()
                #self.slotChangeLinkThreadStatus("disconnect")
                self.setPosition()
                self.loadingWiget.setHintInfo("failed", 0)
                if not self.linkThread.isStartLink and self.buttonState:
                    self.loadingWiget.restartLink()
                return
            else:
                
                LogRecord.instance().logger.info(u"local list is not none")
                self.loadingWiget.hide()
                self.vmWidget.setVMInfoList(localofflist,localofflist)
                self.vmWidget.showVmList()
                self.vmWidget.show()
                self.setPosition()
                self.menuBar.show()
                self.menuBar.raise_()
        
    def postVmStateInfo(self, postInfo):
        self.updateThread.setVmInfoState(postInfo)
        
    def hideMenuBar(self):
        self.menuBar.hide()
    
    def updateWindow(self,language):
        
        self.menuBar.updateWindow()
        self.loadingWiget.updateWindow()
        
        
    def slotShowRestartNetworkInfo(self, status):
        """显示重启网络的状态信息"""
        
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
        
        if status == "Start":
            #InfoHintDialog(self.tr("restarting network, please wait ...")).exec_()
            self.waitingDlg.setHintInfo(self.tr("restarting network, please wait ..."))
        elif status == "Success":
            #InfoHintDialog(self.tr("network setting success")).exec_()
            self.waitingDlg.setHintInfo(self.tr("network setting success"))
        elif status == "Failed":
            #InfoHintDialog(self.tr("network restart failed")).exec_()
            self.waitingDlg.setHintInfo(self.tr("network restart failed"))
        else:
            return
        
        if self.waitingDlg.isHidden():
            desktop = QApplication.desktop()
            self.waitingDlg.move((desktop.width() - self.waitingDlg.width())/2, (desktop.height() - self.waitingDlg.height())/2)
            self.waitingDlg.exec_()
        
    def slotOperateTcpServerCMD(self, command, value):
        
        if command == "TERMINAL_NAME":
                #修改计算机名称到系统配置文件
                StoreInfoParser.instance().setTerminalName(value)
                globalvariable.TERMINAL_NAME = value
                
                self.emit(SIGNAL("terminalchange"))
                
        elif command == "TERMINAL_NETWORK_CONFIG":
                self.operateBroadcastConfigNetwork(value)
                
        if self.TYPE_VM == "online":
            if command == "TICHU":
                #踢出当前的学生机
                globalvariable.TICHU_STATUS = True
                vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
                self.vmWidget.setVMInfoList(vmLessonInfo,[])
                self.vmWidget.updateVMList()
                WindowMonitor.instance().start(2000)
            else:
                LogRecord.instance().logger.info("receive a command which is not understand")
        elif self.TYPE_VM == "offline":
            if command == "shutdown":
                self.vmWidget.domainManager.shutdownDomain()
            elif command == "poweroff":
                self.vmWidget.domainManager.poweroffDomain()
            elif command == "reset":
                self.vmWidget.domainManager.restartDomain()
            elif command == "TICHU":
                self.vmWidget.domainManager.poweroffDomain()
            else:
                LogRecord.instance().logger.info(self.tr("receive a command which is not understand"))

    def operateBroadcastConfigNetwork(self, value):
        LogRecord.instance().logger.info(self.tr("receive a command changing network"))
        self.emit(SIGNAL("update"))
        self.waitingDlg = InfoHintDialog(None)
        if not globalvariable.CLASS_STATUS:
            networkType = value[0]
            if networkType == "static":
                if len(value) >= 5:
                    IPADDR = value[1].strip()
                    NETMASK = value[2].strip()

                    if len(IPADDR) == 0 or len(NETMASK) == 0:
                        InfoHintDialog(self.tr("command is wrong")).exec_()
                        return

                    netconf = globalfunc.setJyStaticNetwork(value)
                    if netconf != "False":
                        #重新启动网络
                        self.restartNetworkTD.setNetConf(netconf)
                        self.restartNetworkTD.start()
                    else:
                        LogRecord.instance().logger.info(u"修改网络配置文件为静态网络失败")
                else:
                    LogRecord.instance().logger.info(u"云主机发送过来的静态网络数据格式有误")
            elif networkType == "dhcp":
                netconf = globalfunc.setJyDynamicNetwork()
                #重新启动网络
                if netconf:
                    self.restartNetworkTD.setNetConf(netconf)
                    self.restartNetworkTD.start()
                else:
                    InfoHintDialog(self.tr('设置自动获取IP失败')).exec_()

    def operateBroadcastStartLesson(self, command):
        """执行上课指令"""
        LogRecord.instance().logger.info(u"接收上课指令")
        globalvariable.CLASS_STATUS = True
        value = globalfunc.getVMCloudsNameFromBroadInfo(command)
        if value:
            globalvariable.CLASS_STATUS_VM_NAME = value
            #关闭所有的window
            if not self.vmWidget.isHidden():
                VMOperation.instance().autoCloseVMLesson()
                WindowMonitor.instance().clearProcessMap()
                WindowMonitor.instance().stop()
                self.startLessonFlag = True
                vmInfo = self.updateThread.getVmInfo()
                vmName = globalvariable.CLASS_STATUS_VM_NAME                         
                vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
                coursename = self.updateThread.getCourseName()
                currentvm = None
                if (not vmInfo) or (not coursename):
                    return
                for item in vmLessonInfo:
                    if item["name"] == coursename:
                        currentvm = item
                        break
                if currentvm !=None:
                    tmp = vmInfo[0]["name"]
                    vmInfo[0]["name"] = coursename
                    vmInfo[0]["vmname"] = vmName
                    vmInfo[0]["os_distro"] = currentvm["os_distro"] 
                    self.vmWidget.setVMInfoList(vmInfo,[])
                else:
                    self.vmWidget.setVMInfoList(vmLessonInfo,[])
                
                self.vmWidget.updateVMList()
                self.vmWidget.show()
                self.setPosition()
                self.menuBar.show()
                self.menuBar.raise_()
                self.ownSleep(1000)
                
                self.openvmThread = threading.Thread(target=self.vmWidget.autoOpenVMLesson,args=(value,))
                self.openvmThread.start()

            elif self.vmWidget.isHidden() and not self.linkThread.isStartLink:
                self.alllessonstart = True
                self.loadingWiget.restartLink()
        else:
            self.vmWidget.hide()
            self.loadingWiget.show()
            self.setPosition()
            LogRecord.instance().logger.info(u"未查询到分配给当前学生机的虚拟机名称")
            self.loadingWiget.setHintInfo("terminalVMIsNone", None)
            time.sleep(5)

    def operateBroadcastStopLesson(self):
        """执行下课指令"""
        LogRecord.instance().logger.info(u"执行下课指令")

        globalvariable.TICHU_STATUS = False
        globalvariable.CLASS_STATUS = False
        globalvariable.CLASS_STATUS_VM_NAME = None
        self.startLessonFlag = False
        WindowMonitor.instance().start(2000)
        
        #关闭所有的window程序
        windowList = WindowMonitor.instance().getCurrentProcessId()
        for ID in windowList:
            os.system("kill -9 %s" % ID)
            
        if self.vmWidget.isHidden() and not self.linkThread.isStartLink:
            self.loadingWiget.restartLink()
        else:
            vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
            self.vmWidget.setVMInfoList(vmLessonInfo,[])
            self.vmWidget.updateVMList()
        
            
    def operateBroadcastRecordUSBStatus(self, command):
        """记录USB的使用状态"""
        if len(command.split(":")) > 1:
            stateValue = command.split(":")[1]
            StoreInfoParser.instance().setUsbState(stateValue)
        else:
            LogRecord.instance().logger.info(u"云主机发送的更改USB数据有误")
            
    def operateBroadcastRecordNetStatus(self, command):
        """Net状态"""
        if len(command.split(":")) > 1:
            stateValue = command.split(":")[1]
            StoreInfoParser.instance().setNetState(stateValue)
            self.vmWidget.domainManager.defineNetFilter(stateValue)
        else:
            LogRecord.instance().logger.info(u"云主机发送的更改Net数据有误")

    def operateBroadcastShutdownByIP(self, command):
        """根据IP执行关机指令"""
        LogRecord.instance().logger.info("operateBroadcastShutdownByIP in")
        if len(command.split(":")) > 1:
            receiveIp = command.split(":")[1]
            serverIp = StoreInfoParser.instance().getCloudsServerIP()
            if receiveIp == serverIp:
                LogRecord.instance().logger.info(u"执行关机指令")
                globalfunc.shutdownTerminal()
            else:
                LogRecord.instance().logger.info(u"接受的云主机地址与当前的不一致")

    def operateBroadcastShutdownByMac(self, command):
        """根据MAC执行关机指令"""
        LogRecord.instance().logger.info(u"执行关机指令")
        LogRecord.instance().logger.info(self.localMac)
        if len(command.split("|")) > 1:
            MAC = command.split("|")[1]
            if MAC == self.localMac:
                globalfunc.shutdownTerminal()
        else:
            LogRecord.instance().logger.info(u"云主机发送的关机命令数据有误")

    def operateBroadcastResolutionModify(self, command):
        """修改学生端的分辨率"""
        if globalvariable.CLASS_STATUS:
            return
        if len(command.split(":")) >= 2:
            new_value = command.split(":")[1]
            globalfunc.setScreenResolution(new_value)
        else:
            LogRecord.instance().logger.info(u"分辨率值格式有误")

    def operateBroadcastRecordCloudServerIP(self, command):
        """记录云主机的IP值"""
        if len(command.split(" ")) >= 5:
            try:
                startIp = command.split(" ")[1].split(":")[1]
                endIp = command.split(" ")[2].split(":")[1]
                mainServerIP = command.split(" ")[3].split(":")[1]
                backupServerIP = command.split(" ")[4].split(":")[1]

                startIndex = int(startIp.split(".")[-1])
                endIndex = int(endIp.split(".")[-1])
                currentIndex = int(globalfunc.get_ip_address().split(".")[-1])

                if currentIndex >= startIndex and currentIndex <= endIndex:
                    LogRecord.instance().logger.info(u"记录云主机的IP地址：%s" % mainServerIP)
                    StoreInfoParser.instance().setServerAddress(mainServerIP)
                    StoreInfoParser.instance().setBackUpServerAddress(backupServerIP)
                    
            except Exception, e:
                LogRecord.instance().logger.info(u"解析接收的云主机IP数据格式有误：%s" % e.message)
        else:
            LogRecord.instance().logger.info(u"接收的云主机IP数据格式有误：%s" % command)

    def slotOperateBroadcastCMD(self, command):
        LogRecord.instance().logger.info(u"执行广播指令")
        
        
        if command.split(" ")[0] == "CLOUDS_SERVER_IP": #记录云主机的IP值
            self.operateBroadcastRecordCloudServerIP(command)
            
        
        if self.TYPE_VM == "online":
            if command.startswith("START_LESSON"): #执行上课指令
                self.operateBroadcastStartLesson(command)
    
            elif command == "STOP_LESSON": #执行下课指令
                self.operateBroadcastStopLesson()
    
            elif command.startswith("USBSTATE"): #记录USB的使用状态
                self.operateBroadcastRecordUSBStatus(command)
    
            elif command.startswith("shutdownVM"): #根据IP执行关机指令
                self.operateBroadcastShutdownByIP(command)
    
            elif command.startswith("SHUT_DOWN"): #根据MAC执行关机指令
                self.operateBroadcastShutdownByMac(command)
    
            elif command == "TERMINAL_STATE": #向云主机注册学生机信息
                LogRecord.instance().logger.info(u"向云主机注册学生机信息")
    
            elif command.startswith("RESOLUTION_MODIFY"): #修改学生端的分辨率
                self.operateBroadcastResolutionModify(command)
    
            elif command.split(" ")[0] == "CLOUDS_SERVER_IP": #记录云主机的IP值
                self.operateBroadcastRecordCloudServerIP(command)
        if self.TYPE_VM == "offline":
            if command.startswith("START_LESSON"): #执行上课指令
                LogRecord.instance().logger.info(u"接收上课指令")
                globalvariable.CLASS_STATUS = True
                value = globalfunc.getVMCloudsNameFromBroadInfo(command)
                if value:
                    globalvariable.CLASS_STATUS_VM_NAME = value
                    coursename = globalvariable.RUNNING_COURSE
                    self.vmWidget.autoOpenCourse(coursename)
                    if self.vmWidget.isHidden() and not self.linkThread.isStartLink:
                        self.loadingWiget.restartLink()
                else:
                    self.vmWidget.hide()
                    self.loadingWiget.show()
                    self.setPosition()
                    LogRecord.instance().logger.info(u"未查询到分配给当前学生机的虚拟机名称")
                    self.loadingWiget.setHintInfo("terminalVMIsNone", None)
                    time.sleep(5)
                    
            elif command.startswith("AUTOSTART_LESSON"): #执行上课指令
                LogRecord.instance().logger.info(u"接收上课指令")
                globalvariable.CLASS_STATUS = True
                classid = globalfunc.getInfoVMCloudsNameFromBroad(command)
                if classid:
                    coursename = globalvariable.RUNNING_COURSE
                    self.vmWidget.autoOpenCourse(coursename,classid)
                    if self.vmWidget.isHidden() and not self.linkThread.isStartLink:
                        self.loadingWiget.restartLink()
                else:
                    self.vmWidget.hide()
                    self.loadingWiget.show()
                    self.setPosition()
                    LogRecord.instance().logger.info(u"未查询到分配给当前学生机的虚拟机名称")
                    self.loadingWiget.setHintInfo("terminalVMIsNone", None)
                    time.sleep(5)
    
            elif command == "STOP_LESSON": #执行下课指令
                self.vmWidget.domainManager.poweroffDomain()
                LogRecord.instance().logger.info(u"执行下课指令")

                globalvariable.TICHU_STATUS = False
                globalvariable.CLASS_STATUS = False
                globalvariable.CLASS_STATUS_VM_NAME = None
                vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
                vmOffLessonInfo = VMInfoManager.instance().getOnlineLessonListInfo()
                self.vmWidget.setVMInfoList(vmLessonInfo,vmOffLessonInfo)
                self.vmWidget.showVmList()
                
    
            elif command.startswith("USBSTATE"): #记录USB的使用状态
                self.operateBroadcastRecordUSBStatus(command)
                
            elif command.startswith("NETSTATE"):
                self.operateBroadcastRecordNetStatus(command)
    
            elif command.startswith("shutdownVM"): #根据IP执行关机指令
                self.operateBroadcastShutdownByIP(command)
                
            elif command.startswith("SHUT_DOWN"): #根据MAC执行关机指令
                self.operateBroadcastShutdownByMac(command)
    
            elif command == "TERMINAL_STATE": #向云主机注册学生机信息
                LogRecord.instance().logger.info(u"向云主机注册学生机信息")
    
            elif command.startswith("RESOLUTION_MODIFY"): #修改学生端的分辨率
                self.operateBroadcastResolutionModify(command)
    
            elif command.split(" ")[0] == "CLOUDS_SERVER_IP": #记录云主机的IP值
                self.operateBroadcastRecordCloudServerIP(command)

        
    def slotShowToolDialog(self, actionType):
        print "hello"
        self.emit(SIGNAL("showToolDialog"), actionType)
        
    def slotChangeLinkThreadButtonStatus(self, status):
       
        if status == "disconnect":
            self.buttonState = False
            self.linkThread.changeLinkStatus(False)
            self.loadingWiget.update()
            self.menuBar.show()
            self.menuBar.raise_()
        elif status == "restartLink":
            self.buttonState = True
            self.linkThread.changeLinkStatus(True)
            self.loadingWiget.update()
            self.menuBar.hide()

    def slotChangeLinkThreadStatus(self, status):
        """改变连接服务器线程的状态，关闭连接或重新连接"""
        if True:
            if status == "disconnect":
                self.linkThread.changeLinkStatus(False)
                self.loadingWiget.update()
                self.menuBar.show()
                self.menuBar.show()
            elif status == "restartLink":
                self.linkThread.changeLinkStatus(True)
                self.loadingWiget.update()
                self.menuBar.hide()
        
    def slotShowConnectFailed(self, failNum):
        """显示连接服务器失败的信息提示"""
        self.TYPE_VM = StoreInfoParser.instance().getVmType()
        #if self.TYPE_VM == "offline":
        self.emit(SIGNAL("connectfailed"))
        if self.TYPE_VM == "offline":
            self.initLocalVm()
            self.vmWidget.stopAllDownload()
            self.currentLinkState = False
        elif self.TYPE_VM == "online":
            os.system("killall window") 
            self.currentLinkState = False
            self.vmWidget.hide()
            self.loadingWiget.show()
            self.setPosition()
            self.loadingWiget.setHintInfo("failed", failNum)
            if self.vmWidget.isHidden() and not self.linkThread.isStartLink and self.buttonState:
                self.loadingWiget.restartLink()
        else:
            self.currentLinkState = False
            self.vmWidget.hide()
            self.loadingWiget.show()
            self.setPosition()
            self.loadingWiget.setHintInfo("failed", failNum)
            if  self.vmWidget.isHidden() and not self.linkThread.isStartLink and self.buttonState:
                self.loadingWiget.restartLink()
        
        
    def slotShowTryConnecting(self, failNum):
        """显示正在连接服务器的信息提示"""
        if self.TYPE_VM == "online":
            if failNum:
                self.loadingWiget.setHintInfo("connecting", failNum)
        elif self.TYPE_VM == "offline":
            pass
        else:
            if failNum:
                self.loadingWiget.setHintInfo("connecting", failNum)
        
    def paintEvent(self,paintEvent):
        """调整子控件的位置"""
        
        # 设置关闭等按钮位置
        self.menuBar.move(self.geometry().width()-self.menuBar.frameGeometry().width(),0)
        # 设置加载widget位置
    def setPosition(self):
        #width = globalfunc.getWidth()
        #height = globalfunc.getHeight()
        
        if not self.menuBar.isHidden():
            self.menuBar.move(self.geometry().width()-self.menuBar.frameGeometry().width(),0)
            self.menuBar.raise_()
            
        #self.menuBar
    #def wheelEvent(self,event):
    #    """鼠标滚轮滚动事件,事件传递给控件vmWidget"""
    #    if not self.vmWidget.isHidden():
    #        self.vmWidget.wheelEvent(event)
        
    def slotShowVMWidget(self):
        self.tryRebindPort()
        self.emit(SIGNAL("connectsuccess"))
        LogRecord.instance().logger.info(u"connect success")
        serverState = VMInfoManager.instance().getCurCloudServerState()
        LogRecord.instance().logger.info(u"get state of clouds server")
        self.TYPE_VM = self.updateThread.getVmType()
        LogRecord.instance().logger.info(u"get vmtype")
        if serverState != "enable":
            if self.TYPE_VM == "offline":
                if serverState != "disable":
                    self.initLocalVm()
                    return
            LogRecord.instance().logger.info(u"server is not available, return")
            self.loadingWiget.setHintInfo("cloudsServerStateDisable", None)
            return
        
        LogRecord.instance().logger.info(u"start get the license")
        license = self.updateThread.getLisence()
        if license == False:
            LogRecord.instance().logger.info(u"the license is not available, stop the refresh timer, show loading widget and return")
            self.timer.stop()
            self.menuBar.hide()
            if not self.loadingWiget.hide():
                self.loadingWiget.setHintInfo("noLicense", None)
                self.loadingWiget.show()
                self.setPosition()
            else:
                self.vmWidget.hide()
                self.loadingWiget.setHintInfo("noLicense", None)
                self.loadingWiget.show()
                self.setPosition()
            return
        LogRecord.instance().logger.info(u"the license is available")
        completeList = LocalImgManager.instance().getCompleteList()
        LogRecord.instance().logger.info(u"get the list of images but do not no the size")
        downloadingList = self.vmWidget.getDownloadingList()
        LogRecord.instance().logger.info(u"get the image of downloading")
        if len(completeList) >= self.vmListLength and len(downloadingList) == 0:
            LogRecord.instance().logger.info(u"if the downloading list is null, start the refresh timer")
            if self.timer.isActive():
                pass
            else:
                self.timer.start(10000)
                self.menuBar.show()
                self.menuBar.raise_()
        if self.currentLinkState and not self.vmWidget.isHidden():
            return
        self.TYPE_VM = self.updateThread.getVmType()
        LogRecord.instance().logger.info(u"get vmtype")
        self.currentLinkState = True
        if self.TYPE_VM == "online": 
            self.showOnVmWidget()
                
        if self.TYPE_VM == "offline":  
            self.showOffVmWidget()
                
    def showOnVmWidget(self):
        
        vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
        """ 得到上线的课程列表 """
        vmOffLessonInfo = VMInfoManager.instance().getOnlineLessonListInfo()
        curriculaNum = len(vmLessonInfo)
        #没有上线的课程库
        if curriculaNum == 0:
            self.loadingWiget.setHintInfo("curriculaIsNone", None)
            self.menuBar.raise_()
            return
        #存在上线的课程，没有分配到云桌面
        if curriculaNum > 0 and len(vmOffLessonInfo) == 0:
            self.setPosition()
            self.loadingWiget.setHintInfo("terminalVMIsNone", None)
            self.menuBar.raise_()
            #self.loadingWiget.restartLink()
            return
        elif curriculaNum > common.UPLIMIT:
            self.loadingWiget.setHintInfo("reachToplimit", None)
            self.menuBar.raise_()
            return
        else:
            self.loadingWiget.hide()
            if common.SCROLL_TYPE == "slider":
                self.vmWidget.setSliderMaxValue(curriculaNum)
            else:
                if self.vmWidget.isHidden() and not globalvariable.TICHU_STATUS:
                    vmInfo = self.updateThread.getVmInfo()#获取云桌面的信息
                    if globalvariable.CLASS_STATUS and (not vmInfo):
                        LogRecord.instance().logger.info(u"显示上课状态时的分配给学生的虚拟机信息")
                        if globalvariable.CLASS_STATUS_VM_NAME:
                            vmName = globalvariable.CLASS_STATUS_VM_NAME                         
                            vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
                            coursename = self.updateThread.getCourseName()
                            currentvm = None
                            for item in vmLessonInfo:
                                if item["name"] == coursename:
                                    currentvm = item
                                    break
                            if currentvm !=None:
                                tmp = vmInfo[0]["name"]
                                vmInfo[0]["name"] = coursename
                                vmInfo[0]["vmname"] = vmName
                                vmInfo[0]["os_distro"] = currentvm["os_distro"] 
                                self.vmWidget.setVMInfoList(vmInfo,[])
                            else:
                                self.vmWidget.setVMInfoList(vmLessonInfo,[])
                            
                            self.vmWidget.updateVMList()
                            self.vmWidget.show()
                            self.setPosition()
                            self.menuBar.show()
                            self.menuBar.raise_()
                            self.ownSleep(1000)
                            if WindowMonitor.instance().getCurrentWindowsProcess(globalvariable.CLASS_STATUS_VM_NAME) == False:
                                self.openvmThread = threading.Thread(target=self.vmWidget.autoOpenVMLesson, args=(globalvariable.CLASS_STATUS_VM_NAME, self.alllessonstart,))
                                self.openvmThread.start()
                                #self.vmWidget.autoOpenVMLesson(globalvariable.CLASS_STATUS_VM_NAME,self.alllessonstart)                               
                            self.alllessonstart = False
                        else:
                            LogRecord.instance().logger.info(u"未查询到分配给当前学生机的虚拟机名称")
                            self.loadingWiget.setHintInfo("terminalVMIsNone", None)
                            self.loadingWiget.show()
                            self.setPosition()
                            return
                    else:
                        LogRecord.instance().logger.info(u"显示下课状态时的课程列表信息")
                        globalvariable.CLASS_STATUS_VM_NAME = None
                        vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
                        self.vmWidget.setVMInfoList(vmLessonInfo,[])
                        
                    self.vmWidget.updateVMList()
            self.vmWidget.show()
            self.setPosition()
            self.menuBar.show()
            self.menuBar.raise_()
            
    def ownSleep(self,sec):
        dieTime = QTime.currentTime().addMSecs(sec)
        while(QTime.currentTime()<dieTime):
            QCoreApplication.processEvents(QEventLoop.AllEvents,100)
            
    def showOffVmWidget(self):
        LogRecord.instance().logger.info(u"terminal post and refresh the list off course list")
        vmOffLessonInfo = VMInfoManager.instance().getOnlineLessonListInfo()
        LogRecord.instance().logger.info(u"get the course list and the offline course list")
        vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
        if vmLessonInfo == None or vmLessonInfo == False or vmOffLessonInfo == None or vmOffLessonInfo == False:
            vmLessonInfo = []
            vmOffLessonInfo = []
        curriculaNum = len(vmLessonInfo)
        if curriculaNum == 0:
            self.loadingWiget.setHintInfo("curriculaIsNone", None)
        elif curriculaNum > common.UPLIMIT:
            self.loadingWiget.setHintInfo("reachToplimit", None)
        else:
            self.loadingWiget.hide()
            if common.SCROLL_TYPE == "slider":
                self.vmWidget.setSliderMaxValue(curriculaNum)
            else:
                if not globalvariable.TICHU_STATUS:
                    if globalvariable.CLASS_STATUS:
                        LogRecord.instance().logger.info(u"显示上课状态时的分配给学生的虚拟机信息")
                        if globalvariable.CLASS_STATUS_VM_NAME:#vmname
                            coursename = self.updateThread.getCourseName()
                            vmOffLessonInfo = VMInfoManager.instance().getOnlineLessonListInfo()
                            vmOnLessonInfo = []
                            for item in vmOffLessonInfo:
                                if coursename == item["name"]:
                                    vmOnLessonInfo = [item]
                            self.vmListLength = 1
                            self.vmWidget.setVMInfoList(vmOnLessonInfo,vmOffLessonInfo)
                            self.vmWidget.autoOpenOffVMLesson()
                        else:
                            LogRecord.instance().logger.info(u"未查询到分配给当前学生机的虚拟机名称")
                            self.loadingWiget.setHintInfo("terminalVMIsNone", None)
                            self.loadingWiget.show()
                            self.vmWidget.hide()
                            self.setPosition()
                            return
                    else:
                        LogRecord.instance().logger.info(u"显示下课状态时的课程列表信息")
                        globalvariable.CLASS_STATUS_VM_NAME = None
                        vmOnLessonInfo = VMInfoManager.instance().getLessonListInfo()
                        vmOffLessonInfo = VMInfoManager.instance().getOnlineLessonListInfo()
                        self.vmListLength = len(vmOffLessonInfo)
                        if len(vmOnLessonInfo) > 0 and len(vmOffLessonInfo) == 0:
                            self.vmWidget.setVMInfoList([], [])
                            self.vmWidget.hide()
                            self.loadingWiget.show()
                            self.vmWidget.hide()
                            self.setPosition()
                            self.loadingWiget.setHintInfo("terminalVMIsNone", None)
                            return
                        if len(vmOnLessonInfo)==0:
                            self.vmWidget.setVMInfoList([], [])
                            self.vmWidget.hide()
                            self.loadingWiget.show()
                            self.vmWidget.hide()
                            self.setPosition()
                            self.loadingWiget.setHintInfo("curriculaIsNone", None)
                            return
                        self.vmWidget.setVMInfoList(vmOnLessonInfo,vmOffLessonInfo)
                    self.vmWidget.showVmList()
            self.vmWidget.show()
            self.setPosition()
            self.menuBar.show()
            self.menuBar.raise_()
            imgMap = LocalImgManager.instance().getCompliteListSize()
            for lesson in vmOnLessonInfo:
                if (lesson.get('name') in imgMap.keys()) and (lesson.get('img_file_size') == imgMap.get(lesson.get('name'))):
                    pass
                else:
                    self.dtimers.start(3000)
                    break
    def startDownload(self):
        self.timer.stop()
        self.menuBar.hide()
        self.dtimers.stop()
        self.vmWidget.autoStartDownload()
        
    def refreshOnWidget(self):
        if not self.timer.isActive():
            self.timer.start(10000)
            self.menuBar.show()
            self.menuBar.raise_()
        if not self.vmWidget.isHidden() and self.loadingWiget.isHidden():
            if common.SCROLL_TYPE == "slider":
                vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
                curriculaNum = len(vmLessonInfo)
                self.vmWidget.setSliderMaxValue(curriculaNum)
            else:         
                if globalvariable.CLASS_STATUS and not globalvariable.TICHU_STATUS:
                    LogRecord.instance().logger.info(u"开始获取上课状态下的学生的虚拟机信息")
                    vmName = globalvariable.CLASS_STATUS_VM_NAME

                    vmInfo = self.updateThread.getVmInfo()#获取云桌面的信息
                    if not vmInfo:
                        LogRecord.instance().logger.info(u"没有获取到上课课程的信息！！")
                        return
                    
                    vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
                    coursename = self.updateThread.getCourseName()
                    if not coursename:
                        LogRecord.instance().logger.info(u"没有获取到上课课程的信息！！")
                        return
                    
                    currentvm = None
                    for item in vmLessonInfo:
                        if item["name"] == coursename:
                            currentvm = item
                            break
                    if currentvm !=None:
                        tmp = vmInfo[0]["name"]
                        vmInfo[0]["name"] = currentvm["name"]
                        vmInfo[0]["vmname"] = vmName
                        vmInfo[0]["os_distro"] = currentvm["os_distro"] 
                        self.vmWidget.setVMInfoList(vmInfo,[])
                    else:
                        self.vmWidget.setVMInfoList(vmLessonInfo,[])
                    self.vmWidget.show()
                    self.vmWidget.updateVMList()
                    self.setPosition()
                    
                    if WindowMonitor.instance().getCurrentWindowsProcess(globalvariable.CLASS_STATUS_VM_NAME) == False:
                        if self.openvmThread == None or not self.openvmThread.isAlive():
                            self.openvmThread = threading.Thread(target=self.vmWidget.autoOpenVMLesson, args=(globalvariable.CLASS_STATUS_VM_NAME,))
                            self.openvmThread.start()
                            #self.vmWidget.autoOpenVMLesson(globalvariable.CLASS_STATUS_VM_NAME)
                else:
                    LogRecord.instance().logger.info(u"开始获取课程列表的信息")
                    
                    vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
                    vmOffLessonInfo = VMInfoManager.instance().getOnlineLessonListInfo()
                    curriculaNum = len(vmLessonInfo)
                    if curriculaNum == 0:
                        self.vmWidget.hide()
                        self.loadingWiget.show()
                        self.setPosition()
                        self.loadingWiget.setHintInfo("curriculaIsNone", None)
                        return
                    if curriculaNum > 0 and len(vmOffLessonInfo) == 0:
                        self.vmWidget.hide()
                        self.loadingWiget.show()
                        self.setPosition()
                        self.loadingWiget.setHintInfo("terminalVMIsNone", None)
                        return
                        
                    self.vmWidget.setVMInfoList(vmLessonInfo,[])
                        
                LogRecord.instance().logger.info(u"刷新界面信息")
                self.vmWidget.updateVMList()
                
            self.vmWidget.show()
            self.setPosition()
        
    def slotRefreshVMList(self):
        """刷新虚拟机列表"""
        LogRecord.instance().logger.info(u"start refresh the list")
        serverState = VMInfoManager.instance().getCurCloudServerState()
        if serverState != "enable":
            return
        self.TYPE_VM = self.updateThread.getVmType()
        if self.TYPE_VM == "online":
            self.refreshOnWidget()
        if self.TYPE_VM == "offline":  
            self.refreshOffWidget()
            
    def refreshOffWidget(self):
        if not self.vmWidget.isHidden() and self.loadingWiget.isHidden():
            if common.SCROLL_TYPE == "slider":
                vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
                curriculaNum = len(vmLessonInfo)
                self.vmWidget.setSliderMaxValue(curriculaNum)
                
            else:                    
                if globalvariable.CLASS_STATUS and not globalvariable.TICHU_STATUS:
                    coursename = self.updateThread.getCourseName()
                    vmOffLessonInfo = VMInfoManager.instance().getOnlineLessonListInfo()
                    if len(vmOffLessonInfo) == 0:
                        self.vmWidget.setVMInfoList([], [])
                        self.vmWidget.hide()
                        self.loadingWiget.show()
                        self.setPosition()
                        self.loadingWiget.setHintInfo("terminalVMIsNone", None)
                        return
                    vmInfoList = []
                    for item in vmOffLessonInfo:
                            if coursename == item["name"]:
                                vmInfoList = [item]
                                
                    if len(vmInfoList) == 0:
                        self.vmWidget.setVMInfoList([], [])
                        self.vmWidget.hide()
                        self.loadingWiget.show()
                        self.setPosition()
                        self.loadingWiget.setHintInfo("curriculaIsNone", None)
                        return
                    self.vmListLength = 1
                    self.vmWidget.setVMInfoList(vmInfoList,vmOffLessonInfo)
                    
                    if len(vmOffLessonInfo) >= 1:
                        self.loadingWiget.hide()
                        
                else:
                    LogRecord.instance().logger.info(u"开始获取课程列表的信息")
                    vmOffLessonInfo = VMInfoManager.instance().getOnlineLessonListInfo()
                    vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
                    if len(vmLessonInfo) > 0 and len(vmOffLessonInfo) == 0:
                        self.vmWidget.setVMInfoList([], [])
                        self.vmWidget.hide()
                        self.loadingWiget.show()
                        self.setPosition()
                        self.loadingWiget.setHintInfo("terminalVMIsNone", None)
                        return
                    if len(vmLessonInfo) == 0:
                        self.vmWidget.setVMInfoList([], [])
                        self.vmWidget.hide()
                        self.loadingWiget.show()
                        self.setPosition()
                        self.loadingWiget.setHintInfo("curriculaIsNone", None)
                        return
                    
                    self.vmListLength = len(vmLessonInfo)    
                    self.vmWidget.setVMInfoList(vmLessonInfo,vmOffLessonInfo)
                        
                LogRecord.instance().logger.info(u"刷新界面信息")
                
                self.vmWidget.showVmList()
                
            self.vmWidget.show() 
            self.setPosition()
            self.adtimers.start(3000)
            #self.vmWidget.autoStartDownload()
        elif self.vmWidget.isHidden() and not self.loadingWiget.isHidden():
            if True:
                if True:
                    LogRecord.instance().logger.info(u"开始获取课程列表的信息")
                    vmOffLessonInfo = VMInfoManager.instance().getOnlineLessonListInfo()
                    vmLessonInfo = VMInfoManager.instance().getLessonListInfo()
                    if vmOffLessonInfo == None or vmOffLessonInfo == False:
                        return
                    curriculaNum = len(vmLessonInfo)
                    self.vmListLength = len(vmLessonInfo)    
                    if curriculaNum == 0:
                        #self.vmWidget.hide()
                        self.loadingWiget.show()
                        self.setPosition()
                        self.loadingWiget.setHintInfo("curriculaIsNone", None)
                        return
                    if curriculaNum > 0 and len(vmOffLessonInfo) == 0:
                        #self.vmWidget.hide()
                        self.loadingWiget.show()
                        self.setPosition()
                        self.loadingWiget.setHintInfo("terminalVMIsNone", None)
                        return
                    self.vmWidget.setVMInfoList(vmLessonInfo,vmOffLessonInfo)
                    self.loadingWiget.setHintInfo("restart", None)
                    self.loadingWiget.hide()
                    
                LogRecord.instance().logger.info("refresh window information")
                
                self.vmWidget.showVmList()
                
            self.vmWidget.show() 
            self.setPosition()
            if self.menuBar.isHidden():
                self.menuBar.show()
                self.menuBar.raise_()
            self.adtimers.start(3000)
            #self.vmWidget.autoStartDownload()
    def checkAddDownload(self):
        
        self.timer.stop()
        self.adtimers.stop()
        self.vmWidget.checkAddDownload()
        
    def checkWindowId(self):
        processID = WindowMonitor.instance().checkDisapearWindowId()
        if processID != None and not globalvariable.CLASS_STATUS:
            globalvariable.VM_IS_CREATE_STATUS = False
            vmName = WindowMonitor.instance().getMapVmID(processID)
            WindowMonitor.instance().deleteProcessId(processID)
            if VMOperation.instance().removeVMLesson(vmName):
                LogRecord.instance().logger.info(u"删除后台相应的虚拟机成功")
                self.slotRefreshVMList()
            else:
                LogRecord.instance().logger.info(u"删除后台相应的虚拟机失败")
                
        elif processID != None and globalvariable.CLASS_STATUS and globalvariable.TICHU_STATUS:
            globalvariable.VM_IS_CREATE_STATUS = False
            vmName = WindowMonitor.instance().getMapVmID(processID)
            WindowMonitor.instance().deleteProcessId(processID)
            if VMOperation.instance().removeVMLesson(vmName):
                LogRecord.instance().logger.info(u"删除后台相应的虚拟机成功")
                self.slotRefreshVMList()
            else:
                LogRecord.instance().logger.info(u"删除后台相应的虚拟机失败")
            
            
        
        
        
