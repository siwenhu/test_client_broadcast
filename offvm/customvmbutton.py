# -*- coding: utf-8 -*-  

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui  import QCursor, QMenu, QAction, QWidget, QLabel, QHBoxLayout, QWidgetAction, QColor
from custombutton import CustomButton
from logrecord import LogRecord
import globalvariable


class CustomVMButton(CustomButton):
        
    def __init__(self,parent = None):
        super(CustomVMButton,self).__init__(parent)
        
        self.setAutoFillBackground(True)
        self.vmInfo = {}
        
        '''self.closeAction = QAction(u"关闭", self)
        self.rebootAction = QAction(u"重启", self)
        self.resetAction = QAction(u"还原", self)
        
        self.connect(self.closeAction, SIGNAL("triggered()"), self.closeVM)
        self.connect(self.rebootAction, SIGNAL("triggered()"), self.startVM)
        self.connect(self.resetAction, SIGNAL("triggered()"), self.resetVM)'''
        
    def closeVM(self):
        self.emit(SIGNAL("controlvm"), "poweroff")
        
    def startVM(self):
        self.emit(SIGNAL("controlvm"), "start")
        
    def resetVM(self):
        self.emit(SIGNAL("controlvm"), "reset")
        
    def setVMInfo(self, vmInfo):
        self.vmInfo = vmInfo
        
    def getVMInfo(self):
        return self.vmInfo
    
#     def contextMenuEvent(self, event):
#         if globalvariable.CLASS_STATUS:
#             top_widget = QWidget()
#             hintLabel = QLabel(u"出故障了？请尝试")
#             hintLabel.setAlignment(Qt.AlignHCenter)
#             hintLabel.setStyleSheet("color:blue;");
#             layout = QHBoxLayout()
#             layout.addWidget(hintLabel)
#             top_widget.setLayout(layout)
#             
#             menu = QMenu(self)
#             menu.setStyleSheet("background:rgb(216, 239, 233);border:1px;border-color:green");
#             top_widget_action = QWidgetAction(menu)
#             top_widget_action.setDefaultWidget(top_widget)
#             menu.addAction(top_widget_action)
#             menu.addSeparator()
#             menu.addAction(self.closeAction)
#             menu.addAction(self.rebootAction)
#             menu.addAction(self.resetAction)
#             menu.exec_(QCursor.pos());
#             event.accept();


