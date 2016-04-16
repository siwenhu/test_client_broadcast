# -*- coding: utf-8 -*-  

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QWidget, QLabel, QSlider, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox
import os
from configFileParser import ConfigFileParser
from base.infohintdialog import InfoHintDialog
from storeinfoparser import StoreInfoParser

class VolumeSettingWidget(QWidget):
        
    def __init__(self, app, parent = None):
        super(VolumeSettingWidget,self).__init__(parent)
        self.setStyleSheet("font-size : 16px")
        self.app = app
        
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setFixedSize(300, 10)
        
        #读取配置文件，获取音量值
        self.volumeValue = self.getVolumeValue()
        self.volumeSlider.setValue(int(self.volumeValue.split("%")[0]))
        volumeLabel = QLabel(u'音量大小')    
        self.volumeValueLabel = QLabel() 
        self.volumeValueLabel.setText(self.volumeValue)
        
        gridLayout = QGridLayout()
        gridLayout.setSpacing(15)
        gridLayout.setMargin(10)
        gridLayout.addWidget(volumeLabel, 0, 0, 1, 1)
        gridLayout.addWidget(self.volumeValueLabel, 0, 1, 1, 1)
        gridLayout.addWidget(self.volumeSlider, 1, 1, 1, 3)
        
        topLayout = QHBoxLayout()
        topLayout.addStretch()
        topLayout.addSpacing(50)
        topLayout.addLayout(gridLayout)
        topLayout.addStretch(1)
        
        vLayout = QVBoxLayout()
        vLayout.addStretch()
        vLayout.addSpacing(50)
        vLayout.addLayout(topLayout)
        vLayout.addStretch(2)
        
        self.setLayout(vLayout)
        self.setLayout(vLayout)
        
        self.setVolumeValue(self.volumeValue)
        
        self.connect(self.volumeSlider, SIGNAL("valueChanged(int)"), self.setLineEditValue)
        
    def setLineEditValue(self, value):
        volumeValue = str(value) + "%"
        self.volumeValueLabel.setText(volumeValue)
        isOk = self.setVolumeValue(volumeValue)
        if isOk:
            StoreInfoParser.instance().setVolumeValue(volumeValue)
            # parser = ConfigFileParser.instance()
            # if not parser.has_section("VOLUME"):
            #     parser.addSection("VOLUME", "value", volumeValue)
            # else:
            #     if not parser.has_option("VOLUME", "value"):
            #         parser.addOption("VOLUME", "value", volumeValue)
            #     else:
            #         parser.changeSectionValue("VOLUME", "value", volumeValue)
                
        
    def setVolumeValue(self, volumeValue):
        cmd = "amixer set Master %s" % volumeValue
        isOk = os.system(cmd)
        if isOk != 0:
            InfoHintDialog(u'设置音量失败').exec_()
            return False
        
        return True
        
    def getVolumeValue(self):
        return StoreInfoParser.instance().getVolumeValue()

        # parser = ConfigFileParser.instance()
        # if parser.has_section("VOLUME"):
        #     if parser.has_option("VOLUME", "value"):
        #         return parser.getValue("VOLUME", "value")
        #     else:
        #         parser.addOption("VOLUME", "value", "100%")
        #         return "100%"
        # else:
        #     parser.addSection("VOLUME", "value", "100%")
        #     return "100%"
        
        
        
        
        
