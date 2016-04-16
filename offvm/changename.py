#coding:utf-8
'''
Created on Dec 30, 2014

@author: root
'''
import xmledit
import pathfolder
import os
import shutil
import uuid
import psutil
from multiprocessing import cpu_count

XML_PATH = pathfolder.XML_PATH
DISK_PATH = pathfolder.DISK_PATH
IMG_PATH = pathfolder.IMG_PATH

def getMem():
    mem = psutil.virtual_memory()
    
    memo = mem.total/1024/1024/1024 - 1
    if memo <= 0:
        return 1
    else:
        return memo
    
def changeMem(name):
    mem = getMem()*1024*1024
    filepath = XML_PATH + name + ".xml"
    if not os.path.exists(filepath):
        return
    xmledit.update_node_text(True, filepath, './memory',str(mem))
    xmledit.update_node_text(True, filepath, './currentMemory',str(mem))

def changeName(name,vmname):
    #change the name of domain
    filepath = XML_PATH + name + ".xml"
    if not os.path.exists(filepath):
        return
    xmledit.update_node_text(True, filepath, './name',vmname)
    
def changeImg(name):
    #change the C img file
    filepath = XML_PATH + name + ".xml"
    imgpath = IMG_PATH + name + "-0.img"
    if not os.path.exists(filepath):
        return
    if not os.path.exists(imgpath):
        pass 
    xmledit.update_node_attrib(True, filepath, "./devices/disk/source", {"file":imgpath})
    
def changeAudio(name,ostype):
    #change the audio of domain, vga,cirrus or others
    filepath = XML_PATH + name + ".xml"
    xmledit.del_node_attrib(True, filepath, "./devices/video/model", "ram")
    if ostype == "Windows 7" or ostype == "Windows 7 x64":
        xmledit.update_node_attrib(True, filepath, "./devices/video/model", {"type":"vga"})
    elif ostype == "Windows XP":
        xmledit.update_node_attrib(True, filepath, "./devices/video/model", {"type":"qxl"})
    else:
        xmledit.update_node_attrib(True, filepath, "./devices/video/model", {"type":"vga"})
        
def changeCpuCore(name):
    #change the audio of domain, vga,cirrus or others
    filepath = XML_PATH + name + ".xml"
    coreCount = cpu_count()
    #if coreCount > 1:
        #coreCount-=1
    
    xmledit.update_node_text(True, filepath, './vcpu',str(coreCount))
    
    xmledit.update_node_attrib(True, filepath, "./cpu/topology", {"cores":str(coreCount)})
    xmledit.update_node_attrib(True, filepath, "./cpu/topology", {"sockets":"1"})
    xmledit.update_node_attrib(True, filepath, "./cpu/topology", {"threads":"1"})

def copyVmXml(name, osType):
    #拷贝xml文件，从一个地方烤到另一个地方        
    LOCAL_XML = "/etc/libvirt/qemu/localtmp.xml"
    dest = XML_PATH + name + '.xml'
    src = ''
    if osType == "windows_xp":
        src = LOCAL_XML
    elif osType == 'windows7':
        src = LOCAL_XML
    else:
        src = LOCAL_XML
    shutil.copyfile(src, dest)#将data从src拷贝到dest
    return dest

def changeUuid(name):
    #change the uuid of domain
    filepath = XML_PATH + name + ".xml"
    uuidc = uuid.uuid4()
    if not os.path.exists(filepath):
        return
    xmledit.update_node_text(True, filepath, './uuid',str(uuidc))
    
def deleteNode(name):
    #delete the node of need to change
    filepath = XML_PATH + name + ".xml"
    if not os.path.exists(filepath):
        return
    for i in range(3):
        xmledit.del_node_by_attrib(True, filepath, './devices', 'disk', {"device":"cdrom"})
        xmledit.del_node_by_attrib(True, filepath, './devices', 'disk', {"device":"disk"})
        xmledit.del_node_by_attrib(True, filepath, './devices', 'disk', {"device":"floppy"})
        #xmledit.del_node_by_attrib(True, filepath, './devices', 'channel', {"type":"spicevmc"})
        xmledit.del_node_by_attrib(True, filepath, './devices', 'redirdev', {"type":"spicevmc"})
        xmledit.del_node_by_attrib(True, filepath, './devices', 'graphics', {"type":"vnc"})
        xmledit.del_node_by_attrib(True, filepath, './devices', 'graphics', {"type":"spice"})
        xmledit.del_node_attrib(True, filepath, "./vcpu", "current")
        xmledit.del_node_attrib(True, filepath, "./vcpu", "placement")
        #xmledit.del_node_by_attrib(flag, xml, xpath, tag, kv_map)
        #xmledit.del_node_by_attrib(True, filepath, 'domain',"cpu")
        #xmledit.del_parent_node_by_attrib(True, filepath, "./cpu/topology", "topology", {"threads":"1"})
        #xmledit.update_node_text(True, filepath, './cpu',"")
    
#deleteNode("xp")
#changeCpuCore("xp")g\

#changeMem("xp")
