#coding:utf-8

'''
Created on Sep 4, 2014

@author: root
'''
from PyQt4.QtCore import QObject,SIGNAL,QTimer
from xml.etree import ElementTree as ET
import libvirt
import os
import time
import threading
import ctypes
import createshot
import socketrance
#from storeinfoparser import StoreInfoParser
from offvm import changename
from offvm import addsdl
from offvm.domstatusmonitor import DomStatusMonitor
from offvm.deleteimgthread import DeleteThread
from offvm.mountDiskThread import MountDiskThread
from storeinfoparser import StoreInfoParser
from offvm import addinterface
from offvm import adddisk
from offvm import pathfolder
from offvm.udev import Udev
from offvm import usbplug
from offvm import xmledit
from offvm import addserial
#from lxml.etree import ElementTree


XML_PATH = pathfolder.XML_PATH

DOM_STATE_MAP = {0: 'nostate',
                 1: 'running',
                 2: 'blocked',
                 3: 'paused',
                 4: 'shutdown',
                 5: 'shutoff',
                 6: 'crashed',
                 7: 'pmsuspended'}

stats = {}

class DomainManager(QObject):
    
    def __init__(self,parent=None):
        super(DomainManager,self).__init__(parent)
        self.conn = None
        self.status = {}
        self.dom = None
        self.usbmap = {}
        self.domainInfo = {}
    
    def getDom(self):
        return self.dom
    def getStatus(self):
        return self.status
    def setDomainInfo(self,domainInfo):
        self.domainInfo = domainInfo
    def getDomainInfo(self):
        return self.domainInfo
    
    def defineNetFilter(self,flag):
        
        if self.domainInfo == {}:
            cloudsip = "0.0.0.0"
        if self.domainInfo.has_key("cloud_ip"):
            cloudsip = self.domainInfo["cloud_ip"]
        else:
            cloudsip = None
        addinterface.defineNetworkFilter(flag, cloudsip)
        
    def createConnection(self):
        '''Open libvirt in read and write mode
        '''
        self.conn = libvirt.open("qemu:///system")
        if self.conn == None:
            msg = 'Failed to open connection to QEMU/KVM'
        else:
#             self.conn.setKeepAlive(5,3)
            msg = 'qemu:///system is created successfully'
        
    def closeConnection(self):
        '''Close current libvirt connection
        '''
        try:
            self.conn.close()
        except:
            return 1
        
    def getDomInfoByName(self,name):
        
        #name = self.domainInfo["name"]
        '''
        @param name: the name of the domain
        @type name: string
        '''
        
        myDom = None
        try:
            if self.conn == None:
                self.createConnection()
                
            myDom = self.conn.lookupByName(name)
        except:
            msg = 'Failed to find the domain with name "%s"' % name
        return myDom
    
    def getDomInfoByUUID(self, strUUID):
        '''
        @param strUUID: the uuid of domain
        @type strUUID: string
        @return: return a domain if success or 1
        '''
        myDom = None
        try:
            if self.conn == None:
                self.createConnection()
            myDom = self.conn.lookupByUUIDString(strUUID)
        except:
            msg =  'Failed to find the domain with UUID "%s"' %strUUID
           
        return myDom
    
    def defineDomainXml(self):
        """ 
        Get content of the xml from @path and define it to make it connected with the image
        @param path: the xml file path
        @type path: string
        """
        name = self.domainInfo["name"]
        vmname = self.domainInfo["vmname"]
        path = XML_PATH + name + ".xml"
        ret = os.path.exists(path)
        if ret is False:
            msg = (path+" is not found")
            return
        
        root = ET.parse(path).getroot()
        xml = ET.tostring(root, 'utf-8')
        if self.conn == None:
                self.createConnection()
        dom = self.getDomInfoByName(vmname)
        if dom == None:
            self.conn.defineXML(xml)
    def undefineDomain(self,name):
        
        #name = self.domainInfo["name"]
        if self.conn == None:
                self.createConnection()
                
        d = self.getDomInfoByName(name)
        myDom = self.getDomInfoByUUID(d.UUIDString())
        if myDom.isActive() == False:
            myDom.undefine()
        else:
            self.shutdownDomain()
            myDom.undefine()

    def startDomainByName(self):
        """ Start the domain. If not active, start it. 
        @param name: the name of virtual machine
        @type name: string
        """
        #edit xml
        #mount disk
        #create snapshot
        #define xml
        #start dom
        #start dommonitor
        imgname = ""
        name = ""
        dom = None
        localresolution = ""
        serverip = ""
        imgname = self.domainInfo["name"]
        name = self.domainInfo["vmname"]
        dom = self.getDomInfoByName(name)
        if dom != None:
            if dom.isActive():
                dom.destroy()
                dom.undefine()
            else:
                dom.undefine()
                #return
        
        ok = createshot.createSnapshot(imgname)
        if ok == 1:
            return
        self.editDomainXml()
        self.defineDomainXml()
        myDom = self.getDomInfoByName(name)
        #myDom = self.getDomInfoByUUID(d.UUIDString())
        myDom.create()
        #cmd = "virsh start " + name
        #os.system(str(cmd))
        
#         ret = self.mountDisk()
#         if ret:
#             pass 
#         else:
#             pass 
        
        localsolution = StoreInfoParser.instance().getResolutionValue()
        serverip = StoreInfoParser.instance().getCloudsServerIP()
        #name
        #type = "offline"
        #if localsolution != "" or len(localsolution.split("x"))
        socketstring = "serverip=" + serverip + "#guestname=" + name + "#resolution=" + localsolution
        if localsolution != "" and serverip != "" and name != "":
            writeStr = localsolution + "x"
            result = 1
            while result != 0:
                try:
                    socketrance.writeToSocket(socketstring)
                    result = 0
                except Exception as e:
                    pass 
                
                time.sleep(1)
        
        self.dom = myDom
        
        self.start_udev()
        
        self.domainMonitor = DomStatusMonitor()
        self.domainMonitor.setName(name)
        self.domainMonitor.start()
        self.connect(self.domainMonitor, SIGNAL("domainshutdown"),self.slotDomainStop)
        
        self.stateTimer = QTimer()
        self.stateTimer.start(5000)
        self.connect(self.stateTimer, SIGNAL("timeout()"),self.updateState)
        return myDom
        
    def start_udev(self):
        self.add_usb_first()
        self.udev = Udev()
        self.udev.monitor_async("usb", None, None)
        self.connect(self.udev, SIGNAL("signal_udev"), self.udev_callback)
    
    def stop_udev(self):
        self.udev.monitorStop()

    def udev_callback(self, device):
        if device.device_type == "usb_device":
            if device.action == "add":
                usbstate = StoreInfoParser.instance().getUsbState()
                if usbstate == "":
                    usbstate = "False"
                if usbstate == "True":
                    file = open(device.sys_path+"/idProduct")
                    idProduct ='0x' + file.read().strip('\n')
                    file = open(device.sys_path+"/idVendor")
                    idVendor ='0x' + file.read().strip('\n')
                    if usbplug.isPassthroughUsbDevice(3, idProduct, idVendor) == False:
                        if not self.usb_infilter(idProduct, idVendor):
                            self.usbmap[device.sys_path]=idProduct+idVendor
                            self.add_usb(idProduct, idVendor)
                        else:
                            pass 
                    else:
                        pass 
                else:
                    pass

            if device.action == "remove" and self.usbmap.has_key(device.sys_path):
                id=self.usbmap.pop(device.sys_path)
                if(id != None):
                    self.del_usb(id[0:6], id[-6:])
                    
    def getDomXml(self):
        if self.dom == None:
            return None
        xml = self.dom.XMLDesc()
        return xml
        
    def usb_infilter(self, idProduct, idVendor):
        plist = xmledit.get_node_attrib_list(False, self.getDomXml(), './devices/redirfilter/usbdev', 'product')
        vlist = xmledit.get_node_attrib_list(False, self.getDomXml(), './devices/redirfilter/usbdev', 'vendor')
        for i in range(len(plist)):
            if idProduct == plist[i] and idVendor == vlist[i]:
                return True
        return False
    
    def add_usb_first(self):
        usbstate = StoreInfoParser.instance().getUsbState()
        if usbstate == "":
            usbstate = "False"
        if usbstate == "True":
            usbplug.addUsbDevice(self.dom, self.usbmap)
        else:
            pass

    def add_usb(self, idProduct, idVendor):
        usbplug.addUsbDevice_byId(self.dom, idProduct, idVendor)

    def del_usb(self, idProduct, idVendor):
        usbplug.delUsbDevice_byId(self.dom, idProduct, idVendor)
        
    
    def slotDomainStop(self,name):
        imgname = self.domainInfo["name"]
        
        #createshot.revertSnapshot(imgname)  
        createshot.deleteSnapshot(imgname)
        self.undefineDomain(name)
        self.stop_udev()
        self.stateTimer.stop()
        self.usbmap.clear()
        stats.clear()
        #self._update_guests_stats()
        #adddisk.umountAllDisk()
        pass
        #revert to snapshot
        #remove snapshot
        #undefine xml
    def updateState(self):
        self._update_guests_stats()
        
    
    def startDomainByUUID(self, strUUID):
        '''
        @param strUUID: the uuid of the domain
        @type strUUID: string
        '''
        myDom = self.getDomInfoByUUID(strUUID)
        
        if myDom.isActive() == False:
            myDom.create()
        return myDom
    
    def shutdownDomain(self):
        '''
        @param name: the name of the domain need to be shutdown
        @type name: string
        '''
        name = self.domainInfo["vmname"]
        myDom = self.getDomInfoByName(name)
        if myDom == None:
            return
        if myDom.isActive() == True:
            myDom.shutdown()
            
    def poweroffDomain(self):
        '''
        @param name: the name of the domain need to be shutdown
        @type name: string
        '''
        name = self.domainInfo["vmname"]
        myDom = self.getDomInfoByName(name)
        if myDom == None:
            return
        if myDom.isActive() == True:
            myDom.destroy()
    def restartDomain(self):
        '''
        @param name: the name of the domain need to be shutdown
        @type name: string
        '''
        name = self.domainInfo["vmname"]
        myDom = self.getDomInfoByName(name)
        if myDom == None:
            return
        if myDom.isActive() == True:
            myDom.reboot()

    def listDefinedDomains(self):
        '''show all the domains by name
        '''
        return self.conn.listDefinedDomains()
    def mountDisk(self):
        name = self.domainInfo["name"]
        vmname = self.domainInfo["vmname"]
        if not self.domainInfo.has_key("classid"):
            if self.domainInfo.has_key("baseName"):
                basename = self.domainInfo["baseName"]
            else:
                basename = "False"
        else:
            studentname = StoreInfoParser.instance().getTerminalName()
            basename = self.domainInfo["classid"] + "-classbase"
            vmname = self.domainInfo["classid"] + "-" + studentname
        serverip = StoreInfoParser.instance().getCloudsServerIP()
        
        self.mountDiskThread = MountDiskThread()
        self.connect(self.mountDiskThread, SIGNAL("mountdisksuccess"), self.attachDeviceDisk)
        self.mountDiskThread.setVmInfo(vmname, serverip, basename, name)
        self.mountDiskThread.start()
        
    def attachDeviceDisk(self,xmlname):
        
        dom = self.getRunningDomain()
        if dom == None:
            return
        else:
            vmname = dom.name()
            attachCmd = "virsh attach-device " + vmname + " /var/lib/chost/disks/" + xmlname + "/" + xmlname + ".xml"
            ok = os.system(str(attachCmd))
            if ok == 0:
                pass 
            else:
                pass 
    
    def editDomainXml(self):
        name = self.domainInfo["name"]
        mac = self.domainInfo["cloud_mac"]
        cloudsip = self.domainInfo["cloud_ip"]
        vmname = self.domainInfo["vmname"]
        ostype = self.domainInfo["os"]
        flag = StoreInfoParser.instance().getNetState()
        changename.changeName(name,vmname)
        changename.changeUuid(name)
        changename.deleteNode(name)
        changename.changeAudio(name,ostype)
        addsdl.graphics_change_sdl(name)
        addinterface.defineNetworkFilter(flag, cloudsip)
        addinterface.addInterface(name, mac)
        addinterface.addSocket(name)
        addserial.addSerial(name)
        adddisk.addCdisk(name, vmname)
        changename.changeCpuCore(name)
        changename.changeMem(name)
        
        
        #copy tmpxml
        #edit name
        #edit uuid
        #edit sdl
        #add network
        #add disk
        #pass
    def deleteImgList(self,imgList):
        
#         for item in imgList:
#             dom = self.getDomInfoByName(item)
#             if dom != None:
#                 if not dom.isActive():
#                     imgList.remove(item)
#                 else:
#                     self.undefineDomain(item)
#         if len(imgList) == 0:
#             return
#         else:
        self.deleteThread = DeleteThread()
        self.deleteThread.setDeleteList(imgList)
        self.deleteThread.start()
            
    def getRunningDomain(self):
        vmname = self.domainInfo["vmname"]
        dom = self.getDomInfoByName(vmname)
        if dom == None:
            return None
        if dom.isActive():
            return dom
        else:
            return None
    def _setStats(self,status):
        
        self.status = status
            
    def _update_guests_stats(self):
        
        try:
            
            dom = self.getRunningDomain()
            if dom == None:
                #self._setStats({})
                stats.clear()
                return
                
            vm_uuid = dom.UUIDString()
            vmname = dom.name()
            name = self.domainInfo["name"]
            info = dom.info()
            state = DOM_STATE_MAP[info[0]]
    
            if state != 'running':
                stats[vm_uuid] = {}
                #continue
    
            if stats.get(vm_uuid, None) is None:
                stats[vm_uuid] = {}
    
            timestamp = time.time()
            prevStats = stats.get(vm_uuid, {})
            seconds = timestamp - prevStats.get('timestamp', 0)
            stats[vm_uuid].update({'timestamp': timestamp})
    
            self._get_percentage_cpu_usage(vm_uuid, info, seconds)
            self._get_network_io_rate(vm_uuid, dom, seconds)
            self._get_disk_io_rate(vm_uuid, dom, seconds)  
            self._get_memory_size(vm_uuid, vmname, name, info)              
            
            self._setStats(stats)
        except Exception as e:
            #self._setStats({})
            stats.clear()


    def _get_percentage_cpu_usage(self, vm_uuid, info, seconds):
        prevCpuTime = stats[vm_uuid].get('cputime', 0)

        cpus = info[3]
        cpuTime = info[4] - prevCpuTime

        base = (((cpuTime) * 100.0) / (seconds * 1000.0 * 1000.0 * 1000.0))
        percentage = max(0.0, min(100.0, base / cpus))

        stats[vm_uuid].update({'cputime': info[4], 'cpu': percentage})

    def _get_network_io_rate(self, vm_uuid, dom, seconds):
        prevNetRxKB = stats[vm_uuid].get('netRxKB', 0)
        prevNetTxKB = stats[vm_uuid].get('netTxKB', 0)
        currentMaxNetRate = stats[vm_uuid].get('max_net_io', 100)

        rx_bytes = 0
        tx_bytes = 0

        tree = ET.fromstring(dom.XMLDesc(0))
        for target in tree.findall('devices/interface/target'):
            dev = target.get('dev')
            io = dom.interfaceStats(dev)
            rx_bytes += io[0]
            tx_bytes += io[4]

        netRxKB = float(rx_bytes) / 1000
        netTxKB = float(tx_bytes) / 1000

        rx_stats = (netRxKB - prevNetRxKB) / seconds
        tx_stats = (netTxKB - prevNetTxKB) / seconds

        rate = rx_stats + tx_stats
        max_net_io = round(max(currentMaxNetRate, int(rate)), 1)

        stats[vm_uuid].update({'net_io': rate, 'max_net_io': max_net_io,
                               'netRxKB': netRxKB, 'netTxKB': netTxKB})

    def _get_disk_io_rate(self, vm_uuid, dom, seconds):
        prevDiskRdKB = stats[vm_uuid].get('diskRdKB', 0)
        prevDiskWrKB = stats[vm_uuid].get('diskWrKB', 0)
        currentMaxDiskRate = stats[vm_uuid].get('max_disk_io', 100)

        rd_bytes = 0
        wr_bytes = 0

        tree = ET.fromstring(dom.XMLDesc(0))
        for target in tree.findall("devices/disk/target"):
            dev = target.get("dev")
            io = dom.blockStats(dev)
            rd_bytes += io[1]
            wr_bytes += io[3]

        diskRdKB = float(rd_bytes) / 1024
        diskWrKB = float(wr_bytes) / 1024

        rd_stats = (diskRdKB - prevDiskRdKB) / seconds
        wr_stats = (diskWrKB - prevDiskWrKB) / seconds

        rate = rd_stats + wr_stats
        max_disk_io = round(max(currentMaxDiskRate, int(rate)), 1)

        stats[vm_uuid].update({'disk_io': rate,
                               'max_disk_io': max_disk_io,
                               'diskRdKB': diskRdKB,
                               'diskWrKB': diskWrKB})
    def _get_memory_size(self, vm_uuid, vmname, name, info):
        
        #memory_size = info[1]
        memory_size = changename.getMem()
        stats[vm_uuid].update({'memory_size':memory_size, 'vmname':vmname, 'name':name})
        
# localsolution = StoreInfoParser.instance().getResolutionValue()
# serverip = StoreInfoParser.instance().getCloudsServerIP()
