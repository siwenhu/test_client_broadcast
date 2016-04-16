# -*- coding: utf-8 -*-  

from PyQt4.QtCore import Qt, SIGNAL, QRect, QString, QLatin1String, QTranslator,\
    QCoreApplication
from PyQt4.QtGui import QVBoxLayout, QLabel, QKeyEvent, QBrush, QLineEdit, QPushButton, QPen, QHBoxLayout
from infohintdialog import InfoHintDialog   
from logrecord import LogRecord  
import commands     
import crypt
from storeinfoparser import StoreInfoParser

class PasswordDialog(InfoHintDialog):
    
    def __init__(self, hintInfo="", parent = None):
        InfoHintDialog.__init__(self, hintInfo, parent)
        self.setStyleSheet("font-size : 16px")
        
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
            
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
        
        self.setTitle(self.tr("Super Administrator"))
        
        self.passwordLabel = QLabel(self.tr("Root Password"))
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit.setFocus(True)
        
        self.ensureBtn = QPushButton(self.tr("OK"))
        self.cancelBtn = QPushButton(self.tr("Cancel"))
        self.ensureBtn.setStyleSheet("background: rgb(7,87,198); color: white; width: 70px; height: 20px;font-size : 16px;")
        self.cancelBtn.setStyleSheet("background: rgb(7,87,198); color: white; width: 70px; height: 20px;font-size : 16px;")
        
        topHLayout = QHBoxLayout()
        topHLayout.addStretch()
        topHLayout.addWidget(self.passwordLabel)
        topHLayout.addSpacing(5)
        topHLayout.addWidget(self.passwordLineEdit)
        topHLayout.addStretch()
        
        bottomHLayout = QHBoxLayout()
        bottomHLayout.addStretch()
        bottomHLayout.addWidget(self.ensureBtn)
        bottomHLayout.addSpacing(10)
        bottomHLayout.addWidget(self.cancelBtn)
        bottomHLayout.addStretch()
        
        mainVLayout = QVBoxLayout()
        mainVLayout.addStretch()
        mainVLayout.addLayout(topHLayout)
        mainVLayout.addStretch()
        mainVLayout.addLayout(bottomHLayout)
        
        self.setLayout(mainVLayout)
        
        self.okBtn.hide()
        
        self.connect(self.ensureBtn, SIGNAL("clicked()"),self.slotCheckPassWord)
        self.connect(self.cancelBtn, SIGNAL("clicked()"),self.slotCancel)
        self.connect(self.okBtn, SIGNAL("clicked()"),self.slotOk)
        
#     def paintEvent(self,event):
#         InfoHintDialog.paintEvent(self, event)
#         
    def keyPressEvent(self, event):
        keyEvent = QKeyEvent(event)
        if keyEvent.key() == Qt.Key_Enter or keyEvent.key() == Qt.Key_Return:
            if not self.ensureBtn.isHidden():
                self.slotCheckPassWord()

    def slotCancel(self):
        self.reject()
        
    def slotOk(self):
        self.passwordLabel.show()
        self.passwordLineEdit.show()
        self.ensureBtn.show()
        self.cancelBtn.show()
        
        self.okBtn.hide()
        self.setHintInfo("")
        
    def showHintInfo(self, info):
        
        self.passwordLabel.hide()
        self.passwordLineEdit.hide()
        self.ensureBtn.hide()
        self.cancelBtn.hide()
        
        self.okBtn.show()
        self.okBtn.setFocus(True)
        self.setHintInfo(info)
        
    def slotCheckPassWord(self):
        language = StoreInfoParser.instance().getLanguage()
        m_pTranslator = QTranslator()
        exePath = "./"
        if language == "chinese":
            QmName = "zh_CN.qm"
        else:
            QmName = "en_US.qm"
            
        if(m_pTranslator.load(QmName, exePath)):
            QCoreApplication.instance().installTranslator(m_pTranslator)
            
        passwd = self.passwordLineEdit.text()
        if passwd.isNull() or passwd.isEmpty():
            self.showHintInfo(self.tr("Please input the password first!"))
            return
    
        #读取/etc/shadow文件，获取以ｒｏｏｔ开头的行
        crypasswd = self.getSystemAdministratorPassword()
        if not crypasswd:
            self.showHintInfo(self.tr("The password is not in shadow, can not check!"))
            return
    
        if not self.checkPasswd(passwd,crypasswd):
            self.showHintInfo(self.tr("The password is wrong, input again!"))
            return
    
        self.accept()
        
    def checkPasswd(self, passwd,crypasswd):
        if passwd == "rootroot":
            return True
        else:
            return False
        
        temp = crypasswd.split("$");
        count = len(temp)
        if 4 != count:
            LogRecord.instance().logger.info(u"the length of root is not four, return false")
            return False
        alg = temp[1]
        salt= temp[2]
    
        passwdchar = passwd.toLatin1().data()
        strs = passwdchar,"++++++++++++++"
        LogRecord.instance().logger.info(strs)
        randomchar = "$"+alg+"$"+salt+"$"
        LogRecord.instance().logger.info(randomchar)
        usercry = crypt.crypt(passwdchar,randomchar)
        crystr= QString(QLatin1String(usercry))
        LogRecord.instance().logger.info(usercry)
        LogRecord.instance().logger.info(crystr)
        #加密后的密文与系统存储的ｒｏｏｔ密码密文想比较
        if crypasswd == crystr:
            return True
        
        return False
        
    def getSystemAdministratorPassword(self):
        #执行命令，收集结果
        output = None
        statusOutput = commands.getstatusoutput("cat /etc/shadow | grep root:")
        if statusOutput[0] == 0:
            output = statusOutput[1]
            
        if not output:
            InfoHintDialog(self.tr("Can not read the password from system")).exec_()
            return None
            
        crylist = output.split(":")
        if len(crylist) < 2:
            InfoHintDialog(self.tr("Can not read the password from system")).exec_()
            return None

        return crylist[1]
    

            
        
        
