# -*- coding: utf-8 -*-  
 
from PyQt4.QtCore import QTextCodec, QFile, QString, Qt
from PyQt4.QtGui import QApplication, QDialog
import sys
import settingWidget
from base.infohintdialog import InfoHintDialog
from base.passworddialog import PasswordDialog
from base.messagebox import MessageBox
 
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
     
#     passwordDlg = MessageBox(u"确定设置为当前选择的分辨率?")
#     if passwordDlg.exec_() != QDialog.Accepted:
#         exit(0)
    window = settingWidget.SettingWidget(app=None)
#     window = InfoHintDialog("sgs")
    window.show()
    app.exec_()
