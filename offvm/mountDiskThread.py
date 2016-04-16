#coding:utf-8
'''
Created on 2015年4月9日

@author: root
'''
from PyQt4.QtCore import QThread, SIGNAL
from PyQt4.QtGui import QApplication
from offvm import adddisk
from vminfomanager import VMInfoManager
#QThread.terminate()
class MountDiskThread(QThread):
    def __init__(self,parent=None):
        super(MountDiskThread,self).__init__(parent)
        self.state = False
        self.vmname = ""
        self.serverip = ""
        self.basename = ""
        self.name = ""
        
    def run(self):
        serverState = VMInfoManager.instance().getCurCloudServerState()
        if serverState != "enable":
            return
        ret = adddisk.mountDisk(self.vmname, self.serverip)
        if not ret:
            return False
        retbase = adddisk.mountBaseDisk(self.basename, self.serverip)
        if ret and retbase:
            #adddisk.addDisk(self.name, self.vmname, self.basename)
            self.emit(SIGNAL("mountdisksuccess"),self.vmname)
            return True
        else:
            return False
        
    def setVmInfo(self,vmname,serverip,basename,name):
        self.name = name
        self.vmname = vmname
        self.serverip = serverip
        self.basename = basename
    
