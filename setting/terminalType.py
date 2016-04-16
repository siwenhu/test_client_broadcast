# -*- coding: utf-8 -*-  

from PyQt4.QtCore import Qt, SIGNAL, QString, QFile, QIODevice, QTextStream
from PyQt4.QtGui import QWidget, QLabel, QLineEdit, QGridLayout, QVBoxLayout, QGroupBox, QCheckBox,\
                        QHBoxLayout, QPushButton, QMessageBox, QRadioButton
import os
from base.infohintdialog import InfoHintDialog
from restartnetworkthread import RestartNetworkThread
import commands
from storeinfoparser import StoreInfoParser
from logrecord import LogRecord

class TerminalTypeWidget(QWidget):
        
    def __init__(self, app, parent = None):
        super(TerminalTypeWidget,self).__init__(parent)
        self.setStyleSheet("font-size : 16px;")
        self.app = app
        
        self.initLayout()
        self.initTerminalVM()
        
        self.connect(self.settingBtn, SIGNAL("clicked()"),self.slotSave)
        
    def initTerminalVM(self):
        if self.isTerminal():
            self.cTerminalRadioBtn.setChecked(True)
        else:
            self.cDesktopRadioBtn.setChecked(True)
    
        self.replaceFirstMenuName()

    def initLayout(self):
        self.terminalTypeGroupbox = QGroupBox(u'终端类型')
        
        self.cDesktopRadioBtn = QRadioButton(u'桌面虚拟化')
        self.cTerminalRadioBtn = QRadioButton(u'终端虚拟化')
        
        self.settingBtn = QPushButton(u"设置")
        self.settingBtn.setStyleSheet("background: rgb(7,87,198); color: white; width: 90px; height: 30px;font-size : 16px;")
        
        topVLayout = QVBoxLayout()
        topVLayout.setSpacing(10)
        topVLayout.setMargin(10)
        
        topVLayout.addSpacing(30)
        topVLayout.addWidget(self.cDesktopRadioBtn)
        topVLayout.addSpacing(20)
        topVLayout.addWidget(self.cTerminalRadioBtn)
        topVLayout.addSpacing(50)
        
        topHLayout = QHBoxLayout()
        topHLayout.setSpacing(10)
        topHLayout.setMargin(10)
        
        topHLayout.addSpacing(40)
        topHLayout.addLayout(topVLayout)
        topHLayout.addSpacing(160)
   
        self.terminalTypeGroupbox.setLayout(topHLayout)
        
        bottomHLayout = QHBoxLayout()
        bottomHLayout.addStretch()
        bottomHLayout.addWidget(self.settingBtn)
        bottomHLayout.addStretch()
        
        #布局调整
        vLayout = QVBoxLayout()
        vLayout.addStretch()
        vLayout.addWidget(self.terminalTypeGroupbox)
        vLayout.addSpacing(80)
        vLayout.addStretch()
        
        topMainLayout = QHBoxLayout()
        topMainLayout.addStretch()
        topMainLayout.addLayout(vLayout)
        topMainLayout.addStretch()
        
        mainHLayout = QVBoxLayout()
        mainHLayout.addLayout(topMainLayout)
        mainHLayout.addLayout(bottomHLayout)
        
        self.setLayout(mainHLayout)
        
        
    def isTerminal(self):
        typeValue = StoreInfoParser.instance().getTerminalType()
        if typeValue == None or typeValue == "desktopVM":
            return False
        else:
            return True
    
    def replaceFirstMenuName(self):
#         pass
        grub_file = QFile("/boot/grub/grub.conf")
        if not grub_file.open(QIODevice.ReadOnly):
            grub_file.close()
            return
     
        fs = QTextStream(grub_file)
        fileContent = fs.readAll()
        grub_file.close()
        if QString(fileContent).contains("MCOS cDesktop Client Start"):
            return
     
        cmd =  "sed -i \"s/CentOS (2.6.32-431.el6.i686)/MCOS cDesktop Client Start/g\" /boot/grub/grub.conf";
     
        ok = os.system(cmd)
        if ok != 0:
            LogRecord.instance().logger(u"替换grub.cfg中的'CentOS (2.6.32-431.el6.i686)'失败")
     
        if QString(fileContent).contains("hiddenmenu"):
            os.system("sed -i \"/hiddenmenu/d\" /boot/grub/grub.conf")
    
    def slotSave(self):
        if self.cDesktopRadioBtn.isChecked():
            if not self.setCDesktop():
                InfoHintDialog(u'设置桌面虚拟化失败').exec_()
            else:
                StoreInfoParser.instance().setTerminalType("desktopVM")
                InfoHintDialog(u'设置桌面虚拟化成功').exec_()
        else:
            if not self.setCTerminal():
                InfoHintDialog(u'设置终端虚拟化失败').exec_()
            else:
                StoreInfoParser.instance().setTerminalType("terminalVM")
                InfoHintDialog(u'设置终端虚拟化成功').exec_()
            
    def setMenuDefaultValue(self, value):
        cmdlist = "cat /boot/grub/grub.conf | awk '{ if($0 ~ \"default=\") {print NR}}'"
         
        statusOutput = commands.getstatusoutput(cmdlist)
        if statusOutput[0] == 0:
            rowNum = statusOutput[1]
            defaultValueCmd = QString("sed -i '%1s/.*/default=%2/g' /boot/grub/grub.conf").arg(rowNum).arg(value)
            ok = os.system(str(defaultValueCmd))
            if ok != 0:
                LogRecord.instance().logger(u"执行命令‘sed -i '%1s/.*/default=%s/g' /boot/grub/grub.conf’失败" % str(value))
                return False
        else:
            LogRecord.instance().logger(u"执行命令‘cat /boot/grub/grub.conf | awk '{ if($0 ~ \"default=\") {print NR}}’失败")
            return False
        
        return True
          
    def setMenuTimeoutValue(self, value):
        #修改timeout值
        cmdlist = "cat /boot/grub/grub.conf | awk '{ if($0 ~ \"timeout=\") {print NR}}'"
         
        statusOutput = commands.getstatusoutput(cmdlist)
        if statusOutput[0] == 0:
            rowNum = statusOutput[1]
            defaultValueCmd = QString("sed -i '%1s/.*/timeout=%2/g' /boot/grub/grub.conf").arg(rowNum).arg(value)
            ok = os.system(str(defaultValueCmd))
            if ok != 0:
                LogRecord.instance().logger(u"执行命令‘sed -i '%1s/.*/timeout=%s/g' /boot/grub/grub.conf’失败" % str(value))
                return False
        else:
            LogRecord.instance().logger(u"执行命令‘cat /boot/grub/grub.conf | awk '{ if($0 ~ \"timeout=\") {print NR}}’失败")
            return False
        
        return True
          
    def setCDesktop(self):
        #修改默认值default
        if not self.setMenuDefaultValue(0):
            return False
        
        if not self.setMenuTimeoutValue(0):
            return False
        
        return True
        

    def setCTerminal(self):
        cmdlist = "cat /boot/grub/grub.conf"
         
        statusOutput = commands.getstatusoutput(cmdlist)
        if statusOutput[0] == 0:
            content = statusOutput[1]
        
            if not QString(content).contains("MCOS cTerminal Client Start"):
                insertContent = "title MCOS cTerminal Client Start\\n\\t" + \
                        "root (hd0,0)\\n\\t" + \
                        "kernel /boot/boot.krn\\n\\t" + \
                        "boot\\n"
                        
#                 insertContent = "sdfwef"
                addCmd = "sed -i '$a %s' /boot/grub/grub.conf" % insertContent
                if os.system(addCmd) != 0:
                    LogRecord.instance().logger(u"执行命令‘sed -i '%sa %s' /boot/grub/grub.conf失败")
                    return False
                
            
            if not self.setMenuDefaultValue(1):
                return False
        
            if not self.setMenuTimeoutValue(5):
                return False
            
            return True
    
        else:
            return False
    