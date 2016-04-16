# -*- coding: utf-8 -*-

import pyudev
from pyudev import Context, Monitor, MonitorObserver
from PyQt4.QtCore import QObject, SIGNAL
from logrecord import LogRecord


class Udev(QObject):
    
    def __init__(self):
        super(Udev, self).__init__()

    def monitor_async(self, subsystems, device_type, callbak):
        context = Context()
        monitor = Monitor.from_netlink(context)
        monitor.filter_by(subsystems)
        def device_event(device):
            self.emit(SIGNAL("signal_udev"), device)
            if callbak != None:
                callbak(device)
        try:
            self.observer = MonitorObserver(monitor, callback=device_event, name='udev-monitor-observer')
            self.observer.daemon
            self.observer.start()
            #observer.stop()
        except Exception as e:
            LogRecord.instance().logger.info(u'USB监听启动异常(%s)'%(str(e)))
            
    def monitorStop(self):
        try:
            self.observer.stop()
        except Exception as e:
            pass 
