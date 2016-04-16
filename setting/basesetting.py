# -*- coding: utf-8 -*-  

from PyQt4.QtCore import SIGNAL, QTranslator, QCoreApplication, Qt
from PyQt4.QtGui import QWidget, QLabel, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,\
                        QMessageBox
import re
import commands
import os
from configFileParser import ConfigFileParser
from base.infohintdialog import InfoHintDialog
import globalfunc
from storeinfoparser import StoreInfoParser
import globalvariable
from logrecord import LogRecord
import common

class BaseSettingWidget(QWidget):
        
    def __init__(self, app, parent = None):
        super(BaseSettingWidget,self).__init__(parent)
        
        self.app = app
        self.setStyleSheet("font-size : 16px;")

        self.pcName = QLabel(self.tr("Student Computer Name"))
        self.cloudsHostIpLabel = QLabel(self.tr("Mcos Center Address"))
        self.backupCloudsHostIpLabel = QLabel(self.tr("Backup Mcos Center Address"))
        
        self.pcNameLineEdit = QLineEdit(self.tr("local"))
        self.pcNameLineEdit.setEnabled(False)
        self.pcNameLineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        self.pcNameLineEdit.setFixedSize(300, 30)
        terminalName = StoreInfoParser.instance().getTerminalName()
        if terminalName:
            self.pcNameLineEdit.setText(terminalName)
        else:
            StoreInfoParser.instance().setTerminalName(str(terminalName))
        
        self.cloudsHostIp = QLineEdit()
        self.cloudsHostIp.setContextMenuPolicy(Qt.NoContextMenu)
        self.cloudsHostIp.setFixedSize(300, 30)
        serverIP = self.getServerAddress()
        if serverIP:
            self.cloudsHostIp.setText(serverIP)
            
        self.currentCloudsHostIp = self.cloudsHostIp.text()
            
        self.backupCloudsHostIp = QLineEdit()
        self.backupCloudsHostIp.setContextMenuPolicy(Qt.NoContextMenu)
        self.backupCloudsHostIp.setFixedSize(300, 30)
        backupServerIP = self.getBackupServerAddress()
        if backupServerIP:
            self.backupCloudsHostIp.setText(backupServerIP)
        
        self.saveBtn = QPushButton(self.tr("Save"))
        self.saveBtn.setStyleSheet("background: rgb(7,87,198); color: white; width: 90px; height: 30px;font-size : 16px;")
        
        gridLayout = QGridLayout()
        gridLayout.setSpacing(15)
        gridLayout.setMargin(10)
        gridLayout.addWidget(self.pcName, 0, 0, 1, 1)
        gridLayout.addWidget(self.pcNameLineEdit, 0, 1, 1, 1)
        gridLayout.addWidget(self.cloudsHostIpLabel, 1, 0, 1, 1)
        gridLayout.addWidget(self.cloudsHostIp, 1, 1, 1, 1)
        gridLayout.addWidget(self.backupCloudsHostIpLabel, 2, 0, 1, 1)
        gridLayout.addWidget(self.backupCloudsHostIp, 2, 1, 1, 1)
        
        topLayout = QHBoxLayout()
        topLayout.addStretch()
        topLayout.addSpacing(50)
        topLayout.addLayout(gridLayout)
        topLayout.addStretch(1)
        
        bottomHLayout = QHBoxLayout()
        bottomHLayout.addStretch()
        bottomHLayout.addWidget(self.saveBtn)
        bottomHLayout.addStretch()
        
        vLayout = QVBoxLayout()
        vLayout.addStretch()
        vLayout.addSpacing(50)
        vLayout.addLayout(topLayout)
        vLayout.addStretch(2)
        vLayout.addSpacing(10)
        vLayout.addLayout(bottomHLayout)
        
        self.setLayout(vLayout)
        
        self.connect(self.saveBtn, SIGNAL("clicked()"),self.slotSave)
    
    def updateWindow(self):
        self.pcName.setText(self.tr("Student Computer Name"))
        self.cloudsHostIpLabel.setText(self.tr("Mcos Center Address"))
        self.backupCloudsHostIpLabel.setText(self.tr("Backup Mcos Center Address"))
        self.saveBtn.setText(self.tr("Save"))
        
    #def getHostName(self):
    #    if self.hostFile == "/etc/sysconfig/network":
    #        statusOutput = commands.getstatusoutput("cat /etc/sysconfig/network | awk -F = '/HOSTNAME/{print $2}'")
    #        if statusOutput[0] == 0:
    #            output = statusOutput[1]
    #            return output
    #    elif self.hostFile == "/etc/hostname":
    #        statusOutput = commands.getstatusoutput("cat %s" % self.hostFile)
    #        if statusOutput[0] == 0:
    #            output = statusOutput[1]
    #            return output
    #    
    #    return None
    
    def getBackupServerAddress(self):
        return StoreInfoParser.instance().getBackupServerAddress()
        # parser = ConfigFileParser.instance()
        # if parser.has_section("cloudsServerAddress"):
        #     if parser.has_option("cloudsServerAddress", "ipbackup"):
        #         return parser.getValue("cloudsServerAddress", "ipbackup")
        #
        # return None
    
    def getServerAddress(self):
        """获取服务器地址"""
        return StoreInfoParser.instance().getCloudsServerIP()
        # parser = ConfigFileParser.instance()
        # if parser.has_section("cloudsServerAddress"):
        #     if parser.has_option("cloudsServerAddress", "ip"):
        #         return parser.getValue("cloudsServerAddress", "ip")
        #
        # return None
        
    def slotSave(self):
        """保存设置"""
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
        pcName = self.pcNameLineEdit.text().trimmed()
        serverIp = self.cloudsHostIp.text().trimmed()
        backupServerIp = self.backupCloudsHostIp.text().trimmed()
        
        #判断输入的内容是否为空
        if pcName.isEmpty() or pcName.isNull() or serverIp.isEmpty() or serverIp.isNull():
            InfoHintDialog(self.tr("computer name or cloud address is empty!")).exec_()
            return
        
        #判断输入的内容的有效性
        pattern = '^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$'
        matchObj = re.match(pattern, str(serverIp))
        if matchObj is None:
            InfoHintDialog(self.tr("cloud address is wrong, please input again!")).exec_()
            self.cloudsHostIp.setFocus()
            return False
        
        if backupServerIp == serverIp:
            InfoHintDialog(self.tr("backupIp is same as serverIP, please input again!")).exec_()
            self.backupCloudsHostIp.setFocus()
            return False
        
        if backupServerIp:
            matchObj = re.match(pattern, str(backupServerIp))
            if matchObj is None:
                InfoHintDialog(self.tr("backcloud address is wrong, please input again!")).exec_()
                self.backupCloudsHostIp.setFocus()
                return False
        
        
        #保存服务器地址到配置文件
        StoreInfoParser.instance().setServerAddress(serverIp)
        StoreInfoParser.instance().setBackUpServerAddress(backupServerIp)

        if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:
            globalfunc.umountFile(SYS_HOSTNAME_CONFIG)

        StoreInfoParser.instance().setTerminalName(str(pcName))
        # if self.hostFile == "/config/etc/hostname" or self.hostFile == "/etc/hostname":
        #     #修改计算机名称到系统配置文件
        #     writeCmd = "echo '%s' > %s" % (pcName, self.hostFile)
        #     if os.system(writeCmd) != 0:
        #         if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:
        #             globalfunc.mountFile(SYS_HOSTNAME_CONFIG)
        #         InfoHintDialog(u'修改计算机名称失败').exec_()
        #         return
        # elif self.hostFile == "/config/etc/sysconfig/network" or self.hostFile == "/etc/sysconfig/network":
        #     cmdDelete = "sed -i /HOSTNAME/d %s" % self.hostFile
        #     cmdAppend = "sed -i '$ a\\HOSTNAME=%s' %s" % (pcName, self.hostFile)
        #     cmd = cmdDelete + "&&" + cmdAppend
        #     if os.system(cmd) != 0:
        #         if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:
        #             globalfunc.mountFile(SYS_HOSTNAME_CONFIG)
        #         InfoHintDialog(u'修改计算机名称失败').exec_()
        #         return

        if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:
            globalfunc.mountFile(SYS_HOSTNAME_CONFIG)

        if self.currentCloudsHostIp != serverIp and self.app:
            self.app.vmWidget.hide()
            self.app.loadingWiget.show()
        
        #弹出修改成功信息框
        InfoHintDialog(self.tr("saved success!")).exec_()
        return
    
        
        
        
        
