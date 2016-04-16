#coding:utf-8
'''
Created on Jan 20, 2015

@author: root
'''

from pyudev import Context, Monitor, MonitorObserver
context = Context()
monitor = Monitor.from_netlink(context)
monitor.filter_by(subsystem='input')
def print_device_event(device):
    print('background event {0.action}: {0.device_path}'.format(device))
    
observer = MonitorObserver(monitor,print_device_event)
observer.daemon
#True
observer.start()
