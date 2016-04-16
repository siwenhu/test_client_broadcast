#coding:utf-8
'''
Created on Dec 29, 2014

@author: root
'''
from offvm import xmledit
from offvm import pathfolder
import os
import commands

XML_PATH = pathfolder.XML_PATH
DISK_PATH = pathfolder.DISK_PATH
IMG_PATH = pathfolder.IMG_PATH
remoteMnt = ":/var/lib/chost/disks/"

def mountDisk(vmname,serverip):
    #mount the personal disk
    if vmname == "" or serverip == "":
        return False
    umountPath = "umount " + DISK_PATH + "*"
    os.system(str(umountPath))
    localMnt = DISK_PATH + vmname
    remontPath = remoteMnt + vmname
    mountcmd = "mount -t nfs -o hard -o timeo=1000 " + serverip + remontPath + " " + localMnt
    if not os.path.exists(localMnt):
        mkdircmd = "mkdir -p " + localMnt
        mkdirok = os.system(str(mkdircmd))
        mountok = os.system(str(mountcmd))
        if mkdirok == 0 and mountok == 0:
            disk = localMnt + "/" + vmname + ".img"
            if os.path.exists(disk):
                return True
            else:
                return False
    else:
        mountok = os.system(str(mountcmd))
        if mountok == 0:
            disk = localMnt + "/" + vmname + ".img"
            
            if os.path.exists(disk):
                return True
            else:
                return False
        
def umountAllDisk():
    #mount the personal disk
    umountPath = "umount " + DISK_PATH + "*"
    os.system(str(umountPath))
            
def mountBaseDisk(basename,serverip):
    #mount the personal base disk
    if basename == "False":
        return True
    if basename == "" or serverip == "":
        return False
    #umountPath = "umount " + DISK_PATH + "*"
    #os.system(str(umountPath))
    
    localMnt = DISK_PATH + basename
    remontPath = remoteMnt + basename
    mountcmd = "mount -t nfs -o hard -o timeo=1000 " + serverip + remontPath + " " + localMnt
    if not os.path.exists(localMnt):
        mkdircmd = "mkdir -p " + localMnt
        mkdirok = os.system(str(mkdircmd))
        mountok = os.system(str(mountcmd))
        if mkdirok == 0 and mountok == 0:
            disk = localMnt + "/" + basename + ".img"
            if os.path.exists(disk):
                return True
            else:
                return False
    else:
        mountok = os.system(str(mountcmd))
        if mountok == 0:
            disk = localMnt + "/" + basename + ".img"
            
            if os.path.exists(disk):
                return True
            else:
                return False
            
def addCdisk(name,vmname):
    #add the C disk
    xml = XML_PATH + name + ".xml"
    cdisk = IMG_PATH + name + "-0-snapshot.img"
    if os.path.exists(xml) and os.path.exists(cdisk):
        #xmledit.del_node_by_attrib(True, xml, './devices', "interface")
        xmledit.add_node(True, xml, './devices', "disk", {"type" : "file", "device":"disk"})
        xmledit.add_node(True, xml, './devices/disk', "driver", {"io":"native", "name" : "qemu", "type":"qcow2"})
        xmledit.add_node(True, xml, './devices/disk', "source", {"file" : cdisk})
        xmledit.add_node(True, xml, './devices/disk', "address", { "bus":"0x00", "domain":"0x0000", "function":"0x0", "slot":"0x09", "type":"pci"})
        xmledit.add_node(True, xml, './devices/disk', "target", {"dev" : "hda", "bus":"virtio"})
    else:
        pass        

def addDisk(name,vmname,basename):
    #add the personal disk
    xml = XML_PATH + name + ".xml"
    disk = DISK_PATH + vmname + "/" + vmname + ".img"
    if basename != "False": 
        disktype = "qcow2"
    else:
        disktype = "raw"
    if os.path.exists(xml) and os.path.exists(disk):
        xmledit.add_node(True, xml, './devices', "disk", {"type" : "file", "device":"disk", "snapshot":"no"})
        xmledit.add_node(True, xml, './devices/disk', "driver", {"name" : "qemu", "type":disktype, "cache":"none", "error_policy":"stop", "io":"threads"})
        xmledit.add_node(True, xml, './devices/disk', "source", {"file" : disk})
        xmledit.add_node(True, xml, './devices/disk', "target", {"dev" : "sdu", "bus":"usb"})
        #xmledit.add_node(True, xml, "./devices/disk", "serial", None, "c6ce5788-8779-4e10-a2b2-1cb0f9d86e50")
        #xmledit.add_node(True, xml, "./devices/disk", tag, attrib, text)
    else:
        pass 

def query_image_formate(path):
    #get the format of the person disk(no use)
    if os.path.exists(path):
        output = ""
        cmd = "qemu-img info " + "'" + path + "'"
        rst = commands.getstatusoutput(str(cmd))
        if rst[0] == 0:
            output = rst[1]
        lines = output.split('\n')
        for line in lines:
            if line.find('format') != -1:
                return str(line.split(':')[1]).strip()
    else:
        pass 
        return ""          
