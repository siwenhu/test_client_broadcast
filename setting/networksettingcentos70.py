# -*- coding: utf-8 -*-  

from PyQt4.QtCore import Qt, SIGNAL, QString, QTranslator, QCoreApplication
from PyQt4.QtGui import QWidget, QLabel, QLineEdit, QGridLayout, QVBoxLayout, QGroupBox, QCheckBox,\
                        QHBoxLayout, QPushButton, QMessageBox
import os
import re
from base.infohintdialog import InfoHintDialog
from restartnetworkthread import RestartNetworkThread
import globalfunc
import commands
import globalvariable
import common
from logrecord import LogRecord
from storeinfoparser import StoreInfoParser

class NetWorkSettingWidget(QWidget):
        
    def __init__(self, app, parent = None):
        super(NetWorkSettingWidget,self).__init__(parent)
        self.setStyleSheet("font-size : 16px;")
        self.app = app

        self.setNetworkCardFilePath()
        
        self.initLayout()
        
        self.initCheckBoxStatus()
        
        self.restartNetworkTD = RestartNetworkThread()
        self.waitingDlg = InfoHintDialog(None)
        
        #绑定信号
        self.connect(self.autoGetIpCheckbox, SIGNAL("stateChanged(int)"),self.slotSettingDHCPType)
        
        self.connect(self.staticIpGroupbox, SIGNAL("clicked(bool)"),self.slotSettingStaticType)
        
        self.connect(self.autoGetDNSCheckBox, SIGNAL("stateChanged(int)"),self.slotSettingDNSType)
        
        self.connect(self.dnsServerAddressGroupbox, SIGNAL("clicked(bool)"),self.slotSettingCustomDNSType)
        
        self.connect(self.saveBtn, SIGNAL("clicked()"),self.slotSave)
        
        self.connect(self.restartNetworkTD, SIGNAL("restartNetwork"),self.slotShowRestartNetworkInfo)

    def setNetworkCardFilePath(self):
        #self.networkconfigFile = common.NETWORK_CONFIG_CENTOS_7_0 + "br0"
        #self.bridgeNetworkconfigFile = common.NETWORK_CONFIG_CENTOS_7_0 + "br0"
        ethName = common.DEFAULT_NETCARD_NAME
        ethNameList = globalfunc.getEthNameList()
        if not ethNameList:
            LogRecord.instance().logger.info(u"获取网卡名称失败！")
        else:
            ethName = ethNameList[0]

        self.originalNetConfigFile = common.NETWORK_CONFIG_CENTOS_7_0 + ethName
        LogRecord.instance().logger.info(u"获取网卡名称:%s" % self.originalNetConfigFile)
        
        self.originalBridgerNetConfigFile = common.BRIDGER_NETWORK_CONFIG_CENTOS_7_0
        LogRecord.instance().logger.info(u"获取bridge网卡名称:%s" % self.originalNetConfigFile)

        self.networkconfigFile = self.originalNetConfigFile
        self.bridgeNetworkconfigFile = self.originalBridgerNetConfigFile
        if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:#running env
            self.networkconfigFile = globalfunc.convertPathToConfigPath(self.originalNetConfigFile)
            self.bridgeNetworkconfigFile = globalfunc.convertPathToConfigPath(self.originalBridgerNetConfigFile)

        
        #self.networkconfigFile = common.NETWORK_CONFIG_CENTOS_7_0 + "br0"

    def initLayout(self):
        #IP设置
        self.autoGetIpCheckbox = QCheckBox(self.tr("Auto get IP"))
        
        self.staticIpGroupbox = QGroupBox(self.tr("Use this IP"))
        self.staticIpGroupbox.setCheckable(True)
        
        self.ipLabel = QLabel(self.tr("IP address"))
        self.netmastLabel = QLabel(self.tr("Net mask"))
        self.defaultGatewayLabel = QLabel(self.tr("Default gateway"))
        
        topSpaceWidget = QLabel()
        topSpaceWidget.setFixedHeight(1)
        
        self.ip = QLineEdit()
        self.ip.setContextMenuPolicy(Qt.NoContextMenu)
        self.ip.setFixedSize(400, 30)
        self.netmast = QLineEdit()
        self.netmast.setContextMenuPolicy(Qt.NoContextMenu)
        self.defaultGateway = QLineEdit()
        self.defaultGateway.setContextMenuPolicy(Qt.NoContextMenu)
        
        topGridLayout = QGridLayout()
        topGridLayout.setSpacing(15)
        topGridLayout.setMargin(20)
        topGridLayout.addWidget(self.ipLabel, 0, 0, 1, 1)
        topGridLayout.addWidget(self.ip, 0, 1, 1, 1)
        topGridLayout.addWidget(self.netmastLabel, 1, 0, 1, 1)
        topGridLayout.addWidget(self.netmast, 1, 1, 1, 1)
        topGridLayout.addWidget(self.defaultGatewayLabel, 2, 0, 1, 1)
        topGridLayout.addWidget(self.defaultGateway, 2, 1, 1, 1)
        topGridLayout.addWidget(topSpaceWidget, 3, 0, 1, 1)
        
        self.staticIpGroupbox.setLayout(topGridLayout)
        
        #DNS设置
        self.autoGetDNSCheckBox = QCheckBox(self.tr("Auto Get DNS"))
        
        self.dnsServerAddressGroupbox = QGroupBox(self.tr("Use This DNS"))
        self.dnsServerAddressGroupbox.setCheckable(True)
        
        self.dnsLabel = QLabel(self.tr("DNS"))
        self.backupDnsLabel = QLabel(self.tr("Backup DNS"))
        
        bottomSpaceWidget = QLabel()
        bottomSpaceWidget.setFixedHeight(1)
        
        self.dns = QLineEdit()
        self.dns.setContextMenuPolicy(Qt.NoContextMenu)
        self.backupDns = QLineEdit()
        self.backupDns.setContextMenuPolicy(Qt.NoContextMenu)
        
        self.saveBtn = QPushButton(self.tr("Save"))
        self.saveBtn.setStyleSheet("background: rgb(7,87,198); color: white; width: 90px; height: 30px;font-size : 16px;")
        
        bottomGridLayout = QGridLayout()
        bottomGridLayout.setSpacing(15)
        bottomGridLayout.setMargin(20)
        bottomGridLayout.addWidget(self.dnsLabel, 0, 0, 1, 1)
        bottomGridLayout.addWidget(self.dns, 0, 1, 1, 1)
        bottomGridLayout.addWidget(self.backupDnsLabel, 1, 0, 1, 1)
        bottomGridLayout.addWidget(self.backupDns, 1, 1, 1, 1)
        bottomGridLayout.addWidget(bottomSpaceWidget, 2, 0, 1, 1)
        
        self.dnsServerAddressGroupbox.setLayout(bottomGridLayout)
        
        #布局调整
        vLayout = QVBoxLayout()
        vLayout.setSpacing(10)
        vLayout.setMargin(10)
        
        vLayout.addWidget(self.autoGetIpCheckbox)
        vLayout.addWidget(self.staticIpGroupbox)
        vLayout.addSpacing(15)
        vLayout.addWidget(self.autoGetDNSCheckBox)
        vLayout.addWidget(self.dnsServerAddressGroupbox)
        vLayout.addStretch()
        
        topMainLayout = QHBoxLayout()
        topMainLayout.addStretch()
        topMainLayout.addSpacing(50)
        topMainLayout.addLayout(vLayout)
        topMainLayout.addStretch(2)
        
        bottomHLayout = QHBoxLayout()
        bottomHLayout.addStretch()
        bottomHLayout.addWidget(self.saveBtn)
        bottomHLayout.addStretch()
        
        mainVLayout = QVBoxLayout()
        mainVLayout.addLayout(topMainLayout)
        mainVLayout.addSpacing(10)
        mainVLayout.addLayout(bottomHLayout)
        
        self.setLayout(mainVLayout)
    
    def updateWindow(self):
        self.autoGetDNSCheckBox.setText(self.tr("Auto Get DNS"))
        self.autoGetIpCheckbox.setText(self.tr("Auto get IP"))
        self.dnsServerAddressGroupbox.setTitle(self.tr("Use This DNS"))
        self.staticIpGroupbox.setTitle(self.tr("Use this IP"))
        self.ipLabel.setText(self.tr("IP address"))
        self.netmastLabel.setText(self.tr("Net mask"))
        self.defaultGatewayLabel.setText(self.tr("Gate way"))
        self.dnsLabel.setText(self.tr("DNS"))
        self.backupDnsLabel.setText(self.tr("Backup DNS"))
        self.saveBtn.setText(self.tr("Save"))
        
    def slotShowRestartNetworkInfo(self, status):
        
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
        """显示重启网络的状态信息"""
        
        if status == "Start":
            self.waitingDlg.setHintInfo(self.tr("network is restarting, waiting..."))
        elif status == "Success":
            self.waitingDlg.setHintInfo(self.tr("network start success!"))
            vmtype = StoreInfoParser.instance().getVmType()
            if vmtype == "offline":
                pass 
        elif status == "Failed":
            self.waitingDlg.setHintInfo(self.tr("network restart failed!"))
        else:
            return
        
        if self.waitingDlg.isHidden():
            self.waitingDlg.exec_()
        
    def slotSave(self):
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
            
        if not self.checkInputValid():
            return

        if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:#running
            if not os.path.exists(self.networkconfigFile):
                os.system("mkdir -p %s" % os.path.dirname(self.networkconfigFile))#create dir
                os.mknod(self.networkconfigFile)#create empty file
                os.system("echo \"%s\" >> /config/files" % self.originalNetConfigFile)#mark
                
            if not os.path.exists(self.bridgeNetworkconfigFile):
                os.system("mkdir -p %s" % os.path.dirname(self.bridgeNetworkconfigFile))#create dir
                os.mknod(self.bridgeNetworkconfigFile)#create empty file
                os.system("echo \"%s\" >> /config/files" % self.originalBridgerNetConfigFile)#mark


            if not os.path.isfile(self.originalNetConfigFile):
                os.system("mkdir -p %s" % os.path.dirname(self.originalNetConfigFile))
                os.mknod(self.originalNetConfigFile)
                
            if not os.path.isfile(self.originalBridgerNetConfigFile):
                os.system("mkdir -p %s" % os.path.dirname(self.originalBridgerNetConfigFile))
                os.mknod(self.originalBridgerNetConfigFile)
        else:
            if not os.path.exists(self.networkconfigFile):
                os.system("mkdir -p %s" % os.path.dirname(self.networkconfigFile))#create dir
                os.mknod(self.networkconfigFile)#create empty file
                #os.system("echo \"%s\" >> /config/files" % self.originalNetConfigFile)#mark
                
            if not os.path.exists(self.bridgeNetworkconfigFile):
                #os.system("mkdir -p %s" % os.path.dirname(self.networkconfigFile))#create dir
                os.mknod(self.bridgeNetworkconfigFile)#create empty file
                #os.system("echo \"%s\" >> /config/files" % self.originalNetConfigFile)#mark


            if not os.path.isfile(self.originalNetConfigFile):
                os.system("mkdir -p %s" % os.path.dirname(self.originalNetConfigFile))
                os.mknod(self.originalNetConfigFile)
                
            if not os.path.isfile(self.originalBridgerNetConfigFile):
                os.system("mkdir -p %s" % os.path.dirname(self.originalBridgerNetConfigFile))
                os.mknod(self.originalBridgerNetConfigFile)
                

        if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:#running
            globalfunc.umountFile(self.originalNetConfigFile)
            globalfunc.umountFile(self.originalBridgerNetConfigFile)


        if self.autoGetIpCheckbox.isChecked():
            if not self.setDynamicNetwork():
                if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:
                    globalfunc.mountFile(self.originalNetConfigFile)
                    globalfunc.mountFile(self.originalBridgerNetConfigFile)
                return
        elif self.staticIpGroupbox.isChecked():
            if not self.setStaticNetwork():
                if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:
                    globalfunc.mountFile(self.originalNetConfigFile)
                    globalfunc.mountFile(self.originalBridgerNetConfigFile)
                return


        if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:
            globalfunc.mountFile(self.originalNetConfigFile)
            globalfunc.mountFile(self.originalBridgerNetConfigFile)

        #重新启动网络
        self.restartNetworkTD.start()
        
        return
            
    def initCheckBoxStatus(self):
        """读取网络配置文件，初始化相应的checkbox的状态"""
        [netType, DNSType] = self.getNetworkType()
        if netType == "dhcp":
            self.autoGetIpCheckbox.setChecked(True)
            self.staticIpGroupbox.setChecked(False)
        else:
            self.autoGetIpCheckbox.setChecked(False)
            self.staticIpGroupbox.setChecked(True)
            [ip, netmask, gateway] = self.getStaticNetworkInfo()
            if ip:
                self.ip.setText(ip)
                
            if netmask:
                self.netmast.setText(netmask)
                
            if gateway:
                self.defaultGateway.setText(gateway)
                
            
        if DNSType == "AUTODNS":
            self.autoGetDNSCheckBox.setChecked(True)
            self.dnsServerAddressGroupbox.setChecked(False)
        else:
            self.autoGetDNSCheckBox.setChecked(False)
            self.dnsServerAddressGroupbox.setChecked(True)
            [DNS_first, DNS_second] = self.getCustomDNSInfo()
            if DNS_first:
                self.dns.setText(DNS_first)
            
            if DNS_second:
                self.backupDns.setText(DNS_second)
            
            
    def getCustomDNSInfo(self):
        """得到自定义DNS的内容"""
        DNS_first = None
        DNS_second = None
        statusOutput = commands.getstatusoutput("cat %s" % self.bridgeNetworkconfigFile)
        if statusOutput[0] == 0:
            outputList = QString(statusOutput[1]).split("\n")
            for value in outputList:
                if value.split("=")[0] == "DNS1":
                    DNS_first = value.split("=")[1]
                elif value.split("=")[0] == "DNS2":
                    DNS_second = value.split("=")[1]
                    
        return [DNS_first, DNS_second]
        
            
    def getStaticNetworkInfo(self):
        """得到静态网络的信息"""
        ip = netmask = gateway = None
        statusOutput = commands.getstatusoutput("cat %s" % self.bridgeNetworkconfigFile)
        if statusOutput[0] == 0:
            outputList = QString(statusOutput[1]).split("\n")
            for value in outputList:
                if value.split("=")[0] == "IPADDR":
                    ip = value.split("=")[1]
                elif value.split("=")[0] == "NETMASK":
                    netmask = value.split("=")[1]
                elif value.split("=")[0] == "GATEWAY":
                    gateway = value.split("=")[1]
            
        return [ip, netmask, gateway]
            
    def getNetworkType(self):
        """得到网络是静态还是动态类型"""
        netType = None
        DNSType = None
        statusOutput = commands.getstatusoutput("cat %s" % self.bridgeNetworkconfigFile)
        if statusOutput[0] == 0:
            output = QString(statusOutput[1])
            if output.contains("dhcp"):
                netType = "dhcp"
            else:
                netType = "static"
                
            if output.contains("DNS"):
                DNSType = "customDNS"
            else:
                DNSType = "AUTODNS"
                
        return [netType, DNSType]
            
    def checkInputValid(self):
        """检测输入的有效性"""
        if self.checkStaticIPInputValid() and self.checkDnsInputValid():
            return True
        return False
    
    def checkStaticIPInputValid(self):
        """检查静态IP输入内容的有效性"""
        ip = self.ip.text().trimmed()
        netmask = self.netmast.text().trimmed()
        gateway = self.defaultGateway.text().trimmed()
        
        if not self.autoGetIpCheckbox.isChecked():
            if ip.isEmpty() or ip.isNull() or netmask.isEmpty() or netmask.isNull():
                InfoHintDialog(self.tr("IP address or net mask is empty")).exec_()
                return False
            
            pattern = '^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$'
            matchObj = re.match(pattern, ip)
            if matchObj is None:
                InfoHintDialog(self.tr("IP address is wrong, please input again")).exec_()
                self.ip.setFocus()
                return False
            
            matchObj = re.match(pattern, str(netmask))
            if matchObj is None:
                InfoHintDialog(self.tr("Net mask is wrong")).exec_()
                self.netmast.setFocus()
                return False
            
            if gateway:
                matchObj = re.match(pattern, str(gateway))
                if matchObj is None:
                    InfoHintDialog(self.tr("Gate way is wrong")).exec_()
                    self.netmast.setFocus()
                    return False
        
        return True
    
    def checkDnsInputValid(self):
        """检查DNS输入的内容的有效性"""
        if not self.autoGetDNSCheckBox.isChecked():
            dns = self.dns.text().trimmed()
            backupDns = self.backupDns.text().trimmed()
            if dns.isEmpty() or dns.isNull():
                InfoHintDialog(self.tr("DNS is empty")).exec_()
                return False
            
            pattern = '^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$'
            matchObj = re.match(pattern, str(dns))
            if matchObj is None:
                InfoHintDialog(self.tr("DNS is wrong, please input again")).exec_()
                self.dns.setFocus()
                return False
            
            if backupDns:
                matchObj = re.match(pattern, str(backupDns))
                if matchObj is None:
                    InfoHintDialog(self.tr("Backup DNS is wrong, please input again")).exec_()
                    self.backupDns.setFocus()
                    return False
            return True
        else:
            return True
        
    def slotSettingDNSType(self, status):
        if status == Qt.Checked:
            self.dnsServerAddressGroupbox.setChecked(False)
        elif status == Qt.Unchecked:
            self.dnsServerAddressGroupbox.setChecked(True)
            
    def slotSettingCustomDNSType(self, status):
        if status:
            self.autoGetDNSCheckBox.setChecked(False)
        else:
            self.autoGetDNSCheckBox.setChecked(True)
        
    def slotSettingDHCPType(self, status):
        if status == Qt.Checked:
            self.staticIpGroupbox.setChecked(False)
        elif status == Qt.Unchecked:
            self.staticIpGroupbox.setChecked(True)
            
            
    def slotSettingStaticType(self, status):
        if status:
            self.autoGetIpCheckbox.setChecked(False)
        else:
            self.autoGetIpCheckbox.setChecked(True)
        
    def setDynamicNetwork(self):
        """设置动态网络的信息到配置文件"""
        # delCmd = "sed -i '/BOOTPROTO/,$'d %s" % self.networkconfigFile
        delCmd = "echo '' > %s" % self.networkconfigFile
        delBrCmd = "echo '' > %s" % self.bridgeNetworkconfigFile
        delOk = os.system(delCmd)
        delOkB = os.system(delBrCmd)
        #return
        deviceName = self.networkconfigFile.split("/")[-1].split("-")[-1]
        macValue = globalfunc.getMacByEthName(deviceName)
        content = None

        #eth0
        
        contenteth = "BOOTPROTO=none\\nDEVICE=%s\\nHWADDR=%s\\nNM_CONTROLLED=no\\nONBOOT=yes\\nBRIDGE=br0" % (deviceName, macValue)
            
            
        #如果是指定DNS地址
        if self.dnsServerAddressGroupbox.isChecked():
            dns = str(self.dns.text().trimmed())
            backupDns = str(self.backupDns.text().trimmed())
         
            if not backupDns:
                content = "BOOTPROTO=dhcp\\nDEVICE=br0\\nNM_CONTROLLED=no\\nONBOOT=yes\\nTYPE=Bridge\\nPEERNTP=yes\\ncheck_link_down(){\\n    return 1; \\n}\\nDNS1=%s" % (dns)
                                   
            else:
                content = "BOOTPROTO=dhcp\\nDEVICE=br0\\NM_CONTROLLED=no\\nONBOOT=yes\\nTYPE=Bridge\\nPEERNTP=yes\\ncheck_link_down(){\\n    return 1; \\n}\\nDNS1=%s\\nDNS2=%s" % (dns,backupDns) 
                                    
        else:
            content = "BOOTPROTO=dhcp\\nDEVICE=br0\\nNM_CONTROLLED=no\\nONBOOT=yes\\nTYPE=Bridge\\nPEERNTP=yes\\ncheck_link_down(){\\n    return 1; \\n}" 
                                    
        
        addEthCmd = "sed -i '$ a\\%s' %s" % (contenteth, self.networkconfigFile)
        addCmd = "sed -i '$ a\\%s' %s" % (content, self.bridgeNetworkconfigFile)
        
        
        # addCmd = "echo %s > %s" % (content, self.networkconfigFile)
        addOk = os.system(addCmd)
        addE = os.system(addEthCmd)
        if delOk != 0 or addOk != 0 or delOkB != 0 or addE != 0:
            InfoHintDialog(self.tr("Auto get IP failed")).exec_()
            return False
        
        return True
            
    def setStaticNetwork(self):
        """设置静态网络的信息到配置文件"""
        # delCmd = "sed -i '/BOOTPROTO/,$'d %s" % self.networkconfigFile
        delCmd = "echo \"\" > %s" % self.networkconfigFile
        delOk = os.system(delCmd)
        
        delCmdBr = "echo \"\" > %s" % self.bridgeNetworkconfigFile
        delOkBr = os.system(delCmdBr)
        
        IPADDR = str(self.ip.text().trimmed())
        NETMASK = str(self.netmast.text().trimmed())
        GATEWAY = str(self.defaultGateway.text().trimmed())
        
        deviceName = self.networkconfigFile.split("/")[-1].split("-")[-1]
        macValue = globalfunc.getMacByEthName(deviceName)
        
        #eth0
        contenteth = "BOOTPROTO=none\\nDEVICE=%s\\nHWADDR=%s\\nNM_CONTROLLED=no\\nONBOOT=yes\\nBRIDGE=br0" % (deviceName, macValue)
        content = None
        
        if not GATEWAY:
            content = "BOOTPROTO=static\\nDEVICE=br0\\nTYPE=Bridge\\nNM_CONTROLLED=no\\nIPADDR=%s\\nNETMASK=%s" % (IPADDR, NETMASK)
        else:
            content = "BOOTPROTO=static\\nDEVICE=br0\\nTYPE=Bridge\\nNM_CONTROLLED=no\\nIPADDR=%s\\nNETMASK=%s\\nGATEWAY=%s" % (IPADDR, NETMASK, GATEWAY)

        #如果是指定DNS地址
        if self.dnsServerAddressGroupbox.isChecked():
            dns = str(self.dns.text().trimmed())
            backupDns = str(self.backupDns.text().trimmed())
         
            if not backupDns:
                content = "%s\\nDNS1=%s" % (content, dns)
            else:
                content = "%s\\nDNS1=%s\\nDNS2=%s" % (content, dns, backupDns)
        
        addCmdEth = "sed -i '$ a\\%s' %s" % (contenteth, self.networkconfigFile)
        addCmdBr = "sed -i '$ a\\%s' %s" % (content, self.bridgeNetworkconfigFile)
        # addCmd = "echo %s > %s" % (content, self.networkconfigFile)
        addOk = os.system(addCmdEth)
        addOkBr = os.system(addCmdBr)
        if delOk != 0 and addOk != 0 and delOkBr != 0 and addOkBr != 0:
            InfoHintDialog(self.tr("Setting static IP failed")).exec_()
            return False
        
        return True
         
        
        
