#-*- coding:utf-8 -*-

from PyQt4.QtCore import Qt, SIGNAL, QString, QTimer, QTranslator,\
    QCoreApplication
from PyQt4.QtGui import QWidget, QLabel, QComboBox, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,\
                        QMessageBox, QDialog
import commands
import os
import json
from ctypes import *
from configFileParser import ConfigFileParser
from base.infohintdialog import InfoHintDialog
from base.messagebox import MessageBox
from storeinfoparser import StoreInfoParser
from logrecord import LogRecord

class ResolutionSettingWidget(QWidget):
        
    def __init__(self, app, parent = None):
        super(ResolutionSettingWidget,self).__init__(parent)
        self.setStyleSheet("font-size : 16px;")
        self.app = app
        CDLL("libjson-c.so", mode=RTLD_GLOBAL)
        self.jytcapi = cdll.LoadLibrary('../lib/libjytcapi.so')
        self.jytcapi.jyinittcapi()
        self.resolutionLabel = QLabel(self.tr("Resolution setting"))
        
        self.resolutionCombox = QComboBox()
        self.resolutionCombox.setFixedSize(300, 30)
        
        self.saveBtn = QPushButton(self.tr("Save"))
        self.saveBtn.setStyleSheet("background: rgb(7,87,198); color: white; width: 90px; height: 30px;font-size : 16px;")
      
        gridLayout = QGridLayout()
        gridLayout.setSpacing(15)
        gridLayout.setMargin(10)
        gridLayout.addWidget(self.resolutionLabel, 0, 0, 1, 1)
        gridLayout.addWidget(self.resolutionCombox, 0, 1, 1, 1)
        
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
        
        self.updateResolutionCombox()
        
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.connect(self.timer,SIGNAL("timeout()"),self.resetScreenResolution);
        
        self.connect(self.saveBtn, SIGNAL("clicked()"),self.slotSave)
    
    def updateWindow(self):
        self.resolutionLabel.setText(self.tr(self.tr("Resolution setting")))
        self.saveBtn.setText(self.tr("Save"))
        
        
    def getCmdExecValue(self, cmd):
        statusOutput = commands.getstatusoutput(cmd)
        monitorList = statusOutput[1].split("\n")
        return monitorList
    def getCmdExecValueT(self, cmd):
        """得到命令执行的结果"""
        statusOutput = commands.getstatusoutput(cmd)
        monitorList = statusOutput[1].split("\n")
        return monitorList
    
    def showCurrentScreenResolution(self, curResolutionValue):
        """显示当前屏幕的分辨率"""
        count = self.resolutionCombox.count()
        for i in range(count):
            if self.resolutionCombox.itemText(i) == curResolutionValue:
                self.resolutionCombox.setCurrentIndex(i)
                return
            
        self.resolutionCombox.setCurrentIndex(-1)
        
    def getCurrentScreenResolution(self, screenName):
        currentSolution = "10"
        reSolution = "auto"
        solutionMap = {"0":"800x600","1":"1024x768","2":"1280x720","3":"1440x900","4":"1600x1020","5":"1920x1080","6":"1280x1024","7":"1366x768","8":"1600x900","10":"auto"}
        cmd = "../lib/ccr_jytcapi current_display"
        value =  self.getCmdExecValueT(cmd)
        for i in range(len(value)):
            LogRecord.instance().logger.info("#".join(value))
            if len(value[i].split(":"))==2 and value[i].split(":")[0]=="res" and value[i].split(":")[1] !="auto":
                currentSolution = value[i].split(":")[1]
                break
        if solutionMap.has_key(currentSolution):
            reSolution = solutionMap[currentSolution]
        return reSolution
        
    def updateResolutionCombox(self):
        """更新分辨率下拉框的内容"""
        #得到屏幕支持的分辨率
        self.resolutionCombox.clear()
        resolutionmMap = self.getScreenResolution()
        if resolutionmMap:
            screenName = resolutionmMap.keys()[0]
            for resolution in resolutionmMap[screenName]:
                if resolution == "800x600":
                    pass
                else:
                    self.resolutionCombox.addItem(resolution)
            self.resolutionCombox.setItemData(0, screenName, Qt.UserRole + 1);
        
        #获取当前屏幕的分辨率
        self.curResolutionValue = self.getCurrentScreenResolution(screenName)
        
        #显示当前屏幕的分辨率
        self.showCurrentScreenResolution(self.curResolutionValue)
        
    def getScreenResolution(self):
        """得到屏幕支持的分辨率"""
        #获得显示器名称，连接状态及行号
        Monitors = self.getCmdExecValueT("../lib/ccr_jytcapi display");

        #根据组合列表把显示器名称和支持的分辨率放入到一个字典中
        resolutionMap = {}
        resolutionList = []
        count = len(Monitors)
        for i in range(count):
            if len(Monitors[i].split(":"))<2:
                continue
            valueName = Monitors[i].split(":")[0]
            valueValue = Monitors[i].split(":")[1]
            
            if valueName == "value":
                resolutionList.append(valueValue)
      
        resolutionMap["monitorName"] = resolutionList
          
        return resolutionMap
    
    
        
    def slotSave(self):
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
            
        """改变当前的分辨率"""
        screenName = self.resolutionCombox.itemData(0, Qt.UserRole + 1).toString()
        if not screenName.isEmpty() and not screenName.isNull():
            self.curResolutionValue = self.getCurrentScreenResolution(str(screenName))
            if self.curResolutionValue:
                reScreen = self.resolutionCombox.currentText()
                if reScreen == "800x600":
                   pass 
                else:
                   pass
                #弹出提示框，默认为取消
                rb = MessageBox(self.tr("making sure set the resolution to current"), self).exec_()
                if rb == QDialog.Accepted:
                   self.jytcapi.jysetdispconf(str(reScreen))
                elif rb == QDialog.Rejected:
                   pass
                    
    def resetScreenResolution(self):
        """还原分辨率"""
        #关闭提示窗口
        children = self.children()
        count = len(children)
        for i in range(count):
            if isinstance(children[i], MessageBox):
                children[i].close()
        
        #还原之前的分辨率
        if self.jytcapi.jysetdispconf(self.curResolutionValue) != 0:
#             QMessageBox.information(None,u"错误",u'还原分辨率失败')
            InfoHintDialog(self.tr("reserve failed")).exec_()
            return
        
        #刷新分辨率下拉框
        self.updateResolutionCombox()
        
        if QString(self.curResolutionValue).contains("x"):
            width = self.curResolutionValue.split("x")[0]
            height = self.curResolutionValue.split("x")[1]
            self.emit(SIGNAL("resizePosition"), width, height)
            
        #刷新屏幕
        self.app.slotRefreshVMList()
    
    def writeConfigFile(self, curResolution):
        """记录修改后的配置文件"""
        StoreInfoParser.instance().setResolutionValue(curResolution)
        # parser = ConfigFileParser.instance()
        # if parser.has_section("SCREEN_RESOLUTION"):
        #     if parser.has_option("SCREEN_RESOLUTION", "resolution"):
        #         parser.changeSectionValue("SCREEN_RESOLUTION", "resolution", curResolution)
        #     else:
        #         parser.addOption("SCREEN_RESOLUTION", "resolution", curResolution)
        # else:
        #     parser.addSection("SCREEN_RESOLUTION", "resolution", curResolution)
        
        
        
        
        
