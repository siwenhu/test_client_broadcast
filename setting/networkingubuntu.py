# -*- coding: utf-8 -*-
from storeinfoparser import StoreInfoParser
from PyQt4.QtCore import Qt, SIGNAL, QString, QTranslator, QCoreApplication
from PyQt4.QtGui import QWidget, QLabel, QLineEdit, QGridLayout, QVBoxLayout, QGroupBox, QCheckBox,\
                        QHBoxLayout, QPushButton, QMessageBox
import os
import re
from base.infohintdialog import InfoHintDialog
from restartnetworkthread import RestartNetworkThread
import commands
import common
import json
from ctypes import *
from logrecord import LogRecord

class NetWorkSettingWidget(QWidget):

    def __init__(self, app, parent = None):
        super(NetWorkSettingWidget,self).__init__(parent)
        self.setStyleSheet("font-size : 16px;")
        self.app = app
        CDLL("../lib/libjson-c.so", mode=RTLD_GLOBAL)
        self.jytcapi = cdll.LoadLibrary('../lib/libjytcapi.so')
        self.jytcapi.jyinittcapi()
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

        if self.autoGetIpCheckbox.isChecked():
            netconf = self.setDynamicNetwork()
        elif self.staticIpGroupbox.isChecked():
            netconf = self.setStaticNetwork()

        #重新启动网络
        self.restartNetworkTD.setNetConf(netconf)
        self.restartNetworkTD.start()

        return

    def getCmdExecValueT(self, cmd):
        """得到命令执行的结果"""
        statusOutput = commands.getstatusoutput(cmd)
        monitorList = statusOutput[1].split("\n")
        return monitorList

    def getNetDnsType(self):
        typeList = ["dhcp","dhcp"]
        networkInfo = self.getCmdExecValueT("../lib/ccr_jytcapi network")
        for item in networkInfo:
            if len(item.split(":")) == 2:
                if item.split(":")[0] == "conf":
                    if item.split(":")[1] == "0":
                        typeList[0] = "dhcp"
                    else:
                        typeList[0] = "static"
                else:
                    pass
        DNSStatus = StoreInfoParser.instance().getDNSStatus()
        if DNSStatus == None:
            pass
        else:
            typeList[1] = DNSStatus
        return typeList

    def getNetStatic(self):
        netList = ["0.0.0.0","255.255.255.0","1.1.1.1"]
        networkInfo = self.getCmdExecValueT("../lib/ccr_jytcapi network")
        for item in networkInfo:
            if len(item.split(":")) == 2:
                if item.split(":")[0] == "ip":
                    netList[0] = item.split(":")[1] 
                elif item.split(":")[0] == "mask":
                    netList[1] = item.split(":")[1] 
                elif item.split(":")[0] == "gateway":
                    netList[2] = item.split(":")[1] 
        return netList

    def getDnsStatic(self):
        dnsList = ["0.0.0.0","2.5.5.0"]
        networkInfo = self.getCmdExecValueT("../lib/ccr_jytcapi network")
        for item in networkInfo:
            if len(item.split(":")) == 2:
                if item.split(":")[0] == "dns1":
                    dnsList[0] = item.split(":")[1] 
                elif item.split(":")[0] == "dns2":
                    dnsList[1] = item.split(":")[1] 
        return dnsList


    def initCheckBoxStatus(self):
        """读取网络配置文件，初始化相应的checkbox的状态"""
        [netType, DNSType] = self.getNetDnsType()
        if netType == "dhcp":
            self.autoGetIpCheckbox.setChecked(True)
            self.staticIpGroupbox.setChecked(False)
            self.autoGetDNSCheckBox.setEnabled(False)
            self.dnsServerAddressGroupbox.setEnabled(False)
        else:
            self.autoGetIpCheckbox.setChecked(False)
            self.staticIpGroupbox.setChecked(True)
            self.autoGetDNSCheckBox.setEnabled(True)
            self.dnsServerAddressGroupbox.setEnabled(True)
            [ip, netmask, gateway] = self.getNetStatic()
            if ip:
                self.ip.setText(ip)

            if netmask:
                self.netmast.setText(netmask)

            if gateway:
                self.defaultGateway.setText(gateway)


        if DNSType == "dhcp":
            self.autoGetDNSCheckBox.setChecked(True)
            self.dnsServerAddressGroupbox.setChecked(False)
        else:
            self.autoGetDNSCheckBox.setChecked(False)
            self.dnsServerAddressGroupbox.setChecked(True)
            [DNS_first, DNS_second] = self.getDnsStatic()
            if DNS_first:
                self.dns.setText(DNS_first)

            if DNS_second:
                self.backupDns.setText(DNS_second)


    def getCustomDNSInfo(self):
        """得到自定义DNS的内容"""
        DNS_first = None
        DNS_second = None
        statusOutput = commands.getstatusoutput("cat %s" % common.NETWORK_CONFIG_UBUNTU)
        if statusOutput[0] == 0:
            outputList = QString(statusOutput[1]).split("\n")
            for value in outputList:
                if value.split(" ")[0] == "dns-nameservers":
                    DNS_first = value.split(" ")[1]
                    if len(value.split(" ")) > 2:
                        DNS_second = value.split(" ")[2]

        return [DNS_first, DNS_second]


    def getStaticNetworkInfo(self):
        """得到静态网络的信息"""
        ip = netmask = gateway = None
        statusOutput = commands.getstatusoutput("cat %s" % common.NETWORK_CONFIG_UBUNTU)
        if statusOutput[0] == 0:
            outputList = QString(statusOutput[1]).split("\n")
            for value in outputList:
                if value.split(" ")[0] == "address":
                    ip = value.split(" ")[1]
                elif value.split(" ")[0] == "netmask":
                    netmask = value.split(" ")[1]
                elif value.split(" ")[0] == "gateway":
                    gateway = value.split(" ")[1]

        return [ip, netmask, gateway]

    def getNetworkType(self):
        """得到网络是静态还是动态类型"""
        netType = None
        DNSType = None
        statusOutput = commands.getstatusoutput("cat %s" % common.NETWORK_CONFIG_UBUNTU)
        if statusOutput[0] == 0:
            output = QString(statusOutput[1])
            if output.contains("dhcp"):
                netType = "dhcp"
            else:
                netType = "static"

            if output.contains("dns-nameservers"):
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
                InfoHintDialog(u'IP地址或子网掩码不能为空').exec_()
                return False

            pattern = '^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$'
            matchObj = re.match(pattern, ip)
            if matchObj is None:
                InfoHintDialog(u'IP地址格式有误，请重新填入').exec_()
                self.ip.setFocus()
                return False

            matchObj = re.match(pattern, str(netmask))
            if matchObj is None:
                InfoHintDialog(u'子网掩码地址格式有误，请重新填入').exec_()
                self.netmast.setFocus()
                return False

            if gateway:
                matchObj = re.match(pattern, str(gateway))
                if matchObj is None:
                    InfoHintDialog(u'网关地址格式有误，请重新填入').exec_()
                    self.netmast.setFocus()
                    return False

        return True

    def checkDnsInputValid(self):
        """检查DNS输入的内容的有效性"""
        if not self.autoGetDNSCheckBox.isChecked():
            dns = self.dns.text().trimmed()
            backupDns = self.backupDns.text().trimmed()
            if dns.isEmpty() or dns.isNull():
                InfoHintDialog(u'DNS不能为空').exec_()
                return False

            pattern = '^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$'
            matchObj = re.match(pattern, str(dns))
            if matchObj is None:
                InfoHintDialog(u'DNS地址格式有误，请重新填入').exec_()
                self.dns.setFocus()
                return False

            if backupDns:
                matchObj = re.match(pattern, str(backupDns))
                if matchObj is None:
                    InfoHintDialog(u'备用DNS地址格式有误，请重新填入').exec_()
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
            self.dnsServerAddressGroupbox.setChecked(False)
            self.autoGetDNSCheckBox.setChecked(True)
            self.autoGetDNSCheckBox.setEnabled(False)
            self.dnsServerAddressGroupbox.setEnabled(False)
        elif status == Qt.Unchecked:
            self.staticIpGroupbox.setChecked(True)
            self.dnsServerAddressGroupbox.setChecked(True)
            self.autoGetDNSCheckBox.setEnabled(True)
            self.autoGetDNSCheckBox.setChecked(False)
            self.dnsServerAddressGroupbox.setEnabled(True)



    def slotSettingStaticType(self, status):
        if status:
            self.autoGetIpCheckbox.setChecked(False)
            self.dnsServerAddressGroupbox.setChecked(True)
            self.autoGetDNSCheckBox.setEnabled(True)
            self.autoGetDNSCheckBox.setChecked(False)
            self.dnsServerAddressGroupbox.setEnabled(True)
        else:
            self.autoGetIpCheckbox.setChecked(True)
            self.dnsServerAddressGroupbox.setChecked(False)
            self.autoGetDNSCheckBox.setEnabled(False)
            self.autoGetDNSCheckBox.setChecked(True)
            self.dnsServerAddressGroupbox.setEnabled(False)
 

    def setDynamicNetwork(self):
        """设置动态网络的信息到配置文件"""
        netconf="conf=0&ip=&mask=&gateway="
        #如果是指定DNS地址
        if self.dnsServerAddressGroupbox.isChecked():
            dns = str(self.dns.text().trimmed())
            backupDns = str(self.backupDns.text().trimmed())
            if not backupDns:
                netconf = netconf + "&dns1=" + dns 
            else:
                netconf = netconf + "&dns1=" + dns + "&dns2=" + backupDns 
            StoreInfoParser.instance().setDNSStatus("static")
        else:
            netconf = netconf + "&dns1=&dns2=" 
            StoreInfoParser.instance().setDNSStatus("dhcp")
        return netconf 
    def setStaticNetwork(self):
        """设置静态网络的信息到配置文件"""

        IPADDR = str(self.ip.text().trimmed())
        NETMASK = str(self.netmast.text().trimmed())
        GATEWAY = str(self.defaultGateway.text().trimmed())
        content = None
        if not GATEWAY:
            content = "conf=1&ip=%s&mask=%s&gateway=" % (IPADDR, NETMASK)
        else:
            content = "conf=1&ip=%s&mask=%s&gateway=%s" % (IPADDR, NETMASK, GATEWAY)

        #如果是指定DNS地址
        if self.dnsServerAddressGroupbox.isChecked():
            dns = str(self.dns.text().trimmed())
            backupDns = str(self.backupDns.text().trimmed())
            if not backupDns:
                content = content + "&dns1=" + dns 
            else:
                content = content + "&dns1=" + dns + "&dns2=" + backupDns 
            StoreInfoParser.instance().setDNSStatus("static")
        else:
            content = content + "&dns1=&dns2="
            StoreInfoParser.instance().setDNSStatus("dhcp")
        return content 


