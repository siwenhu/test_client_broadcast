# -*- coding: utf-8 -*-  

from PyQt4.QtCore import Qt, SIGNAL, QRect, QPoint, QTranslator,\
    QCoreApplication
from PyQt4.QtGui import QDialog, QLabel, QPainter, QBrush, QColor, QPushButton, QPen, QLinearGradient, QFontMetrics
from basedialog import BaseDialog          
from storeinfoparser import StoreInfoParser

class InfoHintDialog(BaseDialog):
        
    def __init__(self, hintInfo, parent = None):
        super(InfoHintDialog,self).__init__(parent)
        
        self.setFixedSize(480, 290)
        
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
        
        self.okBtn = QPushButton(self.tr("OK"), self)
        self.okBtn.setStyleSheet("background: rgb(7,87,198); color: white; width: 70px; height: 20px;font-size : 16px;")
        
        self.setTitle(self.tr("Tip Information"))
        
        self.hintInfo = hintInfo
        
        self.okBtn.move((self.width() - self.okBtn.width())/2, self.height() - self.okBtn.height() - 10)
        
        self.connect(self.okBtn, SIGNAL("clicked()"),self.slotOk)
    
    def updateWindow(self):
        
        #self.setTitle(self.tr("Tip Information"))
        self.okBtn.setText(self.tr("OK"))
        
    def slotOk(self):
        self.accept()
        
    def setTitle(self, title):
        self.title = title
        
    def setHintInfo(self, hintInfo):
        
        self.hintInfo = hintInfo
        self.updateWindow()
        self.update()
        
    def paintEvent(self,event):
        titleHeight = 40
        bottomHeight = 50
        
        #画标题背景
        painter = QPainter(self)
        painter.save()
        linearGradient = QLinearGradient(0, 0,0,titleHeight)
        linearGradient.setColorAt(0, QColor(60,150,255))
        linearGradient.setColorAt(0.1, QColor(6,88,200)) 
        linearGradient.setColorAt(1, QColor(80,150,255))
        painter.setBrush(QBrush(linearGradient))
        contenRect = QRect(0, 0, self.width(), titleHeight)
        painter.fillRect(contenRect, QBrush(linearGradient))
        painter.restore()
        
        #画标题内容
        painter.save()
        painter.setPen(QPen(QColor(255, 255, 255),1))
        font = painter.font()
        font.setPointSize(12)
        painter.setFont(font)
        painter.drawText(QPoint(10,25), self.title)
        painter.restore()
        
        #画中间白色背景
        painter.save()
        painter.setPen(QPen(QColor(255, 255, 255),1))
        brush = QBrush(QColor(242,242,242))
        painter.setBrush(brush)
        contenRect = QRect(0, titleHeight, self.width()-1, self.height() - titleHeight - bottomHeight)
#         painter.fillRect(contenRect, brush)
        painter.drawRect(contenRect)
        painter.restore()
        
        #画提示信息内容
        painter.save()
        painter.setPen(QPen(QColor(1, 1, 1),1))
        font = painter.font()
        font.setPointSize(15)
        painter.setFont(font)
        fm = QFontMetrics(font)
        infoWidth = fm.width(self.hintInfo)
        painter.drawText(QPoint((self.width() - infoWidth - 10)/2, 150), self.hintInfo)
        painter.restore()
        
        #画底层背景
        painter.save()
        brush = QBrush(QColor(219,234,255))
        painter.setBrush(brush)
        contenRect = QRect(0, self.height() - bottomHeight, self.width(), bottomHeight)
        painter.fillRect(contenRect, brush)
        painter.restore()
        
        
        
        
        