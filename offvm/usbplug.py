# -*- coding: utf-8 -*-

'''
    运行此脚本需要安装pyusb
'''

import os
from xml.etree import ElementTree as ET  
from usb import core
from usb import util
        
def __generateUSBXML(venderId, productId):
        root = ET.Element('hostdev', {'mode' : "subsystem", 'type': 'usb', 'managed': 'yes'})
        
        source = ET.Element('source')
        root.append(source)
        
        vender = ET.Element('vendor', {'id' : venderId})
        source.append(vender)
        
        product =  ET.Element('product', {'id' : productId})
        source.append(product)
    
        rough_string = ET.tostring(root, 'utf-8')
        return rough_string   
        
def __getSysPath(venderId, productId):
        for direct in os.listdir("/sys/bus/usb/devices"):
            dir="/sys/bus/usb/devices/"+direct
            if os.path.exists(dir+"/idProduct") and os.path.exists(dir+"/idVendor"):
                file = open(dir+"/idProduct")
                idProduct ='0x' + file.read().strip('\n')
                file = open(dir+"/idVendor")
                idVendor ='0x' + file.read().strip('\n')
                if venderId == idVendor and productId == idProduct:
                    return os.path.realpath(dir)

def __plugDevice(flag, dom, usbmap):              
        for dev in core.find(find_all=True):
            for cfg in dev:
                intf = util.find_descriptor(cfg, find_all=True)
                intf0 = util.find_descriptor(cfg, bInterfaceClass=0)
                intf3 = util.find_descriptor(cfg, bInterfaceClass=3)
                intf9 = util.find_descriptor(cfg, bInterfaceClass=9)
                if intf != None and intf0 == None and intf3 == None and intf9 == None:
                    idVendor = str(hex(dev.idVendor))
                    if len(idVendor) < 6:
                        idVendor = '0x' + '0' * (6 - len(idVendor)) + idVendor[2:]
                     
                    idProduct = str(hex(dev.idProduct))
                    if len(idProduct) < 6:
                        idProduct = '0x' + '0' * (6 - len(idProduct)) + idProduct[2:]

                    xml = __generateUSBXML(idVendor, idProduct)
                    if dom != None and dom.isActive() == True:
                        if flag:
                            dom.attachDevice(xml)
                            syspath=__getSysPath(idVendor, idProduct)
                            if syspath != None:
                                usbmap[syspath]=idProduct+idVendor
                        else:
                            dom.detachDevice(xml)
                            syspath=__getSysPath(idVendor, idProduct)
                            if syspath != None:
                                usbmap.pop(syspath)
                    else:
                        pass 

def isPassthroughUsbDevice(interfaceClass, idP, idV):              
        for dev in core.find(find_all=True):
            for cfg in dev:
                intf = util.find_descriptor(cfg, bInterfaceClass=interfaceClass)
                if intf is not None:
                    idVendor = str(hex(dev.idVendor))
                    if len(idVendor) < 6:
                        idVendor = '0x' + '0' * (6 - len(idVendor)) + idVendor[2:]
                     
                    idProduct = str(hex(dev.idProduct))
                    if len(idProduct) < 6:
                        idProduct = '0x' + '0' * (6 - len(idProduct)) + idProduct[2:]

                    if idVendor !=None and idProduct != None and idVendor == idV and idProduct == idP:
                        return True

        return False

def addUsbDevice(dom, usbmap):
    __plugDevice(True, dom, usbmap)

def addUsbDevice_byId(dom, idProduct, idVendor):
    xml = __generateUSBXML(idVendor, idProduct)
    if dom != None and dom.isActive() == True:
        dom.attachDevice(xml)
    else:
        pass
def delUsbDevice_byId(dom, idProduct, idVendor):
    xml = __generateUSBXML(idVendor, idProduct)
    if dom !=None and dom.isActive() == True:
        dom.detachDevice(xml)
    else:
        pass
