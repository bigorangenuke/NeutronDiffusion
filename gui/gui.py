from PyQt4 import QtGui,QtCore

import os
import numpy as np
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
        #Load the core widget
        QtGui.QDockWidget.__init__(self,parent)
        uic.loadUi(path_to('corewidget.ui'),self)
        
        #Give some initial values for the size attributes
        self.m = 10.
        self.n = 10.
        self.xsize = 10.
        self.ysize = 10.
        
        
        self.nodes = np.empty((self.m,self.n),dtype = object)
        
        #Connect actions and signal to UI
        self.hookupUI()
        #Draw the grid
        self.drawCore()
    
    def drawCore(self): 
        if dbg: print('CoreDockWidget.drawCore()')

        layout = self.coreWidget.layout()
        #layout.addWidget(btn)
        
        for (i,j),node in np.ndenumerate(self.nodes):
            lbl = "%s,%s"%(i,j)
            btn = QtGui.QPushButton(lbl)
            
            #btn.resize(QtCore.QSize(30,30))
            btn.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
            self.nodes[i,j] = btn
            layout.addWidget(btn,i,j)
            btn.setStyleSheet('background-color: red')
        
    def hookupUI(self):
        if dbg: print('CoreDockWidget.hookupUI()')
        self.xSizeLineEdit.editingFinished.connect(self.updateSize)
        self.ySizeLineEdit.editingFinished.connect(self.updateSize)
        self.mNodesLineEdit.editingFinished.connect(self.updateSize)
        self.nNodesLineEdit.editingFinished.connect(self.updateSize)
        
        self.updateCorePushButton.clicked.connect(self.updateCore)
        
    def updateCore(self):
        if dbg: print('CoreDockWidget.updateCore()')
        self.drawCore()
        
    def updateSize(self):
        if dbg: print('CoreDockWidget.updateSize()')
        self.m = int(self.mNodesLineEdit.text())
        self.n = int(self.nNodesLineEdit.text())
        self.xsize = float(self.mNodesLineEdit.text())
        self.ysize = float(self.ySizeLineEdit.text())
        


def setupMainWindow():

    graphDockWidget = GraphDockWidget()
    mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea,graphDockWidget)
    coreDockWidget = CoreDockWidget()
    mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea,coreDockWidget)
    
    
    
if __name__=='__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    
    app = QtGui.QApplication([])
    mainWindow = MainWindow()
    setupMainWindow()
    mainWindow.show()
    

    x = np.linspace(0,7,1000)
    f = np.sin(x)
    plt.plot(x,f)
    app.exec_()

 
    
    