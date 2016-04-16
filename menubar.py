# -*- coding: utf-8 -*-  

from PyQt4.QtCore import QSize, SIGNAL
from PyQt4.QtGui  import QStyle, QHBoxLayout, QIcon, QWidget, QColor

from custombutton import CustomButton, MenuButton


class MenuBar(QWidget):
        
    def __init__(self,parent = None):
        super(MenuBar,self).__init__(parent)
        
        self.freshButton = CustomButton(self)
        self.settingButton = CustomButton(self)
        self.toolButton = CustomButton(self)
        self.aboutButton = CustomButton(self)
        
        self.freshButton.setObjectName("freshButton")
        self.settingButton.setObjectName("settingButton")
        self.toolButton.setObjectName("toolButton")
        self.aboutButton.setObjectName("aboutButton")
        
        self.freshButton.setToolTip(self.tr("refresh"))
        self.settingButton.setToolTip(self.tr("setting"))
        self.toolButton.setToolTip(self.tr("tools"))
        self.aboutButton.setToolTip(self.tr('about'))
        
        self.freshButton.setIcon(QIcon("images/refresh.png"))
        self.settingButton.setIcon(QIcon("images/setting.png"))
        self.toolButton.setIcon(QIcon("images/tools.png"))
        self.aboutButton.setIcon(QIcon("images/about.png"))
                
        self.freshButton.setFlat(True)
        self.settingButton.setFlat(True)
        self.toolButton.setFlat(True)
        self.aboutButton.setFlat(True)
        
        self.freshButton.setIconSize(QSize(30,30))
        self.settingButton.setIconSize(QSize(30,30))
        self.toolButton.setIconSize(QSize(30,30))
        self.aboutButton.setIconSize(QSize(30,30))
        
        self.btnLayout = QHBoxLayout(self)
        
        self.btnLayout.addWidget(self.freshButton)
        self.btnLayout.addWidget(self.settingButton)
        self.btnLayout.addWidget(self.toolButton)
        self.btnLayout.addWidget(self.aboutButton)
        
        self.btnLayout.setSpacing(0)
        self.btnLayout.setMargin(0)
        self.setLayout(self.btnLayout)
        
        self.connect(self.freshButton, SIGNAL("clicked()"),self.slotRefresh)
        
        self.connect(self.toolButton, SIGNAL("clicked()"),self.slotShowToolDialog)
        
        self.connect(self.settingButton, SIGNAL("clicked()"),self.slotShowToolDialog)
        
        self.connect(self.aboutButton, SIGNAL("clicked()"),self.slotShowToolDialog)
    
    
    def updateWindow(self):
        self.freshButton.setToolTip(self.tr("refresh"))
        self.settingButton.setToolTip(self.tr("setting"))
        self.toolButton.setToolTip(self.tr("tools"))
        self.aboutButton.setToolTip(self.tr('about'))
        
    def slotRefresh(self):
        self.emit(SIGNAL("refresh"))
        
    def slotShowToolDialog(self):
        objName = self.sender().objectName()
        if objName == "settingButton":
            self.emit(SIGNAL("showToolDialog"), "showSetting")
        elif objName == "toolButton":
            self.emit(SIGNAL("showToolDialog"), "showTerminalTools")
        elif objName == "aboutButton":
            self.emit(SIGNAL("showToolDialog"), "showAbout")
            
  