# -*- coding: utf-8 -*-  

from PyQt4.QtGui import QWidget, QTabWidget, QPainter, QFont, QLinearGradient, QColor, QIcon, QStyle, QBrush, QPushButton
from PyQt4.QtCore import Qt, QRect, QPoint, SIGNAL
from tabbar import TabBar

class TabWidget(QTabWidget):
       
    def __init__(self,parent = None):
        super(TabWidget,self).__init__(parent)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("QTabBar::tab {   "
                            "height: 40px; "
                            "width: 120px;"
                            "margin-top: 10px;"
                            "margin-left: 10px;"
                            "margin-bottom: 1px;"
                            "border-radius:1px;"   
                            "color: rgb(255, 255, 255);"         
                            "background: rgb(100,100,100,0)"
                            "}"
                            
                            "QTabBar::tab:selected{"
                            "background: rgb(255,255,255);"
                            "color: rgb(1, 1, 1);"
                            "}"
                            "QTabBar::tab:!selected:hover{"
                            "background: rgb(8,80,176);"
                            
                            "}"
                            )
       
        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon("images/close.png"))
        self.closeButton.setFlat(True)      
#         self.closeButton.setStyleSheet("QPushButton::hover{background:rgb(50, 150, 255);};")
        
        self.mousePressed = False
               
        self.connect(self.closeButton, SIGNAL("clicked()"),self.closeWidget)
        
        self.setTabBar(TabBar(self))
        
    def closeBtn(self):
        return self.closeButton
        
    def closeWidget(self):
        self.emit(SIGNAL("closeWidget"))
        
    # 分割线
    def addSeperator(self):
        self.setTabEnabled(self.addTab(QWidget(self), "|"),False)
       
    def paintEvent(self,event):
        # 自定义标题，添加关闭按钮
        painter = QPainter(self)
        linearGradient = QLinearGradient(0, 0,0,self.tabBar().frameGeometry().height())
        linearGradient.setColorAt(0, QColor(60,150,255))
        linearGradient.setColorAt(0.1, QColor(6,88,200))
        linearGradient.setColorAt(1, QColor(80,150,255))
        painter.setBrush(QBrush(linearGradient))
        
        self.menuRect = QRect(0, 0, self.frameGeometry().width(), self.tabBar().height() - 1)#菜单矩形
        
        painter.fillRect(self.menuRect, QBrush(linearGradient))#填充
        
        painter2 = QPainter(self)#画
        brush2 = QBrush(QColor(242,242,242))#笔刷
        painter2.setBrush(brush2)#为画定义笔刷
        self.contenRect2 = QRect(0,self.tabBar().height(),self.frameGeometry().width(),self.frameGeometry().height())
        painter2.fillRect(self.contenRect2, brush2)
        
        self.closeButton.setFixedSize(30,30)
        self.closeButton.move(QPoint(self.geometry().width()-self.closeButton.frameGeometry().width() - 10,
                              (self.tabBar().height()-self.closeButton.frameGeometry().height())/2)) #关闭按钮的位置设定



   
    




