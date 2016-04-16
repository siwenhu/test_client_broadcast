# -*- coding: utf-8 -*-  

import uuid
import socket
import fcntl
import struct
import common
import os
import commands
from logrecord import LogRecord
from PyQt4.QtCore import QString
import globalvariable
from ctypes import *
#import json

#CDLL("../lib/libjson-c.so", mode=RTLD_GLOBAL)
#jytcapi = cdll.LoadLibrary('../lib/libjytcapi.so')
#jytcapi.jyinittcapi()

def setVolumeTerminal():
    jytcapi.jysetvolume("micVolume=100&playVolume=100")

def setScreenResolution(screenvalue):
    current = getCurrentScreenResolution()
    if current == screenvalue:
        return True
    else:
        jytcapi.jysetdispconf(str(screenvalue))
        return True
def shutdownTerminal():
    jytcapi.jyshutdown()
#得到本机的MAC地址
def get_mac_address():
    from storeinfoparser import StoreInfoParser 
    terminalMac = StoreInfoParser.instance().getTerminalMac()
    if terminalMac == "aa:bb:cc:dd:ee:ff" or terminalMac == None:
        pass
    else:
       return terminalMac

    mymac = ["aa","bb","cc","dd","ee","ff"]
    value = getCmdExecValueT("../lib/ccr_jytcapi sysinfo")
    for i in range(len(value)):
       if len(value[i].split(":"))==7 and value[i].split(":")[0]=="wiredMac":
            mymac = value[i].split(":")[1:7]
            break   
    StoreInfoParser.instance().setTerminalMac(":".join(mymac))
    return ":".join(mymac)

def get_cpu_info():
    cpu_info = "aa"
    value = getCmdExecValueT("../lib/ccr_jytcapi sysinfo")
    for i in range(len(value)):
       if len(value[i].split(":"))==2 and value[i].split(":")[0]=="cpuInfo":
            cpu_info = value[i].split(":")[1]
            break   
    return cpu_info 
def get_disk_size():
    disk_size = "1"
    value = getCmdExecValueT("../lib/ccr_jytcapi sysinfo")
    for i in range(len(value)):
       if value[i].split(":")[0]=="hardCap" and len(value[i].split(":")) == 2:
            disk_size = value[i].split(":")[1]
            break   
    return disk_size

def getNetInfo():
    netList = ["0.0.0.0","255.255.255.0","1.1.1.1", "dhcp", "dhcp", "0.0.0.0", "0.0.0.0"]

    networkInfo = getCmdExecValueT("../lib/ccr_jytcapi network")
    for item in networkInfo:
        if len(item.split(":")) == 2:
            if item.split(":")[0] == "ip":
                netList[0] = item.split(":")[1] 
            elif item.split(":")[0] == "mask": 
                netList[1] = item.split(":")[1] 
            elif item.split(":")[0] == "gateway":
                netList[2] = item.split(":")[1]
            elif item.split(":")[0] == "conf":
                if item.split(":")[1] == "0": 
                    netList[3] = "dhcp"
                else:   
                    netList[3] = "static"
            elif item.split(":")[0] == "dns1": 
                netList[4] = "static"
                netList[5] = item.split(":")[1]
            elif item.split(":")[0] == "dns2":
                netList[6] = item.split(":")[1]
    LogRecord.instance().logger.info(netList)
    return netList

def getNetDnsType():
    typeList = ["dhcp","dhcp"]
    networkInfo = getCmdExecValueT("../lib/ccr_jytcapi network")
    for item in networkInfo:
        if len(item.split(":")) == 2:
            if item.split(":")[0] == "conf": 
                if item.split(":")[1] == "0": 
                    typeList[0] = "dhcp"
                else:   
                    typeList[0] = "static"
            elif item.split(":")[0] == "dns1": 
                typeList[1] = "static"
            else:
                pass
    return typeList

def getNetStatic():
    netList = ["0.0.0.0","255.255.255.0","1.1.1.1"]
    networkInfo = getCmdExecValueT("../lib/ccr_jytcapi network")
    for item in networkInfo:
        if len(item.split(":")) == 2:
            if item.split(":")[0] == "ip":
                netList[0] = item.split(":")[1] 
            elif item.split(":")[0] == "mask": 
                netList[1] = item.split(":")[1] 
            elif item.split(":")[0] == "gateway":
                netList[2] = item.split(":")[1]
    return netList
def getDnsStatic():
    dnsList = ["0.0.0.0","0.0.0.0"]
    networkInfo = getCmdExecValueT("../lib/ccr_jytcapi network")
    for item in networkInfo:
        if len(item.split(":")) == 2:
            if item.split(":")[0] == "dns1":
                dnsList[0] = item.split(":")[1]
            elif item.split(":")[0] == "dns2":
                dnsList[1] = item.split(":")[1]
    return dnsList

#得到网卡的名称
def getEthNameList():
    ethList = []
    commandsOutput = commands.getstatusoutput("ls /sys/class/net/")
    if commandsOutput[0] == 0:
        ethList = [name for name in commandsOutput[1].split("\n") if name != "lo" and name != "virbr0" and name != "br0"]
    return ethList

#根据网卡名称活动相应的MAC值
def getMacByEthName(ethName):
    macValue = None
    commandsOutput = commands.getstatusoutput("cat /sys/class/net/%s/address" % ethName)
    if commandsOutput[0] == 0:
        macValue = commandsOutput[1]
        return macValue
    return macValue

#得到本机的IP地址
def get_ip_address():
    staticlist = getNetStatic()   
    return staticlist[0] 


#获取本机网关
def get_netmask_gateway_dns():
    staticlist = getNetStatic()
    netmask = staticlist[1]
    gateway = staticlist[2]
    dnslist = getDnsStatic()
    DNS_first = dnslist[0]
    return [netmask, gateway, DNS_first]

#获取本机网络类型
def get_network_type():
    typelist = getNetDnsType()
    return typelist[0]

# #把课程信息转换为创建虚拟机的参数信息
# def lessonInfoConvertToParamInfo(lsInfo):
#     paramInfo = {}
#     terminalName = StoreInfoParser.instance().getTerminalName()
#     paramInfo["configure"] = "standard"
#     paramInfo["cpus"] = lsInfo["cpu_cores"]
#     paramInfo["memory"] = lsInfo["memory"]
#     paramInfo["disk"] = lsInfo["disk"]
#     paramInfo["name"] = terminalName + lsInfo["name"]
#     paramInfo["os"] = lsInfo["cdrom"].split("/")[-1]
#     paramInfo["iso_path"] = lsInfo["cdrom"]
#     paramInfo["course_flag"] = '0'
#     paramInfo["use_flag"] = True
#     return paramInfo
    
#根据虚拟机的名称从虚拟机列表中找到该名称的虚拟机所有信息
def getVMInfoFromVMS(vmsInfoList, name):
    vmInfo = {}
    for subInfo in vmsInfoList:
        if subInfo["name"] == name:
            vmInfo = subInfo
            
    return vmInfo
    
#从云主机广播的信息中根据本机的MAC值来提取分配给该学生机的云桌面名称
def getVMCloudsNameFromBroadInfo(data):
    contentList = data.split("||")
    length = len(contentList)
    mac = get_mac_address()
    vmName = None
    for i in range(length):
        if contentList[i].split(",")[0] == mac:
            vmName = contentList[i].split(",")[1]
            break
        
    return vmName

#从云主机广播的信息中根据本机的MAC值来提取分配给该学生机的classid
def getInfoVMCloudsNameFromBroad(data):
    contentList = data.split("||")
    classid = None
    if len(contentList)>=2:
        cmd = contentList[0]
        classid = contentList[1]
    return classid
        
#设置计算机的名称
def setStuentPCName(pcName):
    cmdDelete = "sed -i /HOSTNAME/d /etc/sysconfig/network"
    cmdAppend = "sed -i '$ a\\HOSTNAME=%s' /etc/sysconfig/network" % pcName
    cmd = cmdDelete + "&&" + cmdAppend
    if os.system(cmd) != 0:
        return False
    
    return True
    
#获得版本号和版本日期
def getVersionAndReleaseDate():
    version = None
    rDate = None
    #if os.path.exists("/etc/default/version"):
    if os.path.exists("/opt/ccr-student/cfg/version"):
        #statusOutput = commands.getstatusoutput("cat /etc/default/version")
        statusOutput = commands.getstatusoutput("cat /opt/ccr-student/cfg/version")
        if statusOutput[0] == 0:
            outputList = QString(statusOutput[1]).split("\n")
            for value in outputList:
                if value.split("=")[0] == "VERSION":
                    version = value.split("=")[1]
                if value.split("=")[0] == "BUILD_DATE":
                    rDate = value.split("=")[1]
                    
    return version, rDate
                    
#修改计算机名称到系统配置文件
# def changePCMName(pcName):
#     cmdDelete = "sed -i /HOSTNAME/d /etc/sysconfig/network"
#     cmdAppend = "sed -i '$ a\\HOSTNAME=%s' /etc/sysconfig/network" % pcName
#     cmd = cmdDelete + "&&" + cmdAppend
#     if os.system(cmd) != 0:
#         return False
#     return True
def getCurrentScreenResolution():
    currentSolution = "10"
    reSolution = "auto"
    solutionMap = {"0":"800x600","1":"1024x768","2":"1280x720","3":"1440x900","4":"1600x1020","5":"1920x1080","6":"1280x1024","7":"1366x768","8":"1600x900","10":"auto"}
    cmd = "../lib/ccr_jytcapi current_display"
    errorFlg = True 
    while errorFlg:
        try: 
            value =  getCmdExecValueT(cmd)
            errorFlg = False
        except: 
            errorFlg = True 
        
    for i in range(len(value)):
        LogRecord.instance().logger.info("#".join(value))
        if len(value[i].split(":"))==2 and value[i].split(":")[0]=="res" and value[i].split(":")[1] !="auto":
            currentSolution = value[i].split(":")[1]
            break   
    if solutionMap.has_key(currentSolution):
        reSolution = solutionMap[currentSolution]
    if reSolution == "auto":
        LogRecord.instance().logger.info("resolution is auto")
        reSolution = getGdkResolution()

    return reSolution

def getGdkResolution():
    import gtk.gdk
    LogRecord.instance().logger.info("getGdkResolution in")
    resolution = "1024x768"
    w = gtk.gdk.get_default_root_window()
    sz = w.get_size() #(1440,900)
    if len(sz) == 2:
        LogRecord.instance().logger.info(str(sz[0]))
        LogRecord.instance().logger.info(str(sz[1]))
        resolution = str(sz[0]) + "x" + str(sz[1])

    return resolution 

def getCmdExecValueT(cmd):
    """得到命令执行的结果""" 
    statusOutput = commands.getstatusoutput(cmd)
    monitorList = statusOutput[1].split("\n")
    return monitorList
#得到当前屏幕支持的分辨率列表
def getScreenResolution():
    """得到屏幕支持的分辨率"""
    #获得显示器名称，连接状态及行号
    Monitors = getCmdExecValueT("../lib/ccr_jytcapi display")

    #根据组合列表把显示器名称和支持的分辨率放入到一个字典中
    resolutionMap = {}
    resolutionList = []
    count = len(Monitors)
    for i in range(count):
         if len(Monitors[i].split(":")) < 2:
             continue
         valueName = Monitors[i].split(":")[0]
         valueValue = Monitors[i].split(":")[1]

         if valueName == "value":
             resolutionList.append[valueValue]
    
    resolutionMap["monitorName"] = resolutionList

    return resolutionMap

def setUbuntuDynamicNetwork():
    """设置动态网络的信息到配置文件"""
    pass 
def setUbuntuStaticNetwork(params):
    """设置静态网络的信息到配置文件"""
    pass
def setJyDynamicNetwork():
    """设置动态网络的信息到配置文件""" 
    netconf="conf=0&ip=&mask=&gateway=&dns1=&dns2="
    return netconf 

def setJyStaticNetwork(params):
    """设置静态网络的信息到配置文件"""
    IPADDR = params[1].strip()
    NETMASK = params[2].strip()
    if len(IPADDR) == 0 or len(NETMASK) == 0:
        return "False" 
    GATEWAY = params[3].strip()
    DNS = params[4].strip()

    netconf="conf=1&ip=%s&mask=%s&gateway=%s&dns1=%s&dns2=" %(IPADDR,NETMASK,GATEWAY,DNS)
    return netconf

def setDynamicNetwork():
    """设置动态网络的信息到配置文件"""
    if QString(getLinuxOperationSystemType()).contains("Ubuntu"):
        return setUbuntuDynamicNetwork()
		
    if not os.path.exists("/etc/sysconfig/network-scripts/"):
        os.system("mkdir -p /etc/sysconfig/network-scripts")
    if not os.path.exists("/etc/sysconfig/network-scripts/ifcfg-br0"):
        os.mknod("/etc/sysconfig/network-scripts/ifcfg-br0")
        
    #delBrCmd = "sed -i '/BOOTPROTO/,$'d /etc/sysconfig/network-scripts/ifcfg-br0"
    delBrCmd = "echo > /etc/sysconfig/network-scripts/ifcfg-br0"
    #content = "BOOTPROTO=dhcp"
    content = "BOOTPROTO=dhcp\\nDEVICE=br0\\nONBOOT=yes\\nTYPE=Bridge\\nPEERNTP=yes\\ncheck_link_down(){\\n    return 1; \\n}"
    #addCmd = "sed -i '$ a\\%s' /etc/sysconfig/network-scripts/ifcfg-%s" % (content, ethNameList[0])
    addCmd = "sed -i '$ a\\%s' /etc/sysconfig/network-scripts/ifcfg-br0" % (content)
    delOk = os.system(delBrCmd)
    addOk = os.system(addCmd)
    
    os.system(str("persist /etc/sysconfig/network-scripts/ifcfg-br0"))

    if delOk != 0 or addOk != 0:
        return False

    return True

def setStaticNetwork(params):
    """设置静态网络的信息到配置文件"""
    if QString(getLinuxOperationSystemType()).contains("Ubuntu"):
        return setUbuntuStaticNetwork(params)
    if not os.path.exists("/etc/sysconfig/network-scripts/"):
        os.system("mkdir -p /etc/sysconfig/network-scripts")
    if not os.path.exists("/etc/sysconfig/network-scripts/ifcfg-br0"):
        os.mknod("/etc/sysconfig/network-scripts/ifcfg-br0")
    #delCmd = "sed -i '/BOOTPROTO/,$'d /config/etc/sysconfig/network-scripts/ifcfg-%s" % ethNameList[0]
    #delCmd = "sed -i '/BOOTPROTO/,$'d /etc/sysconfig/network-scripts/ifcfg-br0"
    delCmd = "echo > /etc/sysconfig/network-scripts/ifcfg-br0"
    IPADDR = params[1].strip()
    NETMASK = params[2].strip()

    if len(IPADDR) == 0 or len(NETMASK) == 0:
        return False

    GATEWAY = params[3].strip()
    DNS = params[4].strip()

    content = None
    delOk = os.system(delCmd)
    
    if GATEWAY:
        content = "DEVICE=br0\\nONBOOT=yes\\nTYPE=Bridge\\nBOOTPROTO=static\\nIPADDR=%s\\nNETMASK=%s\\nGATEWAY=%s" % (IPADDR, NETMASK, GATEWAY)
    else:
        content = "DEVICE=br0\\nONBOOT=yes\\nTYPE=Bridge\\nBOOTPROTO=static\\nIPADDR=%s\\nNETMASK=%s" % (IPADDR, NETMASK)

    if DNS:
        content = "%s\\nDNS1=%s" % (content, DNS)

    #addCmd = "sed -i '$ a\\%s' /config/etc/sysconfig/network-scripts/ifcfg-%s" % (content, ethNameList[0])
    addCmd = "sed -i '$ a\\%s' /etc/sysconfig/network-scripts/ifcfg-br0" % (content)
    addOk = os.system(addCmd)
    
    os.system(str("persist /etc/sysconfig/network-scripts/ifcfg-br0"))

    if delOk != 0 and addOk != 0:
        return False

    return True

def getLinuxOperationSystemType():
    """得到linux操作系统的类型"""
    statusOutput = commands.getstatusoutput("head -n 1 /etc/issue")
    LogRecord.instance().logger.info(u"/etc/issue文件内容：%s" % statusOutput[1])
    if statusOutput[0] == 0:
        output = QString(statusOutput[1])
        if output.contains("Ubuntu 12.04"):
            return "Ubuntu 12.04"
        if output.contains("Ubuntu 13.04"):
            return "Ubuntu 13.04"
        elif output.contains("CentOS release 6.5"):
            return "CentOS 6.5"
        elif output.contains("CentOS release 7.0"):
            return "CentOS 7.0"
        elif output.contains("Ubuntu 14.04"):
            return "Ubuntu 14.04"
        elif output.contains("Ubuntu"):
            return "Ubuntu"
        elif output.contains("MCOS-cClassroom-student"):
            return "CentOS 7.0"
        elif output.contains("CentOS"):
            return "CentOS"

    return None


def getProgramRunningEnvType():
    """判断程序执行的环境类型"""
    if os.path.exists("/config"):
        return common.DEVELOPED_ENV_TYPE
        #return common.OPERATION_ENV_TYPE
    else:
        return common.DEVELOPED_ENV_TYPE


def convertPathToVarPath(localPath):
    """转换路径到/var类型下的路径"""
    return localPath

def convertPathToConfigPath(localPath):
    """转换路径到/config类型下的路径"""
    if localPath.startswith("/usr"):
        return localPath.replace("/usr", "/config/usr")
    elif localPath.startswith("/etc"):
        return localPath.replace("/etc", "/config/etc")


def umountFile(filePath):
    if os.system("umount %s" % filePath) != 0:
        LogRecord.instance().logger.info(u"卸载配置文件失败，文件路径:%s" % filePath)

def mountFile(filePath):
    mountPath = convertPathToConfigPath(filePath)
    if os.system("mount --bind %s %s" % (mountPath, filePath)) != 0:
        LogRecord.instance().logger.info(u"挂载配置文件失败，挂载路径:%s, 配置文件路径:%s" % (mountPath, filePath))
        
        

# content = "BOOTPROTO=dhcp\\nDEVICE=br0\\nONBOOT=yes\\nTYPE=Bridge\\nPEERNTP=yes\\ncheck_link_down(){\\n    return 1; \\n}"
# addCmd = "sed -i '$ a\\%s' /root/a" % (content)
# addOk = os.system(addCmd)
