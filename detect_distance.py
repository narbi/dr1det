
import sys
from PyQt4 import QtCore, QtGui, uic
 
form_class = uic.loadUiType("tempconv.ui")[0]                 # Load the UI

class MyWindowClass(QtGui.QMainWindow, form_class):
  def __init__(self, parent=None):
      # more code here



app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
