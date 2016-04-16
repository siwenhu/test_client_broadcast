# -*- coding: utf-8 -*-  

from PyQt4.QtCore import SIGNAL, QTranslator, QCoreApplication
from PyQt4.QtGui import QWidget, QLabel, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,\
                        QMessageBox
import commands
import os
from configFileParser import ConfigFileParser
from base.infohintdialog import InfoHintDialog
from storeinfoparser import StoreInfoParser


class MessageBox(InfoHintDialog):
        
    def __init__(self,hintInfo, parent = None):
        InfoHintDialog.__init__(self, hintInfo, parent)
        
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
            
        self.setStyleSheet("font-size : 16px")
        
        self.setTitle(self.tr("Tip Information"))
        
        self.ensureBtn = QPushButton(self.tr("OK"))
        self.cancelBtn = QPushButton(self.tr("Cancel"))
        self.cancelBtn.setDefault(True)
        
        bottomHLayout = QHBoxLayout()
        bottomHLayout.addStretch()
        bottomHLayout.addWidget(self.ensureBtn)
        bottomHLayout.addSpacing(10)
        bottomHLayout.addWidget(self.cancelBtn)
        bottomHLayout.addStretch()
        
        mainVLayout = QVBoxLayout()
        mainVLayout.addStretch()
        mainVLayout.addStretch()
        mainVLayout.addLayout(bottomHLayout)
        
        self.setLayout(mainVLayout)
        
        self.okBtn.hide()
        
        self.connect(self.ensureBtn, SIGNAL("clicked()"),self.slotOk)
        self.connect(self.cancelBtn, SIGNAL("clicked()"),self.slotCancel)
        
    
    def updateWindow(self):
        self.setTitle(self.tr("Tip Information"))
        self.okBtn.setText(self.tr("OK"))
        self.cancelBtn.setText(self.tr("Cancel"))
        
        
        
    def slotOk(self):
        self.accept()
        
    def slotCancel(self):
        self.reject()
        
        
        
        
        