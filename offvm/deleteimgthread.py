#coding:utf-8
'''
Created on Jan 4, 2015

@author: root
'''

#LOCAL_IMG_DIR = "/var/lib/libvirt/images/"
from PyQt4.QtCore import QThread

from offvm.localimgmanager import LocalImgManager
from offvm import pathfolder
import os
LOCAL_IMG_DIR = pathfolder.IMG_PATH

class DeleteThread(QThread):
    def __init__(self,parent=None):
        super(DeleteThread,self).__init__(parent)
        
        self.deleteList = []
    def setDeleteList(self,deletelist):
        self.deleteList = deletelist
        
    def getAllImg(self):
        #deletelist = []
        return LocalImgManager.instance().getImgAll(self.deleteList)
        
    def run(self):
        imgList = self.getAllImg()
        for item in imgList:
            itemdir = LOCAL_IMG_DIR + item
            if os.path.isfile(itemdir):
                #return
                os.remove(itemdir)
            
            
