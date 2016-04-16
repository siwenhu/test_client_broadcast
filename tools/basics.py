# -*- coding: utf-8 -*-  

from PyQt4.QtGui import QFont, QApplication
from PyQt4.QtGui import QWidget,QApplication
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPushButton,QDialog, QKeyEvent
from PyQt4.QtCore import QPoint,QSize, QTranslator, QCoreApplication
from PyQt4.QtCore import Qt,SIGNAL,QString,QProcess,QEvent
from PyQt4.QtGui import QComboBox,QLineEdit,QTextBrowser,QIcon,QTextCursor
# from tab import TabWidget
# from tipDialog import TipDialog
from mythread import MyThread
from base.infohintdialog import InfoHintDialog
from base.tabwidget import TabWidget
import commands
import sys
import globalfunc
from storeinfoparser import StoreInfoParser

#本类创建一个NetWidget，将作为一个组件添加到tab中
class NetWidget(QWidget):
       
    def __init__(self,parent = None):
        super(NetWidget,self).__init__(parent)
        self.setStyleSheet("font-size : 16px")#设置整体的字体大小
        
        
        self.auto = False
        self.pro = QProcess(self)
#         self.tipDlg = TipDialog()
#         self.tipDlg.setModal(True)#引入tipdlg，并且将这个窗口设置为最前端窗口，且后面窗口无法操作
        
            #初始化comBox控件，并且为其添加选项
        self.comBox = QComboBox()
        self.comBox.setFixedWidth(120)
        self.comBox.insertItem(0, self.tr("ping"))
        self.comBox.insertItem(1, self.tr("ifconfig"))
        self.comBox.insertItem(2, self.tr("display"))
        #self.comBox.insertItem(3, self.tr("traceroute"))
        self.comBox.insertItem(4, self.tr("top"))
        self.connect(self.comBox, SIGNAL('activated(QString)'),self.onActivated)#设置combBox为活动的，与函数关联
        """
        #初始话控件设置
        #lineEdit，固定长度
        #runButton，显示字符串，信号量
        #pingLabel，当前显示字符
        #textBrower
          """ 
        self.lineEdit = QLineEdit()
        self.lineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        self.lineEdit.setFixedWidth(250)
        self.runButton = QPushButton(self.tr("Run"))
        self.runButton.setStyleSheet("background: rgb(7,87,198); color: white; width: 70px; height: 20px;font-size : 16px;")
        self.connect(self.runButton, SIGNAL("clicked()"),self.runButton_clicked)
        self.pingLabel = QLabel()#初始话，之后在函数操作中会改变
        self.pingLabel.setText(self.tr("Tip:please input the IP address of pinging,then get the result with clicking the button"))
        self.textBrowser = QTextBrowser()
        """
            #布局一上，横向布局
            #将comBox，lineEdit，runButton添加到布局中
            #设置前面空为20和后面空为280
            """
        hLayout1 = QHBoxLayout()
        hLayout1.addSpacing(20)
        hLayout1.addWidget(self.comBox)
        hLayout1.addWidget(self.lineEdit)
        hLayout1.addWidget(self.runButton)
        #hLayout1.addStretch()
        hLayout1.addSpacing(280)
        
            #布局二中，横向布局
            #将pingLabel添加到布局中，并且诶设置前面的空白为20
        hLayout2 = QHBoxLayout()
        hLayout2.addSpacing(20)
        hLayout2.addWidget(self.pingLabel)
        
            #布局三下
            #将textBrower添加爱到布局中，并且设置前面空白为20，后面空白为60，控件的大小自适应
        hLayout3 = QHBoxLayout()
        hLayout3.addSpacing(20)
        hLayout3.addWidget(self.textBrowser)
        hLayout3.addSpacing(60)
        
            #主题布局总，纵向布局
            #将之上的三个布局添加到总布局中，并且设置布局间空间为20，最下面的空白为40
        mainLayout = QVBoxLayout()
        mainLayout.addSpacing(20)
        mainLayout.addLayout(hLayout1)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(hLayout2)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(hLayout3)
        mainLayout.addSpacing(40)
        self.setLayout(mainLayout)
        
        
        self.thread = MyThread()
        self.connect(self.thread,SIGNAL("getoutput"),self.append)
        
        
    def append(self,actionType):
        self.textBrowser.clear()
        self.textBrowser.append(actionType)
        #cursor = QTextCursor()
        #self.runButton.setText(self.tr("Stop"))
        
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.textBrowser.setTextCursor(cursor)
        #changeLabel = QLabel()
    
    def onActivated(self):
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
            
        """#comBox的相应函数，随着comBox中字符串的改变，分别控制pingLabel的显示，以及lineEdit和textBrower的显示清除和可用状态
            #如果comBox当前的字符串文字为ping
            #pingLabel的文字设置为"提示：请在文本框中输入要ping的目标地址，然后点击执行获取结果"，保持当前大小
            #lineEdit中内容清除，设置为不可用
            #textBrower清空"""
        if(self.comBox.currentText() == "Ping" or self.comBox.currentText() == "ping"):
            self.pingLabel.setText(self.tr("Tip:please input the IP address of pinging,then get the result with clicking the button"))
            self.pingLabel.adjustSize()
            self.lineEdit.clear()
            self.lineEdit.setDisabled(False)
            self.textBrowser.clear()
            #如果comBox当前的字符串文字为ifconfig
            #类上所说
        elif(self.comBox.currentText() == "ifconfig"):
            self.pingLabel.setText(self.tr("Tip:get the net information"))
            self.pingLabel.adjustSize()
            self.lineEdit.clear()
            self.lineEdit.setEnabled(False)
            self.textBrowser.clear()
            #如果comBox当前的字符串文字为display
        elif(self.comBox.currentText() == "display"):
            self.pingLabel.setText(self.tr("Tip:get the resolution information"))
            self.pingLabel.adjustSize()
            self.lineEdit.clear()
            self.lineEdit.setEnabled(False)
            self.textBrowser.clear()
        
        elif(self.comBox.currentText() == "top"):
    
            self.pingLabel.setText(self.tr("Tip:run tom command"))
            self.pingLabel.adjustSize()
            self.lineEdit.setEnabled(False)
            self.lineEdit.clear()
            self.textBrowser.clear()
            #按钮的响应函数
    def runButton_clicked(self):
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
            
        #self.pro = QProcess(self)#外部程序使用声明
        desktop = QApplication.desktop()#获得桌面
        self.textBrowser.clear()#清除
        cmdstr = QString()
        center = QString()
        goal = QString()
        #comBox当前text为ping
        if (self.comBox.currentText() == "Ping" or self.comBox.currentText() == "ping"):
            if (self.runButton.text() == self.tr("Run")) :
                center = self.lineEdit.text().trimmed()
                if not center:
                    InfoHintDialog(self.tr("please input the IP address")).exec_()
#                     self.tipDlg.setTip(self.tr("请输入ping地址!!!"))
#                     self.tipDlg.show()
#                     self.tipDlg.move((desktop.width()-self.tipDlg.width())/2,(desktop.height()-self.tipDlg.height())/2)
                    self.runButton.setText(self.tr("Run"))
                else:
                    self.comBox.setDisabled(True)
                    self.pro = QProcess(self)
                    self.runButton.setText(self.tr("stop ping"))
                    cmdstr = "ping " +center
                    self.textBrowser.clear()
                    self.textBrowser.append(self.tr(" ping ")+center+self.tr(" result:"))
            else:
                self.comBox.setDisabled(False)
                self.runButton.setText(self.tr("Run"))
                self.pro.close()
        elif(self.comBox.currentText() == "ifconfig"):
            self.pro = QProcess(self)
            self.lineEdit.clear()
            self.lineEdit.setEnabled(False)
            self.textBrowser.clear()
            cmdstr = "ifconfig"
#             #如果comBox当前为traceroute
#         elif(self.comBox.currentText() == "traceroute"):
#                 goal = self.lineEdit.text()
#                 if (self.runButton.text() == u"执行"):
#                     if( goal.isEmpty() or goal.isNull() ):
#                         InfoHintDialog(u'请输入tracer地址：').exec_()
# #                         self.tipDlg.setTip(self.tr("请输入tracer地址："))
# #                         self.tipDlg.show()
# #                         self.tipDlg.move((desktop.width()-self.tipDlg.width())/2,(desktop.height()-self.tipDlg.height())/2)
# #                         
#                         #QMessageBox.information(self,self.tr("错误"),self.tr("请输入traceroute的目标地址"))
#                         #return
#                     else:
#                         self.proc = QProcess(self)
#                         #self.textBrowser.clear()
#                         cmdstrc = "traceroute -n "+ goal
#                         self.proc.start(cmdstrc)
#                         self.connect(self.proc, SIGNAL("readyReadStandardOutput()"),self.readR)
#                         self.connect(self.proc, SIGNAL("readyReadStandardError()"),self.readErrorR)
#                         if self.proc.waitForStarted(10) == True:
#                             self.comBox.setDisabled(True)
#                             self.runButton.setText(self.tr("停止执行"))
#                 else:
#                     self.runButton.setText(self.tr("执行"))
#                     self.comBox.setDisabled(False)
#                     self.proc.close()
#             #如果comBox当前为display
        elif (self.comBox.currentText() == "display"):
            self.pro = QProcess(self)
            cmdstr = "../lib/ccr_jytcapi display"
            self.textBrowser.clear()
            #如果当前命令cmdstr不为空，则
        elif (self.comBox.currentText() == "top"):
            if self.runButton.text() == self.tr("Run") :
                self.thread.start()
                self.comBox.setDisabled(True)
                self.runButton.setText(self.tr("stop top"))
            else:
                self.textBrowser.clear()
                self.thread.auto = False
                #self.thread.destroyed()
                self.comBox.setDisabled(False)
                self.runButton.setText(self.tr("Run"))
        if (cmdstr != ""):
                self.pro.start(cmdstr)#开启执行命令
                self.connect(self.pro, SIGNAL("readyReadStandardOutput()"),self.read)#读取执行正常输出槽函数
                self.connect(self.pro, SIGNAL("readyReadStandardError()"),self.readError)#执行异常槽函数
            
            #读取控制台输出
    def read(self):
        res = QString.fromLocal8Bit(self.pro.readAllStandardOutput())
        self.textBrowser.append(res)#添加到text框
        #读取错误
    def readError(self):
        res = QString.fromLocal8Bit(self.pro.readAllStandardError())
        self.textBrowser.append(res)
    def readR(self):
        
        res = QString.fromLocal8Bit(self.proc.readAllStandardOutput())
        #self.textBrowser.clear()
        self.textBrowser.append(res)
        


    def readErrorR(self):

        res = QString.fromLocal8Bit(self.proc.readAllStandardError())
        self.textBrowser.append(res)
        
    def updateWindow(self):
        if self.pro.isOpen():
            self.pro.close()
            
        self.thread.auto = False
        self.comBox.setDisabled(False)
        self.comBox.setCurrentIndex(0)
        self.runButton.setText((self.tr("Run")))
        self.pingLabel.setText(self.tr("Tip:please input the IP address of pinging,then get the result with clicking the button"))
        self.textBrowser.clear()

#本类创建一个HardWidget，之后作为一个组件添加到tab中        
class HardWidget(QWidget):
       
    def __init__(self,parent = None):
        super(HardWidget,self).__init__(parent)
        self.setStyleSheet("font-size : 16px")#设置整体字体
            #分别返回各个函数的返回值
        #self.mymem = self.memory_stat()#返回内存信息
        #self.mydisk = self.disk_stat()#返回硬盘信息
        #self.mycpu = self.cpu_stat()#返回cpu信息
        #self.myload = self.load_stat()#返回负载信息
        #self.myuptime = self.uptime_stat()#返回运行时间
        #self.mypass = self.readText()#读取文件信息，内容为密码
            #引入tipDialog弹出窗口，并且将其设置为最前端，后面窗口不可操作
#         self.tipDlg = TipDialog()
#         self.tipDlg.setModal(True)
        
        self.a = float()#声明一个float类型的數，之后作为本类中某个函数的参数
            #声明一个label，书写超级密码，字体，长度120
        self.passLabel = QLabel(self.tr("Super Password:"))
        self.passLabel.setFixedWidth(120)
        #self.passLabel.setFont(QFont("times",11))
        self.passLabel.setFont(QFont("",11))
            #声明一个label，书写提示信息
        self.tipLabel  = QLabel(self.tr("Tip:input the password to get hardware information"))
            #声明一个文本框，用来输入密码
        self.lineEdit  = QLineEdit()
        self.lineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        self.lineEdit.setEchoMode(QLineEdit.Password)
        self.lineEdit.setFixedWidth(250)
            #声明一个pushbutton，立即收集
        self.runButton = QPushButton(self.tr("Get"))
        self.runButton.setStyleSheet("background: rgb(7,87,198); color: white; width: 70px; height: 20px;font-size : 16px;")
            #声明一个textBrower，用来显示收集的信息
        self.textArea = QTextBrowser()
        
            #布局一，横向布局，添加passLabel,lineEdit,runButton，设置前后的空白分别为20和280，中间充满
        hLayout1 = QHBoxLayout()
        hLayout1.addSpacing(20)
        hLayout1.addWidget(self.passLabel)
        hLayout1.addWidget(self.lineEdit)
        hLayout1.addWidget(self.runButton)
        hLayout1.addSpacing(280)
            #布局二，横向布局，添加tipLabe，提示信息显示，设置前面的空白为20，后边充满
        hLayout2 = QHBoxLayout()
        hLayout2.addSpacing(20)
        hLayout2.addWidget(self.tipLabel)
            #布局三，横向布局，添加textArea，设这前后的空白为20和60，中间充满
        hLayout3 = QHBoxLayout()
        hLayout3.addSpacing(20)
        hLayout3.addWidget(self.textArea)
        hLayout3.addSpacing(60)
        
            #总其布局，纵向布局，将上面的三个布局加入其中，设置间隔为20，最下面的空白为40
        mainLayout = QVBoxLayout()
        mainLayout.addSpacing(20)
        mainLayout.addLayout(hLayout1)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(hLayout2)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(hLayout3)
        mainLayout.addSpacing(40)
        self.setLayout(mainLayout)
        #runButton的槽函数链接
        self.connect(self.runButton, SIGNAL("clicked()"),self.run)

    def keyPressEvent(self, event): 
        keyEvent = QKeyEvent(event)
        if keyEvent.key() == Qt.Key_Enter or keyEvent.key() == Qt.Key_Return:
            self.run()


    #获取内存信息的函数
    def memory_stat(self):
        mem = {}
        f = open("/proc/meminfo")
        lines = f.readlines()
        f.close()
        for line in lines:
            if len(line) < 2: continue
            name = line.split(':')[0]
            var = line.split(':')[1].split()[0]
            mem[name] = long(var)
        mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
        return mem
    #读取磁盘信息函数
    def getMntDistSize(self):
        cmd = "df -h --total | grep /var/lib/chost/disks"
        status = []
        output = ""
        hd = {}
        hd['available'] = 0
        hd['capacity'] = 0
        hd['free'] = 0
        hd['used'] = 0
        status = commands.getstatusoutput(cmd)
        if status[0] == 0:
            output = status[1]
        disklist = QString(output).simplified().split(" ")
        num = len(disklist)
        if num < 5:
            return hd
        else:
            if QString(disklist[3]).contains("T"):
                hd['free'] = int(float(disklist[3].split("T")[0])*1024*1024*1024)
            else:
                hd['free'] = int(float(disklist[3].split("G")[0])*1024*1024)
            if QString(disklist[1]).contains("T"):
                hd['capacity'] = int(float(disklist[1].split("T")[0])*1024*1024*1024)
            else:
                hd['capacity'] = int(float(disklist[1].split("G")[0])*1024*1024)
            if QString(disklist[2]).contains("T"):
                hd['used'] = int(float(disklist[2].split("T")[0])*1024*1024*1024)
            else:
                hd['used'] = int(float(disklist[2].split("G")[0])*1024*1024)
                
            hd['available'] = hd['capacity'] - hd['used']
        return hd
        
    def total_disk_stat(self):
        cmd = "df -h --total | grep total"
        status = []
        output = ""
        hd = {}
        hd['available'] = 0
        hd['capacity'] = 0
        hd['free'] = 0
        hd['used'] = 0
        status = commands.getstatusoutput(cmd)
        if status[0] == 0:
            output = status[1]
        disklist = QString(output).simplified().split(" ")
        num = len(disklist)
        if num < 5:
            return hd
        else:
            if QString(disklist[3]).contains("T"):
                hd['free'] = int(float(disklist[3].split("T")[0])*1024*1024*1024)
            else:
                hd['free'] = int(float(disklist[3].split("G")[0])*1024*1024)
            if QString(disklist[1]).contains("T"):
                hd['capacity'] = int(float(disklist[1].split("T")[0])*1024*1024*1024)
            else:
                hd['capacity'] = int(float(disklist[1].split("G")[0])*1024*1024)
            if QString(disklist[2]).contains("T"):
                hd['used'] = int(float(disklist[2].split("T")[0])*1024*1024*1024)
            else:
                hd['used'] = int(float(disklist[2].split("G")[0])*1024*1024)
                
            hd['available'] = hd['capacity'] - hd['used']
        return hd
    def disk_stat(self):
        hd={}
        hd['total'] = globalfunc.get_disk_size()
        return hd
    #读取cpu信息函数
    def cpu_stat(self):
        cpuinfo = {}
        cpu_info = globalfunc.get_cpu_info()
        cpuinfo["cpuinfo"] = cpu_info
        return cpuinfo
    #读取负载信息函数
    def load_stat(self):
        loadavg = {}
        f = open("/proc/loadavg")
        con = f.read().split()
        f.close()
        loadavg['lavg_1']=con[0]
        loadavg['lavg_5']=con[1]  #average load per five minute
        loadavg['lavg_15']=con[2]
        loadavg['nr']=con[3]
        loadavg['last_pid']=con[4]
        return loadavg
    #读取运行时间函数
    def uptime_stat(self):
        uptime = {}
        f = open("/proc/uptime")
        con = f.read().split()
        f.close()
        all_sec = float(con[0])
        MINUTE,HOUR,DAY = 60,3600,86400
        uptime['day'] = int(all_sec / DAY )
        uptime['hour'] = int((all_sec % DAY) / HOUR)
        uptime['minute'] = int((all_sec % HOUR) / MINUTE)
        uptime['second'] = int(all_sec % MINUTE)
        uptime['Free rate'] = float(con[1]) / float(con[0])
        return uptime
    #读取网络信息函数
    def net_stat(self):
        net = []
        f = open("/proc/net/dev")
        lines = f.readlines()
        f.close()
        for line in lines[2:]:
                con = line.split()
            #if line == "\n":
                if (len(con) == 16):
                    intf = {}
                    intf['interface'] = con[0].split(':')[0].rstrip()#first data includes two content
                    intf['ReceiveBytes'] = int(con[0].split(':')[1])
                    intf['ReceivePackets'] = int(con[1])
                    intf['ReceiveErrs'] = int(con[2])
                    intf['ReceiveDrop'] = int(con[3])
                    intf['ReceiveFifo'] = int(con[4])
                    intf['ReceiveFrames'] = int(con[5])
                    intf['ReceiveCompressed'] = int(con[6])
                    intf['ReceiveMulticast'] = int(con[7])
                    intf['TransmitBytes'] = int(con[8])
                    intf['TransmitPackets'] = int(con[9])
                    intf['TransmitErrs'] = int(con[10])
                    intf['TransmitDrop'] = int(con[11])
                    intf['TransmitFifo'] = int(con[12])
                    intf['Transmitcolls'] = int(con[13])
                    intf['Transmitcarrier'] = int(con[14])
                    intf['TransmitCompressed'] = int(con[15])
                    
                elif (len(con) == 17):
                    intf = {}
                    intf['interface'] = con[0]
                    intf['ReceiveBytes'] = int(con[1])
                    intf['ReceivePackets'] = int(con[2])
                    intf['ReceiveErrs'] = int(con[3])
                    intf['ReceiveDrop'] = int(con[4])
                    intf['ReceiveFifo'] = int(con[5])
                    intf['ReceiveFrames'] = int(con[6])
                    intf['ReceiveCompressed'] = int(con[7])
                    intf['ReceiveMulticast'] = int(con[8])
                    intf['TransmitBytes'] = int(con[9])
                    intf['TransmitPackets'] = int(con[10])
                    intf['TransmitErrs'] = int(con[11])
                    intf['TransmitDrop'] = int(con[12])
                    intf['TransmitFifo'] = int(con[13])
                    intf['Transmitcolls'] = int(con[14])
                    intf['Transmitcarrier'] = int(con[15])
                    intf['TransmitCompressed'] = int(con[16])
                net.append(intf)
        return net
        #将flaot类型的数，转换为string的函数
    def floatToString(self, a):
        if a <= 0 :
            e = int(a*100000000)
            b = QString().number(e)
            m = len(b)
            x = ""
        elif a > 0:
            e = int(a)
            x = QString().number(e)
            s = a - float(e)
            
            f = int(s*100000000)
            b = QString().number(f)
            m = len(b)
            
        if (8-m) == 0:
            n = b
        elif (8-m) == 1:
            n = "0" + b
        elif (8-m) == 2:
            n = "0" + "0" + b
        elif (8-m) == 3:
            n = "0" + "0" + "0" + b
        elif (8-m) == 4:
            n = "0" + "0" + "0" + "0" + b
        elif (8-m) == 5:
            n = "0" + "0" +"0" + "0" + "0" + b   
        else:
            n = "0" + "0" +"0" + "0" + "0" + "0" + b
        c = x +"."+ n
        return c
    
    #读文件，取密码
    def readText(self):
        return "cloudsterminal"
    
    #button运行函数
    def run(self):
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
            
        desktop = QApplication.desktop()
        self.mypass = self.readText()#读取文件信息，内容为密码
        if (self.lineEdit.text() == self.mypass):
                self.textArea.clear()
                self.lineEdit.clear()
      	        self.mymem = self.memory_stat()#返回内存信息
                self.mydisk = self.disk_stat()#返回硬盘信息
                self.mycpu = self.cpu_stat()#返回cpu信息
                self.myload = self.load_stat()#返回负载信息
                self.myuptime = self.uptime_stat()#返回运行时间
                usedText = QString().number(self.mymem['MemUsed'])
                totalText = QString().number(self.mymem['MemTotal'])
                freeText = QString().number(self.mymem['MemFree'])
                buffersText = QString().number(self.mymem['Buffers'])
                cachedText = QString().number(self.mymem['Cached'])
                self.textArea.append(self.tr("Memory:"))
                self.textArea.append(self.tr("Total Memory:") + "\t" + totalText + " \tKB "+ "\r\n" + self.tr("Used Memory:") + "\t" + usedText+ " \tKB "+ "\r\n" + self.tr("Free Memory:") + "\t" + freeText+ " \tKB "+ "\r\n" +"Buffers:\t\t"+ buffersText+ " \tKB "+ "\r\n" +"Cached:\t\t"+ cachedText+ " \tKB ")
                #self.textArea.setText(text2)
                self.textArea.append(" ")
                self.textArea.append(self.tr("Disk:"))
                self.textArea.append(self.tr("Total Disk:") + "\t" + self.mydisk["total"])
                self.textArea.append(" ")
                self.textArea.append(self.tr("Cpu Type:"))
                cpustr = ""
                for key in self.mycpu:
                    curcpu = key + ": " + self.mycpu[key] + "\n"
                    cpustr += curcpu
                self.textArea.append(cpustr)
                #self.textArea.append("\n")
                self.textArea.append(self.tr("Load information:"))
                self.textArea.append(self.tr("lavg_1:") + "\t" + self.myload['lavg_1'] +"\r\n" + self.tr("lavg_5:") + "\t" + self.myload['lavg_5'] +"\r\n" + self.tr("lavg_15:") + "\t" + self.myload['lavg_15'] +"\r\n" + self.tr("nr:") + "\t" + self.myload['nr'] +"\r\n" + self.tr("last_pid:") + "\t" + self.myload['last_pid'])
                self.textArea.append(" ")
                self.textArea.append(self.tr("Run Time:"))
                self.textArea.append(self.tr("Days:")+ "\t" + QString().number(self.myuptime['day']) + "\r\n" +self.tr("Hours:") + "\t"  + QString().number(self.myuptime['hour']) + "\r\n" +self.tr("Minutes:") + "\t" + QString().number(self.myuptime['minute']) + "\r\n" +self.tr("Seconds:") + "\t" + QString().number(self.myuptime['second']))
                a = self.floatToString(self.myuptime["Free rate"])
                self.textArea.append(self.tr("Free Rate:")+ "\t" + a)
                self.textArea.append(" ")
                
        elif self.lineEdit.text() == "":
            InfoHintDialog(self.tr("password is empty")).exec_()
            self.textArea.clear()
        else:
            InfoHintDialog(self.tr("password is wrong")).exec_()
            self.lineEdit.clear()
            
        
    def updateWindow(self):
        self.runButton.setText(self.tr("Get"))
        self.textArea.clear()
        self.passLabel.setText(self.tr("Super Password:"))
        self.tipLabel.setText(self.tr("Tip:input the password to get hardware information"))

class ToolWidget(QDialog):
    def __init__(self,parent = None):
        super(ToolWidget,self).__init__(parent)
        
        #self.desktop = QDesktopWidget()
        self.desktop = QApplication.desktop()
#         self.setFixedSize(800,600)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        
        self.move((self.desktop.width()-self.width())/2,(self.desktop.height()-self.height())/2)
        
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
            
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
        
        self.tabWidget = TabWidget()
        #self.tabWidget.setFont(QFont("Times", 10, QFont.Bold))
        self.tabWidget.setFont(QFont("", 10, QFont.Bold))
        self.tabWidget.netService = NetWidget(self)
        
        self.tabWidget.hardService = HardWidget(self)
        #self.tabWidget.netService.textBrowser.setFixedWidth(self.geometry().width()*4/5)
        self.tabWidget.addTab(self.tabWidget.netService, self.tr("NetInfo"))
        self.tabWidget.addTab(self.tabWidget.hardService, self.tr("HardInfo"))
        
        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)
        layout.setMargin(0)
        self.setLayout(layout)
        
        self.tabWidget.netService.lineEdit.setFocus(True)
        
        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon("images/close.png"))
        
        self.closeButton.setFlat(True)      
        self.closeButton.mousePressed = False
        
        self.connect(self.closeButton, SIGNAL("clicked()"),self.cancel)
        #self.connect(self.cancelButton, SIGNAL("clicked()"),self.cancel)
        
    def mouseMoveEvent(self,event):
        if self.closeButton.mousePressed:
            self.move(self.pos() + event.pos() - self.currentPos)   
        self.default = QString()
    def mousePressEvent(self,event):
        if event.buttons() == Qt.LeftButton:
            self.currentPos = event.pos()
            self.closeButton.mousePressed = True
   
    def mouseReleaseEvent(self,event):
        if event.buttons() == Qt.LeftButton:
            self.closeButton.mousePressed = False
            
    def cancel(self):
        self.close() 
        
    def paintEvent(self,event):
        self.closeButton.setFixedSize(30,30)
        self.closeButton.setIconSize(QSize(30,30))
        self.closeButton.move(QPoint(self.geometry().width()-self.closeButton.frameGeometry().width() - (self.tabWidget.tabBar().height()-self.closeButton.geometry().height())/2,(self.tabWidget.tabBar().height()-self.closeButton.geometry().height())/2))
# app = QApplication(sys.argv)
# hardService = HardWidget()
