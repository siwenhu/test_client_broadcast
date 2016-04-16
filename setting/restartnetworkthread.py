# -*- coding: utf-8 -*-  

from PyQt4.QtCore import SIGNAL, QThread
import os
import globalfunc
from logrecord import LogRecord
from ctypes import *
import json

class RestartNetworkThread(QThread):
    def __init__(self, parent=None):
        super(RestartNetworkThread,self).__init__(parent)
        CDLL("libjson-c.so", mode=RTLD_GLOBAL)
        self.jytcapi = cdll.LoadLibrary('../lib/libjytcapi.so')
        self.jytcapi.jyinittcapi()
        self.netconf = ""
        self.networkInfoFlg = False 
    def setNetConf(self,netconf):
        self.netconf = netconf

    def getNetFlag(self):
	    #print "======get flag:%d" % self.networkInfoFlg
	    return self.networkInfoFlg

    def setNetFlag(self, flag):
        #print "======set flag:%d" % flag  
        self.networkInfoFlg = flag

    def run(self):
        LogRecord.instance().logger.info(u"开始启动网络")
        self.emit(SIGNAL("restartNetwork"), "Start")
        ok = -1
        ok = self.jytcapi.jysetwiredconf(str(self.netconf))
        if ok != 0:
            self.emit(SIGNAL("restartNetwork"), "Failed")
        else:
            self.emit(SIGNAL("restartNetwork"), "Success")
            self.networkInfoFlg = True 
            self.setNetFlag(True) 
        
        
