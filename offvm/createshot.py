#coding:utf-8
'''
Created on Dec 29, 2014

@author: root
'''
#from offvm import xmledit
from offvm import pathfolder
import os
import commands

#IMG_PATH = "/var/lib/libvirt/images/"
#XML_PATH = "/var/lib/libvirt/xml/"
XML_PATH = pathfolder.XML_PATH
DISK_PATH = pathfolder.DISK_PATH
IMG_PATH = pathfolder.IMG_PATH

'''CREATE_SNAPSHOT = "virsh snapshot-create-as "
REVERT_SNAPSHOT = "virsh snapshot-revert "
DELETE_SNAPSHOT = "virsh snapshot-delete "
LIST_SNAPSHOT = "virsh snapshot-list "'''

# CREATE_SNAPSHOT = "qemu-img snapshot -c "
REVERT_SNAPSHOT = "qemu-img snapshot -a "
# DELETE_SNAPSHOT = "qemu-img snapshot -d "
LIST_SNAPSHOT = "qemu-img snapshot -l "

CREATE_SNAPSHOT = "qemu-img create -b "
DELETE_SNAPSHOT = "rm -f "


def isHasSnap(name):
    listCmd = LIST_SNAPSHOT + IMG_PATH + name + "-0.img"
    keyWord = name + "-snapshot"
    output = ""
    status = commands.getstatusoutput(str(listCmd))
    if status[0] == 0:
        output = status[1]
    if output.find(keyWord) > -1:
        return True
    else:
        return False
    
def createSnapshot(name):
    createCmd = CREATE_SNAPSHOT + IMG_PATH + name + "-0.img -f qcow2 " + IMG_PATH + name + "-0-snapshot.img"
    ok = os.system(str(createCmd))
    if ok == 0:
        return 0
    else:
        
        return 1
        
def revertSnapshot(name):
    revertCmd = REVERT_SNAPSHOT + name + "-snapshot " + IMG_PATH + name + "-0.img"
    ok = os.system(str(revertCmd))
    if ok == 0:
        return 0
    else:
        return 1
        
def deleteSnapshot(name):
    deleteCmd = DELETE_SNAPSHOT + IMG_PATH + name + "-0-snapshot.img"
    ok = os.system(str(deleteCmd))
    if ok == 0:
        return 0
    else:
        return 1
    
    
def query_image_formate(path):
    if os.path.exists(path):
        cmd = 'qemu-img info ' + path
        rst = commands.getoutput(cmd)
        lines = rst.split('\n')
        for line in lines:
            if line.find('format') != -1:
                return str(line.split(':')[1]).strip()
    else:
        return ""    
    
