# -*- coding: utf-8 -*-  
from PyQt4.QtCore import Qt, QRect
from PyQt4.QtGui  import QPushButton, QPainter, QPainterPath,QVBoxLayout, QPen,QLabel,QProgressBar, QColor, QPixmap, QIcon, QBrush, QCursor,QMenu,QWidget,QHBoxLayout

class WidgetProgress(QWidget):
    def __init__(self,parent = None):
        super(WidgetProgress,self).__init__(parent)
        self.setStyleSheet("QProgressBar{"
                                        "color:black;"
                                        "border: 1px solid #808080;"
                                        "text-align: center;"
                                        "background-color:white;"
                                         "}"
                            "QProgressBar::chunk {"
                                            
                                            "background-color:rgb(128,128,255);"
                                            "margin: 0.5px;"
                                            "}")
        
        self.tipLabel = QLabel(self.tr("downloading..."))
        self.progressBar = QProgressBar()
        #self.progressBar.setValue(0)
        self.progressBar.setFixedWidth(140)
        labelLayout = QHBoxLayout()
        labelLayout.addSpacing(20)
        labelLayout.addWidget(self.tipLabel)
        labelLayout.addStretch()
         
        progressLayout = QHBoxLayout()
        progressLayout.addStretch()
        progressLayout.addWidget(self.progressBar)
        progressLayout.addStretch()
         
         
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addLayout(labelLayout)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addLayout(progressLayout)
        self.mainLayout.addStretch()
        
        
        
        self.hovered = False
        self.pressed = False
        self.pressedIcon = QIcon()
        self.color = QColor(Qt.gray)
        self.opacity = 1.0
        self.count = 0
#         self.setAutoFillBackground(True)
#         self.setStyleSheet("#Check {background-color: rgb(255, 255, 255);}");
        #self.createContextMenu()  
        self.count = 0
    def setVmName(self,name):
        self.vmname = name
        text = self.tr("course ") + self.vmname + u" downloading..."
        self.tipLabel.setText(text)
    def createContextMenu(self):  
        ''''' 
        创建右键菜单 
        '''  
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu  
        # 否则无法使用customContextMenuRequested信号  
        self.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.customContextMenuRequested.connect(self.showContextMenu) 
         
        # 创建QMenu  
        self.contextMenu = QMenu(self)  
        self.actionA = self.contextMenu.addAction(QIcon("images/0.png"),u'|  动作A')  
        self.actionB = self.contextMenu.addAction(QIcon("images/0.png"),u'|  动作B')  
        self.actionC = self.contextMenu.addAction(QIcon("images/0.png"),u'|  动作C') 
        #添加二级菜单
        self.second = self.contextMenu.addMenu(QIcon("images/0.png"),u"|  二级菜单") 
        self.actionD = self.second.addAction(QIcon("images/0.png"),u'|  动作A')
        self.actionE = self.second.addAction(QIcon("images/0.png"),u'|  动作B')
        self.actionF = self.second.addAction(QIcon("images/0.png"),u'|  动作C')
        # 将动作与处理函数相关联  
        # 这里为了简单，将所有action与同一个处理函数相关联，  
        # 当然也可以将他们分别与不同函数关联，实现不同的功能  
        self.actionA.triggered.connect(self.actionHandler)  
        self.actionB.triggered.connect(self.actionHandler)  
        self.actionC.triggered.connect(self.actionHandler) 
        self.actionD.triggered.connect(self.actionHandler)  
        self.actionE.triggered.connect(self.actionHandler)  
        self.actionF.triggered.connect(self.actionHandler)   
  
    def showContextMenu(self, pos):  
        ''''' 
        右键点击时调用的函数 
        '''  
        self.count+=1
        # 菜单显示前，将它移动到鼠标点击的位置  
        self.contextMenu.exec_(QCursor.pos()) #在鼠标位置显示
        #self.contextMenu.show()  
    def text(self):
        return ""
    def icon(self):
        return ""
    def actionHandler(self):  
        ''''' 
        菜单中的具体action调用的函数 
        '''  
        if self.count%3==1:
            self.setText(u"first")
        elif self.count%3==2:
            self.setText(u"second")
        elif self.count%3==0:
            self.setText(u"third")

    def setEnterCursorType(self, Type):
        self.cursorType = Type
        
    def setColor(self,color):
        self.color = color
        
    def setOpacitys(self,opacity):
        self.opacity = opacity
#         self.setOpacity(0.5)
    def enterEvent(self,event):
        self.hovered = True
        self.repaint()
        QPushButton.enterEvent(self,event)
        
    def leaveEvent(self,event):
        self.hovered = False
        self.repaint()
        self.setCursor(QCursor(Qt.ArrowCursor)) 
        QPushButton.leaveEvent(self,event)
        
    '''def mousePressEvent(self, event):
        self.pressed = True
        self.repaint()
        QPushButton.mousePressEvent(self,event)
    
    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.repaint()
        QPushButton.mouseReleaseEvent(self,event)'''
                
    def paintEvent(self,event):
        painter = QPainter(self)
        btnRect = self.geometry()
        iconRect = QRect(5,5,self.geometry().width()-5,self.geometry().height()-5)
        
        color = QColor(Qt.black)
        if self.hovered:
            color = self.color
        if self.pressed:
            color = self.color.darker(120)
        
        painter.setPen(QPen(QColor(Qt.lightGray),2))
        outline = QPainterPath()
        outline.addRoundedRect(0, 0, btnRect.width(), btnRect.height(), 0, 0)
        painter.setOpacity(1)
        painter.drawPath(outline)
       
        painter.setBrush(QBrush(color)) 
        painter.setOpacity(self.opacity)
        painter_path = QPainterPath()
        painter_path.addRoundedRect(1, 1, btnRect.width() - 2, btnRect.height() - 2, 0, 0)
        if self.hovered:
            painter.setClipPath(painter_path)
            painter.drawRoundedRect(1, 1, btnRect.width() - 2, btnRect.height() - 2, 0, 0)
        
        painter.setOpacity(1)       
        
        iconPos,textPos = self.calIconTextPos(btnRect, iconRect)
        # 重画文本
        if not self.text() == "":
            painter.setFont(self.font())
            painter.setPen(QPen(QColor(Qt.black),2))
            painter.drawText(textPos.x(), textPos.y(), textPos.width(), textPos.height(), Qt.AlignCenter, self.text())
            # 重画图标
        if not self.icon() == "":
            painter.drawPixmap(iconPos, QPixmap(self.icon().pixmap(self.iconSize())))
            
    # 计算图标和文本大小位置
    def calIconTextPos(self,btnSize,iconSize):
        if self.text() == "":
            iconWidth = iconSize.width()*3/5
            iconHeight = iconSize.height()*3/5
        else:
            iconWidth = iconSize.width()
            iconHeight = iconSize.height() - 50
            
        iconX = (btnSize.width()-iconWidth)/2
        iconY = (btnSize.height()-iconHeight)/2
        
        iconPos = QRect()
        iconPos.setX(iconX)
        iconPos.setY(iconY)
        iconPos.setWidth(iconWidth)
        iconPos.setHeight(iconHeight)
        
        textPos = QRect()
        if not self.text() == "":
            textPos.setX(iconX)
            textPos.setY(btnSize.height()- 50)
            textPos.setWidth(iconWidth)
            textPos.setHeight(50)
        return (iconPos,textPos)
