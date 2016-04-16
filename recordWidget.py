#coding:utf-8
'''
Created on 2014-8-19

@author: root
'''
from PyQt4.QtGui import QWidget,QTextBrowser,QHBoxLayout,QTextCursor,QApplication,QPushButton,QIcon,QPainter,QLinearGradient,QBrush,QColor,QLabel,QFont
from PyQt4.QtCore import SIGNAL,Qt,QRect,QString, QTranslator, QCoreApplication
from myTipThread import MyThread
import sys
from storeinfoparser import StoreInfoParser
class RecordWidget(QWidget):
    def __init__(self,parent=None):
        super(RecordWidget,self).__init__(parent)
        self.setFixedSize(900,400)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.setStyleSheet("QTextBrowser{border:5px;}"
                           "QTextBrowser{background:black;}"
                           "QTextBrowser{color:white;}"
                           "QTextBrowser{font-size:15px;}")
        
        self.topLine = 50
        self.mythread = MyThread()
        self.mythread.start()
        
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setFixedSize(self.geometry().width()-20,self.geometry().height()-self.topLine-45)
        self.textBrowser.move(10,self.topLine)
        
        self.pauseButton = QPushButton(self)
        self.pauseButton.setFixedSize(880,30)
        self.pauseButton.setText(self.tr("Pause"))
        self.pauseButton.move(10,self.height()-40)
        self.pauseButton.setStyleSheet("QPushButton{background:rgb(180,200,255);}"
                                       "QPushButton{border:0px;}"
                                       "QPushButton:hover{background:rgb(100,100,100);}"
                                       "QPushButton:pressed{background:rgb(80,0,255);}")
        self.connect(self.pauseButton, SIGNAL("clicked()"),self.pauseThread)
        
        
        self.closeButton = QPushButton(self)
        self.closeButton.setFixedSize(30,30)
        self.closeButton.setIcon(QIcon("images/close.png"))
        self.closeButton.setStyleSheet("QPushButton{border:0px;}"
                                       "QPushButton:hover{background:rgb(180,200,255);}"
                                       "QPushButton:pressed{background:rgb(80,0,255);}")
        self.closeButton.move(self.geometry().width()-35,5)
        
        self.connect(self.closeButton,SIGNAL("clicked()"),self.cancel)
        
        
        #self.mainLayout = QHBoxLayout(self)
        #self.mainLayout.setMargin(0)
        #self.mainLayout.addSpacing(30)
        #self.mainLayout.addWidget(self.textBrowser)
        
        self.connect(self.mythread, SIGNAL("getoutput"),self.output)
        
        self.tipText = QLabel(self.tr("Student Computer Log"),self)
        self.tipText.setFont(QFont("times",15,QFont.Bold))
        self.tipText.move(5,5)
        
        
        self.mousePressed = False
    
    def updateWindow(self):
        self.tipText.setText(self.tr("Student Computer Log"))
        self.pauseButton.setText(self.tr("Pause"))
        self.mythread.start()
    
    def pauseThread(self):
        
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
            
        if self.pauseButton.text() == self.tr("Pause"):
            self.mythread.stop()
            self.pauseButton.setText(self.tr("Restart"))
        elif self.pauseButton.text() == self.tr("Restart"):
            self.mythread.start()
            self.pauseButton.setText(self.tr("Pause"))
    def cancel(self):
        self.mythread.stop()
        self.close()
    def output(self, text):
        self.textBrowser.clear()
        self.textBrowser.setText(self.trUtf8(text))
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textBrowser.setTextCursor(cursor)
        
    def mouseMoveEvent(self,event):
        if self.mousePressed:
            self.move(self.pos() + event.pos() - self.currentPos)   
        
    def mousePressEvent(self,event):
        if event.buttons() == Qt.LeftButton:
            self.currentPos = event.pos()
            self.mousePressed = True
    def mouseReleaseEvent(self,event):
        if event.buttons() == Qt.LeftButton:
            self.mousePressed = False
            
    def paintEvent(self,event):
        painter = QPainter(self)
        painter.save()
        linearGradient = QLinearGradient(0,0,0,self.geometry().width())
        linearGradient.setColorAt(0, QColor(60,150,255))
        linearGradient.setColorAt(0.1, QColor(6,88,200))
        linearGradient.setColorAt(1, QColor(80,150,255))
        painter.setBrush(QBrush(linearGradient))
        contenRect = QRect(0, 0, self.width(), self.topLine-10)
        painter.fillRect(contenRect, QBrush(linearGradient))
        painter.restore()
        
        painterBack = QPainter(self)
        backBrush = QBrush(QColor(200,200,250))
        painterBack.setBrush(backBrush)
        backRect = QRect(0,self.topLine-10,self.width(),self.height())
        painterBack.fillRect(backRect, backBrush)

        
        
