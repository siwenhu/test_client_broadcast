# -*- coding: utf-8 -*-  

from PyQt4.QtCore import Qt, QRect
from PyQt4.QtGui  import QPushButton, QPainter, QPainterPath, QPen, QColor, QPixmap, QIcon, QBrush, QCursor

class MenuButton(QPushButton):
        
    def __init__(self,parent = None):
        super(MenuButton,self).__init__(parent)
        
        self.setFlat(True)
        self.hovered = False
        self.pressed = False
        self.color = QColor(Qt.lightGray)
        
    def enterEvent(self,event):
        self.hovered = True
        self.repaint()
        QPushButton.enterEvent(self,event)
        
    def leaveEvent(self,event):
        self.hovered = False
        self.repaint()
        QPushButton.leaveEvent(self,event)
        
    def mousePressEvent(self, event):
        self.pressed = True
        self.repaint()
        QPushButton.mousePressEvent(self,event)
    
    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.repaint()
        QPushButton.mouseReleaseEvent(self,event)
    
    def setColor(self,color):
        self.color = color

    def paintEvent(self,event):
        painter = QPainter(self)
        btnRect = self.geometry()
        
        color = QColor(Qt.black)
        if self.hovered:
            color = self.color
        if self.pressed:
            color = self.color.darker(120)
            
        painter.setBrush(QBrush(color)) 
        painter_path = QPainterPath()
        painter_path.addRoundedRect(1, 1, btnRect.width() - 2, btnRect.height() - 2, 0, 0)
        
        if self.hovered:
            painter.setPen(QPen(color,2))
            outline = QPainterPath()
            outline.addRoundedRect(0, 0, btnRect.width(), btnRect.height(), 0, 0)
            painter.setOpacity(1)
            painter.drawPath(outline)
            painter.setClipPath(painter_path)
            painter.drawRoundedRect(1, 1, btnRect.width() - 2, btnRect.height() - 2, 0, 0)
        
        iconWidth = self.iconSize().width()*3/5
        iconHeight = self.iconSize().height()*3/5
        iconX = (btnRect.width()-iconWidth)/2
        iconY = (btnRect.height()-iconHeight)/2
        
        if self.pressed:
            iconX += 2
            iconY += 2
        
        iconPos = QRect()
        iconPos.setX(iconX)
        iconPos.setY(iconY)
        iconPos.setWidth(iconWidth)
        iconPos.setHeight(iconHeight)
        
        painter.drawPixmap(iconPos, QPixmap(self.icon().pixmap(self.iconSize())))

class CustomButton(QPushButton):
        
    def __init__(self,parent = None):
        super(CustomButton,self).__init__(parent)
        
        self.hovered = False
        self.pressed = False
        self.pressedIcon = QIcon()
        self.color = QColor(Qt.gray)
        self.opacity = 1.0
        
#         self.setAutoFillBackground(True)
#         self.setStyleSheet("#Check {background-color: rgb(255, 255, 255);}");

        
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
        
    def mousePressEvent(self, event):
        self.pressed = True
        self.repaint()
        QPushButton.mousePressEvent(self,event)
    
    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.repaint()
        QPushButton.mouseReleaseEvent(self,event)
                
    def paintEvent(self,event):
        painter = QPainter(self)
        btnRect = self.geometry()
        iconRect = self.iconSize()
        
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
        if not self.text().isNull():
            painter.setFont(self.font())
            painter.setPen(QPen(QColor(Qt.black),2))
            painter.drawText(textPos.x(), textPos.y(), textPos.width(), textPos.height(), Qt.AlignCenter, self.text())
            # 重画图标
        if not self.icon().isNull():
            painter.drawPixmap(iconPos, QPixmap(self.icon().pixmap(self.iconSize())))
            
    # 计算图标和文本大小位置
    def calIconTextPos(self,btnSize,iconSize):
        if self.text().isNull():
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
        if not self.text().isNull():
            textPos.setX(iconX)
            textPos.setY(btnSize.height()- 50)
            textPos.setWidth(iconWidth)
            textPos.setHeight(50)
        return (iconPos,textPos)
   