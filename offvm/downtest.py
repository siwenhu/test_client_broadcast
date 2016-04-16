#coding:utf-8
'''
Created on Dec 17, 2014

@author: root
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mybutton import MenuButton
from myprogress import WidgetProgress
from downloadthread import DownloadThread
from progressthread import ProgressThread
import sys
CMD="rsync -avzp root@192.168.5.133:/var/lib/libvirt/images/xp-0.img"

class DownloadTest(QWidget):
    def __init__(self,parent=None):
        super(DownloadTest,self).__init__(parent)
        self.setFixedSize(820,620)
        
        self.vmTableWidget = QTableWidget()
        self.setTableWidgetStyle()
        #self.mainLayout = QHBoxLayout(self)
        hLayout = QHBoxLayout()
        hLayout.setMargin(0)
        hLayout.addStretch()
        hLayout.addWidget(self.vmTableWidget)
        hLayout.addStretch()
        
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(hLayout)
        self.mainLayout.addStretch()
        
        
        
        self.downloadThread = DownloadThread()
        self.progressThread = ProgressThread()
        
        self.downloadingList = []
        
        self.showVmList()
#         self.vmTableWidget.setColumnCount(3)
#         self.vmTableWidget.setRowCount(1)
#         self.vmTableWidget.setFrameShape(QFrame.NoFrame)
#         self.vmTableWidget.setSelectionMode(QAbstractItemView.NoSelection)
#         self.vmTableWidget.verticalHeader().setVisible(False)#设置垂直头不可见
#         self.vmTableWidget.horizontalHeader().setVisible(False)#设置垂直头不可见
#         self.vmTableWidget.setShowGrid(False)
#         self.vmTableWidget.verticalHeader().setDefaultSectionSize(600)
#         self.vmTableWidget.horizontalHeader().setDefaultSectionSize(800)
#         self.vmTableWidget.setStyleSheet("QTableWidget{background-color: rgb(235, 235, 235,0);}")
        
        
    def setTableWidgetStyle(self):
        
        #self.vmTableWidget.setColumnCount(3)
        #self.vmTableWidget.setRowCount(1)
        self.vmTableWidget.setFrameShape(QFrame.NoFrame)
        self.vmTableWidget.setEditTriggers(QTableWidget.NoEditTriggers)#不能编辑
        self.vmTableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.vmTableWidget.verticalHeader().setVisible(False)#设置垂直头不可见
        self.vmTableWidget.horizontalHeader().setVisible(False)#设置垂直头不可见
        self.vmTableWidget.setShowGrid(False)
        self.vmTableWidget.setFocusPolicy(Qt.NoFocus)
        
        self.vmTableWidget.setStyleSheet("QTableWidget{background-color: rgb(235, 235, 235,0);}")
    def getVmList(self):
        vmList = []
        vmInfo = {}
        vmInfo["id"] = "15615123021654541"
        vmInfo["status"] = "offline"
        
        vmInfo1 = {}
        vmInfo1["id"] = "1561545421654541"
        vmInfo1["status"] = "offline"
        
        vmInfo2 = {}
        vmInfo2["id"] = "1561afew21654541"
        vmInfo2["status"] = "offline"
        
        vmInfo3 = {}
        vmInfo3["id"] = "afewfdsafewfa"
        vmInfo3["status"] = "offline"
        
        vmList.append(vmInfo)
        vmList.append(vmInfo1)
        vmList.append(vmInfo2)
        vmList.append(vmInfo3)
        
        return vmList
    def showVmList(self):
        self.vmTableWidget.clear()
        vmList = self.getVmList()
        num = len(vmList)
        if num <=3:
            rowCount = 1
            if num == 1:
                columnCount = 1
            elif num == 2:
                columnCount = 2
            elif num == 3:
                columnCount = 3
        else:
            rowCount = num/3 + 1
            columnCount = 3
            
        self.vmTableWidget.setColumnCount(columnCount)
        self.vmTableWidget.setRowCount(rowCount)
        self.vmTableWidget.setFixedWidth(800)
        self.vmTableWidget.setFixedHeight(800/columnCount*rowCount)
        self.vmTableWidget.verticalHeader().setDefaultSectionSize(800/columnCount)
        self.vmTableWidget.horizontalHeader().setDefaultSectionSize(800/columnCount)
        #self.setWidget("status")
        if columnCount <= 3 and rowCount == 1:
            for i in range(columnCount):
                self.setRowColumnWidget(0,i,vmList[i]["id"])
        
        for i in range(rowCount):
            for j in range(3):
                if i*3 + j <= num-1:
                    self.setRowColumnWidget(i, j, vmList[i*3+j]["id"])
#     
    def setRowColumnWidget(self,row,column,vmid):
        status = "sfw"
        #self.vmTableWidget.clear()
        mainWidget = QWidget()
        #self.vmTableWidget.hideColumn()
        
        firMybutton = MenuButton()
        firMybutton.setFixedSize(QSize(250,250))
        firMybutton.setIcon(QIcon("windows.png"))
        firMybutton.setIconSize(QSize(250,250))
        #firMybutton.setStatus("undownload")
        firMybutton.setObjectName(vmid + ":" + QString.number(row) + ":" + QString.number(column))
        self.connect(firMybutton, SIGNAL("clicked()"),self.startDownload)
        
            
        progressBar = WidgetProgress()
        progressBar.setFixedSize(250,250)
        progressBar.setObjectName(vmid + ":" + QString.number(row) + ":" + QString.number(column))
        #progressBar.objectName()
            
           
        #self.firMybutton.setText(self.tr("确萨"))
        
        #progressBar = QProgressBar()
        
        myLayout = QHBoxLayout()
        myLayout.setMargin(0)
        myLayout.addWidget(firMybutton)
        myLayout.addWidget(progressBar)
        
        if vmid in self.downloadingList:
            firMybutton.hide()
        else:
            progressBar.hide()
             
        #firMybutton.hide()
        mainWidget.setLayout(myLayout)
        
        
        self.vmTableWidget.setCellWidget(row, column, mainWidget)
        #self.mainLayout.addWidget(mainWidget)
    def startDownload(self):
        pbp = QPushButton().sender()
        buttonName = pbp.objectName()
        vmid = buttonName.split(":")[0]
        row = buttonName.split(":")[1]
        column = buttonName.split(":")[2]
        self.downloadingList.append(vmid)
        #pbp.setStatus("downloading")
        self.downloadThread = DownloadThread()
        self.progressThread = ProgressThread()
        self.downloadThread.setProcessId(buttonName)
        self.progressThread.setProcessId(buttonName)
        self.downloadThread.start()
        self.progressThread.start()
        #self.connect(downloadThread, SIGNAL(""))
        self.connect(self.progressThread, SIGNAL("currentprogress"),self.updateProgressBar)
        self.connect(self.progressThread, SIGNAL("downloadover"),self.downloadOver)
        #self.setWidget("downloading")
        self.setRowColumnWidget(int(row), int(column), vmid)
    def updateProgressBar(self,count,objectname):
#         for i in range(len(self.downloadingList)):
#             if objectname == self.downloadingList[i]:
#                 progress=self.vmTableWidget.findChild((WidgetProgress, ),objectname)
#                 progress.progressBar.setValue(count) 
        progress=self.vmTableWidget.findChild((WidgetProgress, ),objectname)
        progress.progressBar.setValue(count) 
    def downloadOver(self,name):
        vmid = name.split(":")[0]
        row = name.split(":")[1]
        column = name.split(":")[2]
        self.downloadingList.remove(vmid)
        self.setRowColumnWidget(int(row), int(column), vmid)
    
        
# app=QApplication(sys.argv)
# dialog=DownloadTest()
# dialog.show()
# app.exec_()        
