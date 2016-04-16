
# -*- coding: utf-8 -*-  

from PyQt4.QtGui import QFont, QPainter, QBrush, QPalette
from PyQt4.QtGui import QColor, QDialog
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QLabel, QPixmap,QWidget
from PyQt4.QtCore import Qt, SIGNAL, QEvent, QRect, QTranslator,\
    QCoreApplication

from tabwidget import TabWidget
import globalfunc
        
class AboutTab(QWidget):
       
    def __init__(self,parent = None):
        super(AboutTab,self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        version, rDate = globalfunc.getVersionAndReleaseDate()
        textpalette = QPalette()
        textpalette.setColor(QPalette.WindowText, QColor(33,97,143))
        self.adminLabel = QLabel(self.tr("Mcos-student"))
        self.adminLabel.setFixedWidth(200)
        self.adminLabel.setFont(QFont("simhei",20))
        self.adminLabel.setPalette(textpalette)
        if version:
            self.banbenLabel = QLabel(self.tr("Version:") + "%s" % version)
            self.banbenLabel.setPalette(textpalette)
        else:
            self.banbenLabel = QLabel()
            
        if rDate:
            self.releaseDate = QLabel(self.tr("Version Time:") + "%s" % rDate)
            self.releaseDate.setPalette(textpalette)
        else:
            self.releaseDate = QLabel()
        textLayout = QVBoxLayout()
        textLayout.addWidget(self.adminLabel)
        textLayout.addWidget(self.banbenLabel)
        textLayout.addWidget(self.releaseDate)
        textLayout.setMargin(20)
        textLayout.setSpacing(20)
        
        
        self.logoLabel = QLabel()
        self.logoLabel.setPixmap(QPixmap("images/productlogo.png"))
   
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.logoLabel)
        mainLayout.addLayout(textLayout)
        mainLayout.setMargin(50)
        
        self.setLayout(mainLayout)
        
    def updateWindow(self):
        version, rDate = globalfunc.getVersionAndReleaseDate()
        self.adminLabel.setText(self.tr("Mcos-student"))
        self.banbenLabel.setText(self.tr("Version:") + "%s" % version)
        self.releaseDate.setText(self.tr("Version Time:") + "%s" % rDate)
        
        
class AboutWidget(QWidget):
       
    def __init__(self,parent = None):
        super(AboutWidget,self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        #self.setWindowModality(Qt.WindowModal)
        self.tabWidget = TabWidget(self)
        self.aboutTab = AboutTab()
        self.tabWidget.addTab(self.aboutTab,self.tr("About"))
        self.tabWidget.setHasUnderLine(False)
        
        mainLayout = QVBoxLayout()
        mainLayout.setMargin(0)
        mainLayout.setSpacing(0)
        mainLayout.addWidget(self.tabWidget)
        self.setLayout(mainLayout)
        
        self.mousePressed = False
        
        self.tabWidget.closeBtn().installEventFilter(self)
    
        self.connect(self.tabWidget, SIGNAL("closeWidget"),self.close)
    
    def updateWindow(self):
#         m_pTranslator = QTranslator()
#         exePath = "/root/workspace/nwclient/"
#         language1 = "chinese"
#         if language1 == "chinese":
#             QmName = "zh_CN.qm"
#         else:
#             QmName = "en_US.qm"
#             
#         if(m_pTranslator.load(QmName, exePath)):
#             QCoreApplication.instance().installTranslator(m_pTranslator)
            
        self.aboutTab.updateWindow()
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.aboutTab,self.tr("About"))
        
    def eventFilter(self, target, event):
        if target == self.tabWidget.closeBtn():
            if event.type() == QEvent.Enter:
                self.tabWidget.closeBtn().setStyleSheet("background:rgb(255, 255, 255)")
                self.tabWidget.closeBtn().setAutoFillBackground(True);
            elif event.type() == QEvent.Leave:
                self.tabWidget.closeBtn().setAutoFillBackground(False);
                return True
            
        return QWidget.eventFilter(self, target, event)
    
    # 添加鼠标移动窗口
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
        painterBack = QPainter(self)
        backBrush = QBrush(QColor(244,250,250))
        painterBack.setBrush(backBrush)
        backRect = QRect(0,0,self.width(),self.height())
        painterBack.fillRect(backRect, backBrush)
            
