from PyQt4 import QtGui,QtCore

import os
import types

from mplwidget import MplWidget as mpl

from PyQt4 import uic

dbg = True
def path_to(file):
    #return absolute path to file
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),file)

class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        if dbg: print('MainWindow.__init__()')
        QtGui.QMainWindow.__init__(self,parent)
        #build the .ui file
        uic.loadUi(path_to('mainwindow.ui'), self)
        self.hookupUI()
        
    def hookupUI(self):
        if dbg: print('MainWindow.hookupUI()')
        
class GraphDockWidget(QtGui.QDockWidget):
    def __init__(self,parent=None):
        if dbg: print('GraphDockWidget.__init__()')
        QtGui.QDockWidget.__init__(self,parent)
        uic.loadUi(path_to('graphwidget.ui'),self)
        self.graph = self.mplwidget
        
        self.hookupUI()
        
        
    def hookupUI(self):
        if dbg: print('GraphDockWidget.hookupUI()')

class CoreDockWidget(QtGui.QDockWidget):
    def __init__(self,parent=None):
        if dbg: print('CoreDockWidget.__init__()')
        QtGui.QDockWidget.__init__(self,parent)
        uic.loadUi(path_to('corewidget.ui'),self)
        
        
        self.hookupUI()
        
        
    def hookupUI(self):
        if dbg: print('CoreDockWidget.hookupUI()')



def Launch():
    mainWindow = MainWindow()
    graphDockWidget = GraphDockWidget()
    mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea,graphDockWidget)
    mainWindow.show()

if __name__=='__main__':
    app = QtGui.QApplication([])
    Launch()
    
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.linspace(0,100,1000)
    f = np.sin(x)
    plt.plot(x,f)
    app.exec_()

 
    
    