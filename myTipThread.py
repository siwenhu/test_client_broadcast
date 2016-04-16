#coding:utf-8
'''
Created on 2014-8-19

@author: root
'''
#from PyQt4.QtGui import QThread
from PyQt4.QtCore import QThread,SIGNAL
import time
import commands
import common

class MyThread(QThread):
    def __init__(self,parent = None):
        super(MyThread,self).__init__(parent)
        
        
    def run(self):
        self.auto = True
        while self.auto:
            statusOutput = commands.getstatusoutput("cat %s" % common.LOG_PATH)
            #commands.getoutput("top -b /root/a)
            #statusOutput = commands.getstatusoutput("top -b ")
            if statusOutput[0] == 0:
                output = statusOutput[1]                
                self.emit(SIGNAL("getoutput"), output)
#                 return output
                time.sleep(1.5)
    def stop(self):
        self.auto = False
        
