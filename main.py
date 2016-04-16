# -*- coding: utf-8 -*-  

from PyQt4.QtCore import QTextCodec, QFile, QString
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QFont,QFontDatabase
from mainframe import MainFrame
import sys
import os
#import globalvariable
#import uuid
#import common
#from storeinfoparser import StoreInfoParser
#from logrecord import LogRecord
#import globalfunc
#import time
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))
#from ctypes import *
#import json
reload(sys)
sys.setdefaultencoding('utf-8')
import warnings
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ##获取分辨率并保存
    #currentSolution = globalfunc.getCurrentScreenResolution()
    #LogRecord.instance().logger.info(currentSolution)
    #StoreInfoParser.instance().setResolutionValue(currentSolution)
	
    #globalfunc.setVolumeTerminal()

    #if StoreInfoParser.instance().getTerminalName() is not None:
    #    terminalName = StoreInfoParser.instance().getTerminalName()
    #    globalvariable.TERMINAL_NAME = str(terminalName)


    #LogRecord.instance().logger.info(u"进入主函数")  
    #将字体文件名传给addApplicationFont,得到字体的Id
    #fontId = QFontDatabase.addApplicationFont("./simhei.ttf")
    #将字体Id传给applicationFontFamilies,得到一个QStringList,其中的第一个元素为新添加字体的family
    #msyh = QFontDatabase.applicationFontFamilies(fontId)[0]
    #font = QFont(msyh,10)
    #将此字体设为QApplication的默认字体
    #app.setFont(font)


    #加载QSS样式表
    #qss= QFile("clouds.qss")
    #qss.open(QFile.ReadOnly)
    #app.setStyleSheet(QString(qss.readAll()))
    #qss.close()
    
    #关闭屏保
    #os.system("xset dpms 0 0 0")
    #os.system("xset s 0 0")
    #os.system("setenforce 0")
       
    window = MainFrame()
    window.show()
    #window.repaint()
    #window.setPosition()
    
    #time.sleep(5)
    app.exec_()
