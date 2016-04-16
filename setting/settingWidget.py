# -*- coding: utf-8 -*-  
from PyQt4.QtGui  import QDialog, QApplication, QHBoxLayout, QVBoxLayout, QPalette, QBrush, QMenu, QCursor,\
                         QAction, QKeyEvent
from PyQt4.QtCore import Qt, SIGNAL, QEvent, QSize, QTranslator,\
    QCoreApplication

from base.tabwidget import TabWidget
from basesetting import BaseSettingWidget
from resolutionsetting import ResolutionSettingWidget
from volumesetting import VolumeSettingWidget
from base.basedialog import BaseDialog
from terminalType import TerminalTypeWidget
from languagesetting import LanguageSettingWidget
import globalfunc
from storeinfoparser import StoreInfoParser

from networkingubuntu import NetWorkSettingWidget

class SettingWidget(BaseDialog):
       
    def __init__(self, app, parent = None):
        super(SettingWidget,self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        
        
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
            
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
        
        
        self.app = app
        self.mousePressed = False

#         self.setFixedSize(800, 600)
        self.baseSetting = BaseSettingWidget(app)
        self.networkSetting = NetWorkSettingWidget(app)
        self.resolutionSetting = ResolutionSettingWidget(app)
        #self.volumnSetting = VolumeSettingWidget(app)
        #self.terminalType = TerminalTypeWidget(app)
        self.languageSetting = LanguageSettingWidget(app)
        
        self.tabWidget = TabWidget()
        self.tabWidget.addTab(self.baseSetting, self.tr("Basic"))
        self.tabWidget.addTab(self.networkSetting, self.tr("Net"))
        self.tabWidget.addTab(self.resolutionSetting, self.tr("Resolution"))
        #self.tabWidget.addTab(self.volumnSetting, self.tr("音量设置"))
        #self.tabWidget.addTab(self.terminalType, self.tr("终端类型"))
        self.tabWidget.addTab(self.languageSetting,self.tr("Language"))
        
        self.tabWidget.closeBtn().installEventFilter(self)

        #self.closeAction = QAction(u"关闭", self)
        
        #self.connect(self.closeAction, SIGNAL("triggered()"), self.close)
        self.connect(self.tabWidget, SIGNAL("closeWidget"),self.close)
        self.connect(self.resolutionSetting, SIGNAL("resizePosition"),self.slotResizePosition)
        self.connect(self.languageSetting, SIGNAL("languagechanged"),self.slotLanguageChange)

        mainVLayout = QVBoxLayout()
        mainVLayout.setSpacing(0)
        mainVLayout.setMargin(0)
        mainVLayout.addWidget(self.tabWidget)
        
        self.setLayout(mainVLayout)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setFocus()
    
    def updateWindow(self):
        
        self.tabWidget.removeTab(0)
        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(2)
        self.tabWidget.removeTab(3)
        self.baseSetting.updateWindow()
        self.networkSetting.updateWindow()
        self.resolutionSetting.updateWindow()
        self.languageSetting.updateWindow()
        self.tabWidget.addTab(self.baseSetting, self.tr("Basic"))
        self.tabWidget.addTab(self.networkSetting, self.tr("Net"))
        self.tabWidget.addTab(self.resolutionSetting, self.tr("Resolution"))
        self.tabWidget.addTab(self.languageSetting, self.tr("Language"))
        self.tabWidget.setCurrentIndex(3)
    
    def eventFilter(self, target, event):
        if target == self.tabWidget.closeBtn():
            if event.type() == QEvent.Enter:
                self.tabWidget.closeBtn().setStyleSheet("background:rgb(255, 255, 255)")
                self.tabWidget.closeBtn().setAutoFillBackground(True);
            elif event.type() == QEvent.Leave:
                self.tabWidget.closeBtn().setAutoFillBackground(False);
                return True
            
        return QDialog.eventFilter(self, target, event)
        
    def slotResizePosition(self, width, height):
        self.emit(SIGNAL("resizePosition"), width, height)
        #self.resize(QSize(int(width)/9*5 + 150,int(height)/6*4))
        #self.move((int(width) - self.width())/2, (int(height) - self.height())/2)
  
        
#     def contextMenuEvent(self, event):
#         menu = QMenu(self)
#         menu.setStyleSheet("background:rgb(216, 239, 233);border:1px;border-color:green");
#         menu.addAction(self.closeAction)
#         menu.exec_(QCursor.pos());
#         event.accept();
 
    def slotLanguageChange(self,language):
        self.emit(SIGNAL("languagechanged"),language)
        self.updateWindow()
        
        
    def keyPressEvent(self, event):
        keyEvent = QKeyEvent(event)
        if keyEvent.key() == Qt.Key_Enter or keyEvent.key() == Qt.Key_Return:
            if hasattr(self.tabWidget.currentWidget(), "slotSave"):
                self.tabWidget.currentWidget().slotSave()


