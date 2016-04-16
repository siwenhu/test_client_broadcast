# -*- coding: utf-8 -*-  

from PyQt4.QtCore import Qt, SIGNAL, QString, QCoreApplication, QTranslator
from PyQt4.QtGui import QWidget, QLabel, QSlider, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox,\
    QComboBox, QPushButton
import os
from configFileParser import ConfigFileParser
from base.infohintdialog import InfoHintDialog
from storeinfoparser import StoreInfoParser
import globalvariable

class LanguageSettingWidget(QWidget):
        
    def __init__(self, app, parent = None):
        super(LanguageSettingWidget,self).__init__(parent)
        self.setStyleSheet("font-size : 16px")
        self.app = app
        self.languageLabel = QLabel(self.tr("Language setting"))
        
        languageList = [self.tr("中文简体"),"English"]
        
        self.languageCombox = QComboBox()
        self.languageCombox.addItems(languageList)
        self.languageCombox.setFixedSize(300, 30)
        
        self.saveBtn = QPushButton(self.tr("Save"))
        self.connect(self.saveBtn, SIGNAL("clicked()"),self.slotSave)
        self.saveBtn.setStyleSheet("background: rgb(7,87,198); color: white; width: 90px; height: 30px;font-size : 16px;")
      
        gridLayout = QGridLayout()
        gridLayout.setSpacing(15)
        gridLayout.setMargin(10)
        gridLayout.addWidget(self.languageLabel, 0, 0, 1, 1)
        gridLayout.addWidget(self.languageCombox, 0, 1, 1, 1)
        
        topLayout = QHBoxLayout()
        topLayout.addStretch()
        topLayout.addSpacing(50)
        topLayout.addLayout(gridLayout)
        topLayout.addStretch(1)
        
        bottomHLayout = QHBoxLayout()
        bottomHLayout.addStretch()
        bottomHLayout.addWidget(self.saveBtn)
        bottomHLayout.addStretch()
        
        vLayout = QVBoxLayout()
        vLayout.addStretch()
        vLayout.addSpacing(50)
        vLayout.addLayout(topLayout)
        vLayout.addStretch(2)
        vLayout.addSpacing(10)
        vLayout.addLayout(bottomHLayout)
        
        self.setLayout(vLayout)
        
        self.updateLanguageCombox()
    
    def updateWindow(self):
        
        self.languageLabel.setText(self.tr("Language setting"))
        self.saveBtn.setText(self.tr("Save"))
        
    def updateLanguageCombox(self):
        language = StoreInfoParser.instance().getLanguage()
        if language == "chinese":
            self.languageCombox.setCurrentIndex(0)
        else:
            self.languageCombox.setCurrentIndex(1)
    
    def slotSave(self):
        languageco = self.languageCombox.currentText()
        
        m_pTranslator = QTranslator()
        exePath = "./"
        
        if languageco == self.tr("中文简体"):
            QmName = "zh_CN.qm"
            language = "chinese"
        else:
            QmName = "en_US.qm"
            language = "english"
            
        
        self.writeConfigFile(language)
            
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
        
        self.emit(SIGNAL("languagechanged"),language)
        
        globalvariable.LANGUAGE = language
        InfoHintDialog(self.tr("saved success!")).exec_()
        
    def writeConfigFile(self, language):
        StoreInfoParser.instance().setLanguage(language)
        
        
        
        
        
        
