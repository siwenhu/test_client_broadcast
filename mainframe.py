# -*- coding: utf-8 -*-  

from PyQt4.QtCore import Qt, QPoint, QSize, SIGNAL, QTimer, QTranslator,\
    QCoreApplication
from PyQt4.QtGui import QWidget, QDialog, QPixmap, QColor, QPen, QPainterPath, QPainter, QApplication, \
                        QFontMetrics, QAction, QKeySequence, QLabel, QFont,\
    QPalette
from mainwindow import MainWindow
from storeinfoparser import StoreInfoParser
from tools.basics import ToolWidget
from setting.settingWidget import SettingWidget
from about.aboutwidget import AboutWidget
from base.passworddialog import PasswordDialog
#from logrecord import LogRecord  
#import globalvariable
#from recordWidget import RecordWidget
from broadclient.udpclient import UdpClient
import  mainwindow          

class MainFrame(QWidget):
        
    def __init__(self,parent = None):
        super(MainFrame,self).__init__(parent)
        
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
            StoreInfoParser.instance().setLanguage("chinese")
        else:
            QmName = "en_US.qm"
            
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
        #初始化子控件
        self.initSubWidget()

        #绑定信号和槽
        self.bandSignalSlot()
        
        self.setMinimumSize(800,600)
        self.showFullScreen()
        
        self.updateWidgetInfo()
        self.setPosition()
        #self.repaint()
    def initSubWidget(self):
        
        self.linesPath = None
        self.widthtwo = 0
        self.widthseven = 0
        self.heightone = 0
        self.heightfive = 0
        
        self.copyLabel = QLabel(self)
        self.copyLabel.setFixedWidth(400)
        self.copyLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel = QLabel(self)
        self.nameLabel.setFixedWidth(400)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.copyLabel.setFont(QFont("simhei",9))
        self.nameLabel.setFont(QFont("simhei",15))
        
        self.netLabel = QLabel(self)
        self.netLabel.setFixedWidth(800)
        self.netLabel.setFixedHeight(20)
        #self.netLabel.setAlignment(Qt.AlignLeft)
        self.netLabel.setAlignment(Qt.AlignCenter)
        self.netLabel.setText(self.tr("Can not connect to server, please check network and server address!"))
        self.netLabel.setFont(QFont("simhei",12,QFont.Bold))
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.red)
        self.netLabel.setPalette(pe)
        self.netLabel.hide()
        
        #self.updateTimer = QTimer(self)
        #self.connect(self.updateTimer, SIGNAL("timeout"),self.updateWidgetInfo)
        #self.updateTimer.start(10)
        
        #主窗口
        self.mainwindow = MainWindow(self)

        #关于对话框
        self.aboutWidget = AboutWidget(self)
        self.aboutWidget.hide()
        #self.showDlg = SettingWidget(self.mainwindow)
        #日志窗口
        #self.recordWidget = RecordWidget(self)
        #self.recordWidget.mythread.stop()
        #self.recordWidget.hide()

        #self.toolWidget = ToolWidget()
        #self.toolWidget.hide()

        #创建action
        #self.action_showRecord_A = QAction(self)
        #self.action_closeRecord_B = QAction(self)
        #self.action_showRecord_A.setShortcut(QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_B))
        #self.action_closeRecord_B.setShortcut(QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_C))
        #self.addAction(self.action_showRecord_A)
        #self.addAction(self.action_closeRecord_B)
        
        self.udpClient = UdpClient()
        self.connect(self.udpClient, SIGNAL("start"),self.startB)
        self.connect(self.udpClient, SIGNAL("stop"),self.stopB)
    
    def initLanguage(self):
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
            
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
    
    
    def updateWindow(self,language):
        hintInfo = self.tr("MASSCLOUDS CO.,LTD. Copyright 2014-2018")
        self.copyLabel.setText(hintInfo)
        self.netLabel.setText(self.tr("Can not connect to server, please check network and server address!"))
        self.mainwindow.updateWindow(language)
        #self.recordWidget.updateWindow()
        self.aboutWidget.updateWindow()
        
    def startB(self):
        self.udpClient.show()
        self.setBroadSize()
        
    def setBroadSize(self,width=None,height=None):
        #if self.udpClient.isActiveWindow():
        if width == None:
            widtht = self.getWidth()
            heightt = self.getHeight()
            self.udpClient.setFixedSize(QSize(widtht,heightt))
        else:
            self.udpClient.setFixedSize(QSize(width,height))
        
        self.udpClient.move(QPoint(0,0))
            #self.udpClient.imgLabelTwo.setFixedSize(QSize(QApplication.desktop().width(),QApplication.desktop().height()))
        
    def stopB(self):
        
        self.udpClient.close()

    def bandSignalSlot(self):
        """绑定信号和槽"""
        self.connect(self.mainwindow, SIGNAL("showToolDialog"),self.slotShowToolDialog)
        self.connect(self.mainwindow, SIGNAL("update"),self.slotUpdate)
        self.connect(self.mainwindow, SIGNAL("terminalchange"),self.changeTerminalName)
        self.connect(self.mainwindow, SIGNAL("resetsolution"),self.setPosition)
        self.connect(self.mainwindow, SIGNAL("connectfailed"),self.showNetlabel)
        self.connect(self.mainwindow, SIGNAL("connectsuccess"),self.hideNetlabel)

        #self.connect(self.action_showRecord_A,SIGNAL("triggered()"),self.showRecord)
        #self.connect(self.action_closeRecord_B,SIGNAL("triggered()"),self.closeRecord)

    def showNetlabel(self):
        self.netLabel.show()
        
    def hideNetlabel(self):
        self.netLabel.hide()
        self.udpClient.bindUdpPort()

    def changeTerminalName(self):
        name = globalvariable.TERMINAL_NAME
        self.nameLabel.setText(name)
        self.setPosition()
    
    def showRecord(self):
        self.recordWidget.show()
        self.recordWidget.mythread.start()
        self.recordWidget.move((self.width()-self.recordWidget.width())/2,(self.height()-self.recordWidget.height())/2)
    
    def closeRecord(self):
        self.recordWidget.mythread.stop()
        self.recordWidget.close()
        
        
    def slotShowToolDialog(self, actionType):
        showDlg = None
        if actionType == "showSetting":
            if PasswordDialog().exec_() == QDialog.Accepted:
                showDlg = SettingWidget(self.mainwindow)
                #showDlg.updateWindow()
                showDlg.move(QPoint(self.geometry().width()/9*2,self.geometry().height()/6))
                if self.geometry().width() < 1440:
                    showDlg.resize(QSize(self.geometry().width()/9*5,self.geometry().height()/6*4))
                else:
                    showDlg.resize(QSize(self.geometry().width()/9*5,self.geometry().height()/6*4))
                self.connect(showDlg, SIGNAL("resizePosition"),self.resizePostion)
                self.connect(showDlg, SIGNAL("languagechanged"),self.slotLanguageChange)
                showDlg.exec_()
        elif actionType == "showTerminalTools":
            showDlg = ToolWidget()
            showDlg.move(QPoint(self.geometry().width()/9*2,self.geometry().height()/6))
            showDlg.resize(QSize(self.geometry().width()/9*5,self.geometry().height()/6*4))
            showDlg.exec_()
            #self.toolWidget.show()
            #self.toolWidget.move(QPoint(self.geometry().width()/9*2,self.geometry().height()/6))
            #self.toolWidget.resize(QSize(self.geometry().width()/9*5,self.geometry().height()/6*4))
            
        elif actionType == "showAbout":
            self.aboutWidget.show()
            desktop = QApplication.desktop()
            self.aboutWidget.move((desktop.width() - self.aboutWidget.width())/2, (desktop.height() - self.aboutWidget.height())/2)
#             
    def updateWidgetInfo(self):
        
        self.widthtwo = self.getWidth()/9*2
        self.widthseven = self.getWidth()/9*7
        self.heightone = self.getHeight()/6
        self.heightfive = self.getHeight()/6*5
        
    def updateLinesPath(self):
        """获取四条线路径"""
        self.linesPath = QPainterPath()
        self.linesPath.moveTo(self.widthtwo,self.heightone)
        self.linesPath.lineTo(self.widthseven,self.heightone)
        self.linesPath.moveTo(self.widthtwo,self.heightfive)
        self.linesPath.lineTo(self.widthseven,self.heightfive)
        self.linesPath.moveTo(self.widthtwo,self.heightone)
        self.linesPath.lineTo(self.widthtwo,self.heightfive)
        self.linesPath.moveTo(self.widthseven,self.heightone)
        self.linesPath.lineTo(self.widthseven,self.heightfive)
        self.linesPath.closeSubpath()

    def slotUpdate(self):
        self.setPosition()
        self.setBroadSize()

    def getWidth(self):
        '''desktop = QApplication.desktop()
        width = desktop.width()
        height = desktop.height()'''
        width = "1024"
        resolution = StoreInfoParser.instance().getResolutionValue()
        if resolution == None or resolution == "" or len(resolution.split("x")) != 2:
            width = "1024"
        else:
            width = resolution.split("x")[0]
        return int(width)
    
    def getHeight(self):
        height = "768"
        resolution = StoreInfoParser.instance().getResolutionValue()
        if resolution == None or resolution == "" or len(resolution.split("x")) != 2:
            height = "768"
        else:
            height = resolution.split("x")[1]
        return int(height)
    
    def paintEvent(self,paintEvent):
        """设置背景图片，画线"""
        painter = QPainter(self)
        #设置背景图片
        painter.drawPixmap(self.rect(),QPixmap("images/background.png"))
        #获取四条线路径
        self.updateLinesPath()
        painter.setPen(QPen(QColor(Qt.lightGray),1))
        painter.drawPath(self.linesPath)
#         painter.drawText(QPoint(self.geometry().width()*3/7,self.geometry().height()*21/24), self.tr("乾云启创信息科技有限公司\nCopyright 2014-2018"))
        #painter.drawText(QPoint((self.geometry().width() - infoWidth)*1/2, self.geometry().height()*21/24), hintInfo)
        #painter.drawText(QPoint((self.geometry().width() - infoWidth)*1/2,self.geometry().height()*1/24), globalvariable.TERMINAL_NAME)
    def resizePostion(self, widths, heights):
        #self.setPosition()
        #self.repaint()
        #return
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
            
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
            
        width = int(widths)
        height = int(heights)
        self.mainwindow.move(QPoint(width/9*2,height/6))
        self.mainwindow.resize(QSize(width/9*5,height/6*4))
        self.mainwindow.setPosition()
        
        hintInfo = self.tr("MASSCLOUDS CO.,LTD. Copyright 2014-2018")
        self.copyLabel.setText(hintInfo)
        infoWidth = self.copyLabel.width()
        #self.copyLabel.move(QPoint(self.geometry().width()*3/7,self.geometry().height()*21/24))
        self.copyLabel.move(QPoint((width-infoWidth)/2,height*22/24))
        
        if globalvariable.TERMINAL_NAME:
            info = globalvariable.TERMINAL_NAME
            self.nameLabel.setText(info)
            infoWidth = self.nameLabel.width()
            self.nameLabel.move(QPoint((width - infoWidth)*1/2,height*1/24))
            
        netlabelwidth = self.netLabel.width()
        self.netLabel.move(QPoint((width-netlabelwidth)/2,height*21/24))
        #self.netLabel.move(QPoint(width/9*2,height/6 - 20))
        
        self.widthtwo = width/9*2
        self.widthseven = width/9*7
        self.heightone = height/6
        self.heightfive = height/6*5
        
        self.update()
        
        self.setBroadSize(width,height)
    
    def slotLanguageChange(self,language1):
        
        m_pTranslator = QTranslator()
        exePath = "./"
        if language1 == "chinese":
            mainwindow.language = "chinese"
            QmName = "zh_CN.qm"
        else:
            mainwindow.language = "english"
            QmName = "en_US.qm"
            
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
            
        
        
        self.updateWindow(language1)
        
    def getDesktopWidth(self):
        pass
        
    def setPosition(self):
        self.setMainwindowPosition()
        #self.setTerminalNamePosition()
        #self.setTerminalCopyRight()
        self.updateWidgetInfo()
        #self.setBroadSize()
        self.repaint()
    
    def setMainwindowPosition(self):
        #调整主窗口的位置和大小

        width = self.getWidth()
        height = self.getHeight()
        self.mainwindow.move(QPoint(width/9*2,height/6))
        self.mainwindow.resize(QSize(width/9*5,height/6*4))
        self.mainwindow.setPosition()
    
    def setTerminalCopyRight(self):
        #显示公司信息

        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
            
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
            
        width = self.getWidth()
        height = self.getHeight()
        hintInfo = self.tr("MASSCLOUDS CO.,LTD. Copyright 2014-2018")
        self.copyLabel.setText(hintInfo)
        infoWidth = self.copyLabel.width()
        #self.copyLabel.move(QPoint(self.geometry().width()*3/7,self.geometry().height()*21/24))
        self.copyLabel.move(QPoint((width-infoWidth)/2,height*22/24))
        
    def setTerminalNamePosition(self):
        #显示学生机的名称
        width = self.getWidth()
        height = self.getHeight()
        if globalvariable.TERMINAL_NAME:
            info = globalvariable.TERMINAL_NAME
            self.nameLabel.setText(info)
            infoWidth = self.nameLabel.width()
            self.nameLabel.move(QPoint((width - infoWidth)*1/2,height*1/24))
            
        netlabelwidth = self.netLabel.width()
        self.netLabel.move(QPoint((width-netlabelwidth)/2,height*21/24))
         
    def wheelEvent(self,event):
        """鼠标滚轮滚动事件"""
        self.mainwindow.wheelEvent(event)
        
        
        
