#coding:utf-8
'''
Created on Dec 18, 2014

@author: root
'''
from PyQt4.QtCore import QThread,SIGNAL
from vminfomanager import VMInfoManager
import commands
import os
import time
from offvm import pathfolder
#CMD="rsync -avzp root@192.168.5.133:/var/lib/libvirt/images/xp-0.img /var/lib/libvirt/images/xp-0.img"
#IMG_PATH = "/var/lib/libvirt/images/"
#XML_PATH = "/var/lib/libvirt/xml/"
IMG_PATH = pathfolder.IMG_PATH
XML_PATH = pathfolder.XML_PATH
IMGNAME = "-0.img"
class ProgressThread(QThread):
    def __init__(self,parent=None):
        super(ProgressThread,self).__init__(parent)
        self.auto = True
    def setNeccInfo(self):
        pass
    def setProcessId(self,vmid):
        self.vmid = vmid.split(":")[0] +":" + vmid.split(":")[1] + ":" + vmid.split(":")[2]
        self.filesize = vmid.split(":")[3]
        self.filename = vmid.split(":")[0]
    def run(self):
        count = 0
        count = self.getProgress()
        while count < 100:
            serverstate = VMInfoManager.instance().getCurCloudServerState()
            if serverstate != "enable":
                break
            self.emit(SIGNAL("currentprogress"),count,self.vmid)
            #count += 2
            count = self.getProgress()
            time.sleep(1)
            if self.auto == False:
                count = 556
        
        if count >= 100 and count < 555:
            #self.emit(SIGNAL("downloadover"),count,self.vmid)
            pass 
    def getImgTotalSize(self):
        return self.filesize
    def getProgress(self):
        totalSize = int(self.getImgTotalSize())
        filePath = IMG_PATH + self.filename + "-0.img"
        xfilePath = XML_PATH + self.filename + ".xml"
        if os.path.exists(filePath):
            if os.path.getsize(filePath) == totalSize :
                time.sleep(1)
                return 100
            else:
                os.remove(filePath)
                return 0
        else:
            currentSize = self.imgIsInList()
            return currentSize*100/totalSize
    def getCurrentDirList(self):
        cmd = "ls -a " + IMG_PATH
        statusoutput = []
        statusoutput = commands.getstatusoutput(cmd)
        if statusoutput[0] == 0:
            output = statusoutput[1]
            return output.split("\n")
        else:
            output = ""
            return []
    def imgIsInList__(self):
        fileList = self.getCurrentDirList()
        strname = self.filename + IMGNAME
        for item in fileList:
            if len(item.split(strname)) == 2 and item.split(strname)[0] == ".":
                fileDir = IMG_PATH + item
                return os.path.getsize(fileDir)
            
        return 0
    def imgIsInList(self):
        fileList = self.getCurrentDirList()
        strname = self.filename + IMGNAME
        for item in fileList:
            if len(item.split(strname)) == 2:
                fileDir = IMG_PATH + item
                return os.path.getsize(fileDir)
            
        return 0
    
    def stop(self):
        self.auto = False
        
