#coding:utf-8
'''
Created on Dec 29, 2014

@author: root
'''
import os
import xmledit
from offvm import pathfolder
XML_PATH = pathfolder.XML_PATH
DISK_PATH = pathfolder.DISK_PATH
IMG_PATH = pathfolder.IMG_PATH

def graphics_change_sdl(name):
    #change the graphics to sdl
    display = os.environ.get('DISPLAY')
    if display == None:
        display = ":0.0"

    xauthfile = os.environ.get('XAUTHORITY')
    if xauthfile == None:
        xauthfile = "/root/.xauthority"
    os.system("chmod +r " + xauthfile)
    
    xml = XML_PATH + name + ".xml"
    if os.path.exists(xml):
        xmledit.del_node_by_attrib(True, xml, './devices', "graphics")
        xmledit.add_node(True, xml, './devices', "graphics", {"type" : "sdl", "display" : display, "xauth" : xauthfile, "fullscreen" : "yes"})
    else:
        pass 
            

            
#graphics_change_sdl("xp")
