#coding:utf-8
'''
Created on Feb 27, 2015

@author: root
'''
import socket
import time

def writeToSocket(solution):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    #sock.sun_family = writesocket.AF_UNIX
    #sock.family = writesocket.AF_UNIX
    conn = '/var/lib/libvirt/qemu/channels/com.massclouds.cclassroom.0'
    sock.connect(conn)
    time.sleep(1)
    sock.send(solution)
    sock.close()
    

#writeToSocket("1024x768x")
