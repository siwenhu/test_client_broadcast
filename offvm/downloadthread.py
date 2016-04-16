#coding:utf-8
'''
Created on Dec 18, 2014

@author: root
'''
from PyQt4.QtCore import QThread, SIGNAL
import commands
import os
import pexpect
from storeinfoparser import StoreInfoParser
from vminfomanager import VMInfoManager
from offvm import pathfolder
import time
CMD="rsync -avzp root@"
CMD_DIR = ":/var/lib/libvirt/images/"
XCMD="rsync -avzp root@"
SCPCMD = "scp root@"
XCMD_DIR = ":/etc/libvirt/qemu/"
add = " " + pathfolder.IMG_PATH
xadd = " " + pathfolder.XML_PATH
XML_PATH = pathfolder.XML_PATH

IMG_PATH = pathfolder.IMG_PATH

USERNAME="root"
USERPASSWD="root+-*/root"

class DownloadThread(QThread):
    def __init__(self,parent=None):
        super(DownloadThread,self).__init__(parent)
        
    def setNeccInfo(self):
        pass
    def setProcessId(self,vmid):
        self.vmid = vmid
        self.filename = vmid.split(":")[0]
        self.signalid = vmid.split(":")[0] +":" + vmid.split(":")[1] + ":" + vmid.split(":")[2]
        #serverip = StoreInfoParser.instance().getCloudsServerIP()
    def run(self):
        serverip = StoreInfoParser.instance().getCloudsServerIP()
        progress = self.getProgress()
        xmlfile = XML_PATH + self.filename + ".xml"
        TCMD = CMD + serverip + CMD_DIR + self.vmid.split(":")[0] + "-0.img" + add + self.vmid.split(":")[0] + "-0.img"
        XMCMD = XCMD + serverip + XCMD_DIR + self.vmid.split(":")[0] + ".xml" + xadd + self.vmid.split(":")[0] + ".xml"
        SCMD = SCPCMD + serverip + CMD_DIR + self.vmid.split(":")[0] + "-0.img" + add + self.vmid.split(":")[0] + "-0.img.scp"
        SXMCMD = SCPCMD + serverip + XCMD_DIR + self.vmid.split(":")[0] + ".xml" + xadd + self.vmid.split(":")[0] + ".xml"
        MVCMD = "mv -f" + add + self.vmid.split(":")[0] + "-0.img.scp" + add + self.vmid.split(":")[0] + "-0.img"
        if progress == 100:
            if os.path.exists(xmlfile):
                pass
            else:
                result,msg = self.exeDownloadCmd(str(SXMCMD))
                
            if not result:
                self.emit(SIGNAL("downloaderror"),self.signalid)
                return
                
        elif progress == 99:
            imgd,msg = self.exeDownloadCmd(str(SCMD))
            if not imgd:
                self.emit(SIGNAL("downloaderror"),self.signalid)
                return
            
            if os.path.exists(xmlfile):
                pass
            else:
                xmld,msg = self.exeDownloadCmd(str(SXMCMD))
                if not xmld:
                    self.emit(SIGNAL("downloaderror"),self.signalid)
                    return
                
        else:
            imgd,msg = self.exeDownloadCmd(str(SCMD))
            if not imgd:
                self.emit(SIGNAL("downloaderror"),self.signalid)
                return
            if os.path.exists(xmlfile):
                pass
            else:
                xmld,msg = self.exeDownloadCmd(str(SXMCMD))
                if not xmld:
                    self.emit(SIGNAL("downloaderror"),self.signalid)
                    return
        serverState = VMInfoManager.instance().getCurCloudServerState()
        if serverState != "enable":
            return
        os.system(str(MVCMD))            
        time.sleep(5)
        self.emit(SIGNAL("downloadover"),100,self.signalid)        
        
    def getImgTotalSize(self):
        return str(self.vmid.split(":")[3])
    
    def getProgress(self):
        totalSize = int(self.getImgTotalSize())
        filePath = IMG_PATH + self.filename + "-0.img"
        if os.path.exists(filePath):
            if os.path.getsize(filePath) == totalSize:
                time.sleep(1)
                return 100
            else:
                return 99
        else:
            return 0
    def exeDownloadCmd(self, cmd):
            # 开始同步
        child = pexpect.spawn(command=cmd, timeout=365*24*60*60)
        state = False
        msg = ''
        if True:
            ssh_newkey = 'Are you sure you want to continue connecting'
            index = child.expect ([ssh_newkey,'password:',pexpect.EOF, pexpect.TIMEOUT])
            if index == 0:
                child.sendline('yes')
                index = child.expect (['password:',pexpect.EOF, pexpect.TIMEOUT])
                if index == 0:
                    state = True
                    child.sendline(USERPASSWD)
                    index = child.expect(["total size is" ,pexpect.EOF, pexpect.TIMEOUT])
                    if index == 1:
                        msg = "error"
                    elif index == 2:
                        msg =  "timeout"
                    else:
                        state = True
                        child.close(force=True)
                        return state,"complete"
                
                elif index == 1:
                    msg = "error"
                elif index == 2:
                    msg =  "timeout"
               
            elif index == 1:
                state = True
                child.sendline(USERPASSWD)
                index = child.expect(["total size is" ,pexpect.EOF, pexpect.TIMEOUT])
                
                if index == 1:
                    msg =  "error"
                    
                elif index == 2:
                    msg = "timeout"
                else:
                    child.close(force=True)
                    return state, "complete"
                    
            elif index == 2:
                state = False
                msg = "error"
                
            elif index == 3:
                state = False
                msg =  "timeout"
                
        child.close(force=True) 
        return state,msg
    
