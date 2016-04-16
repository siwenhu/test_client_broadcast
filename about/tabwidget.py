# -*- coding: utf-8 -*-  

from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import Qt,QString
from PyQt4.QtGui  import QPainter
from PyQt4.QtGui  import QPainterPath
from PyQt4.QtGui  import QPen
from PyQt4.QtGui  import QColor
from PyQt4.QtGui  import QIcon
from PyQt4.QtGui  import QStyle
from PyQt4.QtGui  import QBrush
from PyQt4.QtGui  import QPushButton
from PyQt4.QtCore import QRect
from PyQt4.QtCore  import QPoint
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QFont
from PyQt4.QtCore import SLOT
from PyQt4.QtGui  import QTabBar,QLinearGradient,QLabel,QPalette

class TabBar(QTabBar):
       
    def __init__(self,parent = None):
        super(TabBar,self).__init__(parent)
       
        self.hoveredTab = 0
        self.setMouseTracking(True)
        self.hasUnderLine = True
        self.textLabel = QLabel(self)
        self.setFont(QFont("Times New Roman", 15))
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(255,255,255))
        self.setPalette(palette)
   
    def leaveEvent(self,event):
        self.hoveredTab = self.currentIndex ()
        self.repaint()
        QTabBar.leaveEvent(self,event)
        
    def setHasUnderLine(self,flag):
        self.hasUnderLine = flag
           
    def paintEvent(self,event):
        painter = QPainter(self)
        if self.hasUnderLine:
            rect = self.tabRect(self.hoveredTab)
            linesPath = QPainterPath()
            linesPath.moveTo(QPoint(rect.x()+10,rect.height()-5))
            linesPath.lineTo(QPoint(rect.x()-10+rect.width(),rect.height()-5))
            linesPath.closeSubpath()
            painter.setPen(QPen(QColor(170,200,200),6))
            painter.drawPath(linesPath)
            # 如果不是当前选中的页，在页标签下画线
            if self.hoveredTab != self.currentIndex ():
                if self.isTabEnabled(self.hoveredTab):
                    rect = self.tabRect(self.hoveredTab)
                    linesPath = QPainterPath()
                    linesPath.moveTo(QPoint(rect.x()+10,rect.height()-5))
                    linesPath.lineTo(QPoint(rect.x()-10+rect.width(),rect.height()-5))
                    linesPath.closeSubpath()
                    painter.setPen(QPen(QColor(170,200,200),6))
                    painter.drawPath(linesPath)
        QTabBar.paintEvent(self,event)
       
    def mouseMoveEvent(self,event):
        index = 0
        while(index < self.count()):
            if self.tabRect(index).contains(event.pos(),True):
                self.hoveredTab = index
                self.repaint()
                break
            index += 1
        QTabBar.mouseMoveEvent(self,event)

class TabWidget(QTabWidget):
       
    def __init__(self,parent = None):
        super(TabWidget,self).__init__(parent)
       
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("QTabBar::tab {   "
                            "height: 40px; "
                            "background: rgb(214,214,214,0)   "
                            "}")
        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon("images/close.png"))
        self.closeButton.setFlat(True)      
        self.mousePressed = False
               
        self.connect(self.closeButton, SIGNAL("clicked()"),self.closeWidget)
        
        self.setTabBar(TabBar(self))
       
    def closeBtn(self):
        return self.closeButton
        
    def closeWidget(self):
        self.emit(SIGNAL("closeWidget"))
        
    def setHasUnderLine(self,flag):
        self.tabBar().setHasUnderLine(flag)
       
    # 分割线
    def addSeperator(self):
        self.setTabEnabled(self.addTab(QWidget(self), "|"),False)
       
    def paintEvent(self,event):
        # 自定义标题，添加关闭按钮
        painter = QPainter(self)
        linearGradient = QLinearGradient(0, 0,0,self.tabBar().frameGeometry().height())
        linearGradient.setColorAt(0, QColor(60,150,255))
        linearGradient.setColorAt(0.05, QColor(6,88,200))
        linearGradient.setColorAt(1, QColor(80,150,255))
        painter.setBrush(QBrush(linearGradient))
        self.menuRect = QRect(0, 0, self.frameGeometry().width(), self.tabBar().height())
        painter.fillRect(self.menuRect, QBrush(linearGradient))
        self.closeButton.move(QPoint(self.geometry().width()-self.closeButton.frameGeometry().width(),
                              (self.tabBar().height()-self.closeButton.frameGeometry().height())/2))
        
       
   

