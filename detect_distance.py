
import sys
from PyQt4 import QtCore, QtGui, uic
 
form_class = uic.loadUiType("tempconv.ui")[0]                 # Load the UI

class MyWindowClass(QtGui.QMainWindow, form_class):
  def __init__(self, parent=None):
      # more code here
      # MAC addresses: 60:60:1F, 90:03:B7, A0:14:3D, 00:12:1C, 00:26:7E
   

app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
