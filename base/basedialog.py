# -*- coding: utf-8 -*-  

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog
                        

class BaseDialog(QDialog):
        
    def __init__(self,parent = None):
        super(BaseDialog,self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.mousePressed = False
        
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
            
            