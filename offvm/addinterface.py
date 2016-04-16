#coding:utf-8
'''
Created on Dec 29, 2014

@author: root
'''
from offvm import xmledit
from offvm import pathfolder
import os
import commands
import globalfunc
XML_PATH = pathfolder.XML_PATH
DISK_PATH = pathfolder.DISK_PATH
IMG_PATH = pathfolder.IMG_PATH
DROP_PATH = pathfolder.DROP_NETXML_PATH
ACCEPT_PATH = pathfolder.ACCEPT_NETXML_PATH

def create_dstipfilter():
    #dstipaddr:需要传参
    mes = " <filter name='no-ip-out' chain='ipv4'>\
                <uuid>fce8ae34-e69e-83bf-262e-30786c1f8072</uuid>\
                <rule action='drop' direction='out' priority='500'>\
                    <ip match='no' dstipaddr='192.168.5.0' dstipmask='255.255.255.0'/>\
                </rule>\
            </filter>"
    
    os.system('touch dstipfilter.xml')
    os.system('echo %s >> dstipfilter.xml')
    os.system('virsh nwfilter-define dstipfilter.xml')
    #2.在addInterface 24行加入
    #xmledit.add_node(True, xml, './devices/interface', "filterref", {"filter" : "no-ip-out"})

def createFilterFile(num,ipone,iptwo=None):
    
    contentone = '''<filter name='no-ip-out' chain='ipv4'>
    <uuid>fce8ae34-e69e-83bf-262e-30786c1f8072</uuid>
    <rule action='accept' direction='out' priority='100'>
        <ip srcipaddr='0.0.0.0' dstipaddr='255.255.255.255' protocol='udp' srcportstart='68' dstportstart='67'/>
    </rule>
    <rule action='accept' direction='in' priority='100'>
        <ip protocol='udp' srcportstart='67' dstportstart='68'/>
    </rule>
    <rule action='drop' direction='out' priority='200'>
        <ip match='no' dstipaddr='%s' dstipmask='255.255.255.0'/>
    </rule>
</filter>''' % (ipone)

    contenttwo = '''<filter name='no-ip-out' chain='ipv4'>
    <uuid>fce8ae34-e69e-83bf-262e-30786c1f8072</uuid>
    <rule action='accept' direction='out' priority='100'>
        <ip srcipaddr='0.0.0.0' dstipaddr='255.255.255.255' protocol='udp' srcportstart='68' dstportstart='67'/>
    </rule>
    <rule action='accept' direction='in' priority='100'>
        <ip protocol='udp' srcportstart='67' dstportstart='68'/>
    </rule>
    <rule action='drop' direction='out' priority='200'>
        <ip match='no' dstipaddr='%s' dstipmask='255.255.255.0'/>
        <ip match='no' dstipaddr='%s' dstipmask='255.255.255.0'/>
    </rule>
</filter>''' %(ipone,iptwo)
                
                
    f= open(DROP_PATH, 'w')
    if num == 1:
        f.write(contentone)
    else:
        f.write(contenttwo)
    f.close()


def defineNetworkFilter(flag,cloudsip):
    #undefineNetworkFilter()
    ipaddr = "0.0.0.0"
    cipaddr = "0.0.0.0"
    #xmledit.del_node_by_attrib(True, DROP_PATH, './devices', 'disk', {"device":"cdrom"})
    if flag == "False":
        ip = globalfunc.get_ip_address().split('.')
        ip[3] = '0'  #list become ["192","168","5","0"]
        ipaddr = '.'.join(ip) #list become a str of "192.168.5.0"
        if cloudsip !=None:
            cip = cloudsip.split('.')
            cip[3] = "0"
            cipaddr = '.'.join(cip)
        else:
            cipaddr = ipaddr
        
        if ipaddr == cipaddr:
            createFilterFile(1,ipaddr)
        else:
            createFilterFile(2,ipaddr,cipaddr)
        defineCmd = "virsh nwfilter-define " + DROP_PATH
    else:
        defineCmd = "virsh nwfilter-define " + ACCEPT_PATH
        
    #ok = os.system(defineCmd)
    #if ok == 0:
    (status,output) = commands.getstatusoutput(defineCmd)
    if status != 0:
       pass 
    
def undefineNetworkFilter():
    output = getFilterList()
    if output.find("no-ip-out"):
        undefineCmd = "virsh nwfilter-undefine no-ip-out"
        os.system(undefineCmd)
    else:
        return

def getFilterList():
    listCmd = "virsh nwfilter-list"
    output = ""
    status = commands.getstatusoutput(listCmd)
    if status[0] == 0:
        output = status[1]
    
    return output

def addInterface(name,mac):
    #add the net of interface
    xml = XML_PATH + name + ".xml"
    if os.path.exists(xml):
        xmledit.del_node_by_attrib(True, xml, './devices', "interface")
        xmledit.add_node(True, xml, './devices', "interface", {"type" : "bridge"})
        xmledit.add_node(True, xml, './devices/interface', "mac", {"address" : mac})
        xmledit.add_node(True, xml, './devices/interface', "source", {"bridge" : "br0"})
        xmledit.add_node(True, xml, './devices/interface', "model", {"type" : "virtio"})
        xmledit.add_node(True, xml, './devices/interface', "filterref", {"filter" : "no-ip-out"})
        #xmledit.add_node(True, xml, './devices/interface', "address", {"type" : "pci", "domain":"0x0000", "slot":"0x03", "bus":"0x00", "function":"0x0"})
    else:
        pass 
        
def addSocket(name):
    #add the net of interface
    xml = XML_PATH + name + ".xml"
    if os.path.exists(xml):
        xmledit.del_node_by_attrib(True, xml, './devices', "channel")
        xmledit.add_node(True, xml, './devices', "channel", {"type" : "unix"})
        xmledit.add_node(True, xml, './devices/channel', "source", {"mode" : "bind", "path":"/var/lib/libvirt/qemu/channels/com.massclouds.cclassroom.0"})
        xmledit.add_node(True, xml, './devices/channel', "target", {"type" : "virtio", "name":"com.massclouds.cclassroom.0"})
        xmledit.add_node(True, xml, './devices/channel', "address", {"type" : "virtio-serial", "controller":"0", "bus":"0", "port":"4"})
        #xmledit.add_node(True, xml, './devices/interface', "address", {"type" : "pci", "domain":"0x0000", "slot":"0x03", "bus":"0x00", "function":"0x0"})
    else:
        pass 

# xmledit.update_node_attrib(True, "/root/workspace/nwclient/dstipfilter.xml", "./rule/ip", {"dstipaddr":"0.0.0.0"})
# xmledit.add_node(True, "/root/workspace/nwclient/dstipfilter.xml", './rule', "ip", {"dstipaddr":"0.0.0.0", "dstipmask":"1.2.65.2", "match":"no"})
#xmledit.del_node_by_attrib(True, "/root/workspace/nwclient/dstipfilter.xml", './rule', 'ip', {"match":"no"})
#xmledit.del_parent_node_by_attrib(True, "/root/workspace/nwclient/dstipfilter.xml", "./rule", "ip", {"match":"no"})



#createFilterFile(2,"192.168.5.0","192.168.4.0")
