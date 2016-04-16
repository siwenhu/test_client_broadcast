#coding:utf-8

#LOCAL_IMG_DIR = "/var/lib/libvirt/images/"

from offvm import createshot
from PyQt4.QtCore import QObject, QString
from offvm import pathfolder
import os
import commands
LOCAL_IMG_DIR = pathfolder.IMG_PATH

class LocalImgManager(QObject):
    _instance = 0 
    def __init__(self):
        super(LocalImgManager,self).__init__()
        self.imgList = []

    def getCompleteList(self):
        #get the img file list as a list
        cmd = "ls " + LOCAL_IMG_DIR + "*.img"
        status = commands.getstatusoutput(cmd)
        if status[0] == 0:
            output = status[1]
        else:
            output = ""
        imgcList = output.split("\n")
        imgList = []
        for item in imgcList:
            if len(item.split("/var/lib/libvirt/images/"))>=2:
                imgList.append(item.split("/var/lib/libvirt/images/")[1].split("-0.img")[0])
        return imgList
    def getCompliteListSize(self):
        #get the size of img files as a dict
        imgMap = {}
        cmd = "ls " + LOCAL_IMG_DIR + "*.img"
        status = commands.getstatusoutput(cmd)
        if status[0] == 0:
            output = status[1]
        else:
            output = ""
        imgcList = output.split("\n")
        for item in imgcList:
            if item != "" or os.path.exists(item):
                fileSize = os.path.getsize(item)
                if len(item.split("/var/lib/libvirt/images/"))>=2:
                    key = item.split("/var/lib/libvirt/images/")[1].split("-0.img")[0]
                    imgMap[key] = fileSize
        return imgMap
        
    def getOneAll(self,name):
        cmd = "ls -a " + LOCAL_IMG_DIR
        status = commands.getstatusoutput(cmd)
        if status[0] == 0:
            output = status[1]
        else:
            output = ""
        imgcList = output.split("\n")
        imgList = []
        imgName = name + "-0.img"
        for item in imgcList:
            if QString(item).contains(imgName):
                item = LOCAL_IMG_DIR + item
                imgList.append(item)
                
        return imgList
    def getImgAll(self,deletelist):
        deleteImgList = []
        for item in deletelist:
            deleteImgList.append(str(item["name"]+"-0.img"))
            deleteImgList.append(str(item["name"]+"-0-snapshot.img"))
            #deleteImgList.append(str(item["name"]+"-0.img.scp"))
            
        cmd = "ls -a " + LOCAL_IMG_DIR
        status = commands.getstatusoutput(cmd)
        if status[0] == 0:
            output = status[1]
        else:
            output = ""
        imgcList = output.split("\n")
        
        for item in deleteImgList:
            if item in imgcList:
                imgcList.remove(item)
#         for item in imgcList:
#             if item in deleteImgList:
#                 imgcList.remove(item)
        return imgcList
    def getDeleteListAll(self,deletelist):
        deleteList = []
        for item in deletelist:
            oneAll = self.getOneAll(item)
            deleteList.append(oneAll)
        allImg = []
        for item in deleteList:
            for tmp  in item:
                allImg.append(tmp)
        return allImg
                
        
    def getImgList(self):
        return self.imgList    
    def setImgList(self,list): 
        self.imgList = list
        
    @classmethod 
    def instance(cls):
        if (cls._instance == 0):
            cls._instance = LocalImgManager()
            
        return cls._instance

#ob = LocalImgManager()
