# -*- coding: utf-8 -*-  

from PyQt4.QtGui  import QTabBar, QFont, QColor, QPen, QPainterPath, QPainter
from PyQt4.QtCore import QPoint

class TabBar(QTabBar):
       
    def __init__(self,parent = None):
        super(TabBar,self).__init__(parent)
       
        self.hoveredTab = 0
        self.setMouseTracking(True)
        self.setFont(QFont("simhei", 15));
   
#     def leaveEvent(self,event):
#         self.hoveredTab = self.currentIndex ()
#         self.repaint()
#         QTabBar.leaveEvent(self,event)
           
#     def paintEvent(self,event):
#         painter = QPainter(self)
#         rect = self.tabRect(self.currentIndex ())
#         linesPath = QPainterPath()
#         linesPath.moveTo(QPoint(rect.x()+10,rect.height()-5))
#         linesPath.lineTo(QPoint(rect.x()-10+rect.width(),rect.height()-5))
#         linesPath.closeSubpath()
#         painter.setPen(QPen(QColor(87,192,2),6))
#         painter.drawPath(linesPath)
#         # 如果不是当前选中的页，在页标签下画线
#         if self.hoveredTab != self.currentIndex ():
#             if self.isTabEnabled(self.hoveredTab):
#                 rect = self.tabRect(self.hoveredTab)
#                 linesPath = QPainterPath()
#                 linesPath.moveTo(QPoint(rect.x()+10,rect.height()-5))
#                 linesPath.lineTo(QPoint(rect.x()-10+rect.width(),rect.height()-5))
#                 linesPath.closeSubpath()
#                 painter.setPen(QPen(QColor(170,200,200),6))
#                 painter.drawPath(linesPath)
#         QTabBar.paintEvent(self,event)
#        



#     def mouseMoveEvent(self,event):
#         index = 0
#         while(index < self.count()):
#             if self.tabRect(index).contains(event.pos(),True):
#                 self.hoveredTab = index
#                 self.repaint()
#                 break
#             index += 1
#         QTabBar.mouseMoveEvent(self,event)

