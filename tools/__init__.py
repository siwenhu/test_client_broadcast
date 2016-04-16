# -*- coding: utf-8 -*-  
 
from PyQt4.QtCore import QTextCodec, QFile, QString
from PyQt4.QtGui import QApplication
import sys
from basics import ToolWidget
 
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
     
     
    window = ToolWidget()
    window.show()
    app.exec_()
