# -*- coding: utf-8 -*-  

from PyQt4.QtCore import QObject
import os
from configFileParser import ConfigFileParser
import common
import globalvariable
import globalfunc
from logrecord import LogRecord

class StoreInfoParser(QObject):
    _instance = 0 
    def __init__(self):
        super(StoreInfoParser,self).__init__()

        # #配置文件挂载目录
        self.configFilePath = common.CONFIG_PATH

        if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:
            mountPath = globalfunc.convertPathToConfigPath(common.CONFIG_PATH)

            if not os.path.exists(self.configFilePath):
                os.system("mkdir -p %s" % os.path.dirname(self.configFilePath))
                os.mknod(self.configFilePath)


            if not os.path.isfile(mountPath):
                os.system("mkdir -p %s" % os.path.dirname(mountPath))
                os.mknod(mountPath)

        self.parser = ConfigFileParser().instance()



        
    @classmethod 
    def instance(cls):
        if (cls._instance == 0):
            cls._instance = StoreInfoParser()
            
        return cls._instance

    def changeConfigFile(self, section, option, value):
        if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:
            globalfunc.umountFile(self.configFilePath)

        if self.parser.has_section(section):
            if self.parser.has_option(section, option):
                localvalue = self.parser.getValue(section, option) 
                if localvalue == value: 
                    pass 
                else: 
                    self.parser.changeSectionValue(section, option, value)
                     
            else:
                self.parser.addOption(section, option, value)
        else:
            self.parser.addSection(section, option, value)

        if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:
            globalfunc.mountFile(self.configFilePath)


    def getCloudsServerIP(self):
        if self.parser.has_section("cloudsServerAddress"):
            if self.parser.has_option("cloudsServerAddress", "ip"):
                return self.parser.getValue("cloudsServerAddress", "ip")
            
        return None
    
    def getBackupServerAddress(self):
        if self.parser.has_section("cloudsServerAddress"):
            if self.parser.has_option("cloudsServerAddress", "ipbackup"):
                return self.parser.getValue("cloudsServerAddress", "ipbackup")
            
        return None
    
    def setServerAddress(self, serverIp):
        #保存服务器地址到配置文件
        self.changeConfigFile("cloudsServerAddress", "ip", serverIp)

            
    def setBackUpServerAddress(self, backupServerIp):
        #保存服务器地址到配置文件
        self.changeConfigFile("cloudsServerAddress", "ipbackup", backupServerIp)

        
    def setTerminalName(self, terminalName):
        #保存终端名称到配置文件
        self.changeConfigFile("terminalName", "name", terminalName)
            
            
    def getTerminalName(self):
        if self.parser.has_section("terminalName"):
            if self.parser.has_option("terminalName", "name"):
                return self.parser.getValue("terminalName", "name")
            
        return None
    def setTerminalMac(self, terminalMac):
        #保存终端名称到配置文件
        self.changeConfigFile("terminalMac", "mac", terminalMac)
            
            
    def getTerminalMac(self):
        if self.parser.has_section("terminalMac"):
            if self.parser.has_option("terminalMac", "mac"):
                return self.parser.getValue("terminalMac", "mac")
            
        return None
 
    def setDNSStatus(self, DNSStatus):
        #保存终端名称到配置文件
        self.changeConfigFile("DNSStatus", "DNSStatus", DNSStatus)
            
            
    def getDNSStatus(self):
        if self.parser.has_section("DNSStatus"):
            if self.parser.has_option("DNSStatus", "DNSStatus"):
                return self.parser.getValue("DNSStatus", "DNSStatus")
            
        return None
    
    def setTerminalType(self, terminalType):
        self.changeConfigFile("terminalType", "type", terminalType)
            
    
    def getTerminalType(self):
        if self.parser.has_section("terminalType"):
            if self.parser.has_option("terminalType", "type"):
                return self.parser.getValue("terminalType", "type")
            
        return None
    
    def setUsbState(self, stateValue):
        self.changeConfigFile("USBState", "usb_status", stateValue)

            
    def getUsbState(self):
        if self.parser.has_section("USBState"):
            if self.parser.has_option("USBState", "usb_status"):
                return self.parser.getValue("USBState", "usb_status")
            
        return None
    
    def setNetState(self, stateValue):
        self.changeConfigFile("NETState", "net_status", stateValue)

            
    def getNetState(self):
        if self.parser.has_section("NETState"):
            if self.parser.has_option("NETState", "net_status"):
                return self.parser.getValue("NETState", "net_status")
            
        return None

    def moveAwayGtkmo(self):
	if os.path.exists("/usr/share/locale/en_US/LC_MESSAGES/gtk20.mo"):
	    moveawaycmd = "mv /usr/share/locale/en_US/LC_MESSAGES/gtk20.mo /usr/share/locale/en_US/LC_MESSAGES/gtk20-bak.mo"
	    os.system(moveawaycmd)
    def moveBackGtkmo(self):
	if os.path.exists("/usr/share/locale/en_US/LC_MESSAGES/gtk20-bak.mo"):
	    movebackcmd = "mv /usr/share/locale/en_US/LC_MESSAGES/gtk20-bak.mo /usr/share/locale/en_US/LC_MESSAGES/gtk20.mo"
    	    os.system(movebackcmd)
    def setLanguage(self, language):
        self.changeConfigFile("Language", "language", language)
	if language == "english":
	    self.moveAwayGtkmo()
	else:
	    self.moveBackGtkmo()

            
    def getLanguage(self):
        if self.parser.has_section("Language"):
            if self.parser.has_option("Language", "language"):
                return self.parser.getValue("Language", "language")
            
        return "chinese"
    
    def setResolutionValue(self, resolutionValue):
        self.changeConfigFile("SCREEN_RESOLUTION", "resolution", resolutionValue)
  
    
    def getResolutionValue(self):
        if self.parser.has_section("SCREEN_RESOLUTION"):
            if self.parser.has_option("SCREEN_RESOLUTION", "resolution"):
                return self.parser.getValue("SCREEN_RESOLUTION", "resolution")
        return None
    
    def setVmType(self, vmType):
        self.changeConfigFile("VMTYPE", "vmtype", vmType)
  
    
    def getVmType(self):
        if self.parser.has_section("VMTYPE"):
            if self.parser.has_option("VMTYPE", "vmtype"):
                return self.parser.getValue("VMTYPE", "vmtype")
        return None
    
    def setLicense(self, license):
        self.changeConfigFile("LICENSE", "license", license)
  
    def getLicense(self):
        if self.parser.has_section("LICENSE"):
            if self.parser.has_option("LICENSE", "license"):
                return self.parser.getValue("LICENSE", "license")
        return None
    
    def setLessonList(self, lessenlist):
        self.changeConfigFile("LESSENLIST", "lessenlist", lessenlist)
  
    def getLessonList(self):
        if self.parser.has_section("LESSENLIST"):
            if self.parser.has_option("LESSENLIST", "lessenlist"):
                return self.parser.getValue("LESSENLIST", "lessenlist")
        return None
    
    def setOffLessonList(self, offlessenlist):
        self.changeConfigFile("OFFLESSENLIST", "offlessenlist", offlessenlist)
  
    def getOffLessonList(self):
        if self.parser.has_section("OFFLESSENLIST"):
            if self.parser.has_option("OFFLESSENLIST", "offlessenlist"):
                return self.parser.getValue("OFFLESSENLIST", "offlessenlist")
        return None
    
    
    def setVolumeValue(self, volumeValue):
        self.changeConfigFile("VOLUME", "value", volumeValue)


    def getVolumeValue(self):
        if self.parser.has_section("VOLUME"):
            if self.parser.has_option("VOLUME", "value"):
                return self.parser.getValue("VOLUME", "value")
            else:
                self.parser.addOption("VOLUME", "value", "100%")
                return "100%"
        else:
            self.parser.addSection("VOLUME", "value", "100%")
            return "100%"
