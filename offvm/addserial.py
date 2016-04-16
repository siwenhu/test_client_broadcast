#coding:utf-8
'''
Created on Mar 17, 2015

@author: root
'''
"""
<serial type='dev'>
    <source path='/dev/ttyS0'/>
    <target port='0'/>
</serial>
<console type='dev'>
    <source path='/dev/ttyS0'/>
    <target type='serial' port='0'/>
</console>
"""
from offvm import pathfolder
from offvm import xmledit
XML_PATH = pathfolder.XML_PATH
def addSerial(name):
    xml = XML_PATH + name + ".xml"
    xmledit.del_node_by_attrib(True, xml, './devices', "serial")
    xmledit.del_node_by_attrib(True, xml, './devices', "console")
    xmledit.add_node(True, xml, './devices', "serial", {"type" : "dev"})
    xmledit.add_node(True, xml, './devices/serial', "source", {"path" : "/dev/ttyS0"})
    xmledit.add_node(True, xml, './devices/serial', "target", {"port" : "0"})
    
    xmledit.add_node(True, xml, './devices', "console", {"type" : "dev"})
    xmledit.add_node(True, xml, './devices/console', "source", {"path" : "/dev/ttyS0"})
    xmledit.add_node(True, xml, './devices/console', "target", {"port" : "0"})
    
    
#addSerial("hg")