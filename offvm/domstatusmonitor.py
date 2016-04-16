#coding:utf-8
'''
Created on Dec 29, 2014

@author: root
'''
from PyQt4.QtCore import QThread,SIGNAL
import commands
import libvirt
import time

class DomStatusMonitor(QThread):
    def __init__(self,parent=None):
        super(DomStatusMonitor,self).__init__(parent)
        
        self.auto = True
    def getDomStatus(self,name):
        cmd = "virsh list"
        status = commands.getstatusoutput(str(cmd))
        if status[0] == 0:
            output = status[1]
        else:
            output = ""
            
        if output.find(name) > -1:
            return True
        else:
            return False
        
    def run(self):
        oldauto= self.getDomStatus(self.domName)
        
        while self.auto:
            self.auto = self.getDomStatus(self.domName)
            if oldauto == self.auto == False:
                self.auto = True
                
            elif oldauto == True and self.auto == True:
                self.auto = True
                
            elif oldauto == False and self.auto == True:
                oldauto = True
                
            elif oldauto == True and self.auto == False:
                self.auto = False
            
            time.sleep(1)
            
        self.emit(SIGNAL("domainshutdown"),self.domName)
        #self.stop()
        
    def setName(self,name):
        self.domName = name
        self.auto = True


        
        