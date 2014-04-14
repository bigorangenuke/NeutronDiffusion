from PyQt4 import QtGui,QtCore

import os
import numpy as np
from mplwidget import MplWidget as mpl
from PyQt4 import uic

dbg = True

def path_to(file):
    #return absolute path to file
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),file)

def layout_widgets(layout):
    #return iterator of widgets in layout
    return (layout.itemAt(i) for i in range(layout.count))

def removeWidgetsFromLayout(layout):
    #deletes all the widgets in layout
    try:
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
    except:
        print('gui.removeWidgetsFromLayout() ERROR')
        return False
    return True

class CellMaterial():
    def __init__(self):
        self.materials = {'PWR':0,'Water':1,'Graphite':2}
        self.pwr = self.materials['PWR']
        self.water= self.materials['Water']
        self.graphite=self.materials['Graphite']
        
        
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
            
class NodeTableWidgetItem(QtGui.QTableWidgetItem):
    def __init__(self,i,j,material=None,parent = None):
        super(NodeTableWidgetItem,self).__init__()
        if not material:
            material = 0
        self.i = int(i)
        self.j = int(j)
        self.set_material(material)

    def set_material(self,material):
        #if dbg: print('NodeTableWidgetItem.set_material()')
        self.material = material
        self.color()
        
        
    def color(self):
        color = QtGui.QColor(255,255,255)
        print('material = ', self.material)
        if self.material==0:
            color = QtGui.QColor(255,0,0)
        elif self.material==1:
            color=  QtGui.QColor(0,0,255)
        elif self.material==2:
            color = QtGui.QColor(60,60,60)
        brush = QtGui.QBrush(color)
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.setBackground(brush)
 
 
    def __repr__(self):
        return self.row,self.column,self.material
    

class CoreDockWidget(QtGui.QDockWidget):
    def __init__(self,parent=None):
        
        if dbg: print('CoreDockWidget.__init__()')
        #Load the core widget
        QtGui.QDockWidget.__init__(self,parent)
        uic.loadUi(path_to('corewidget.ui'),self)
        
        #Give some initial values for the size attributes
        self.set_reactor_parameters(10,10,10.,10.)
        self.nodes = np.empty((self.m,self.n),dtype = object)
        
        #Connect actions and signal to UI
        self.hookupUI()
        self.coreTable = None
        
        #Draw the grid
        self.drawCore()

    def set_reactor_parameters(self,m,n,xsize,ysize):
    	self.set_m(m)
    	self.set_n(n)
    	self.set_xsize(xsize)
    	self.set_ysize(ysize)

    def set_m(self,m):
    	self.mNodesLineEdit.setText(str(m))
    	self.m = m

    def set_n(self,n):
    	self.nNodesLineEdit.setText(str(n))
    	self.n = n

    def set_xsize(self,xsize):

    	self.xSizeLineEdit.setText(str(xsize))
    	self.xsize = xsize

    def set_ysize(self,ysize):
    	self.ySizeLineEdit.setText(str(ysize))
    	self.ysize = ysize

    def hookupUI(self):
        if dbg: print('CoreDockWidget.hookupUI()')
        self.xSizeLineEdit.editingFinished.connect(self.updateSize)
        self.ySizeLineEdit.editingFinished.connect(self.updateSize)
        self.mNodesLineEdit.editingFinished.connect(self.updateSize)
        self.nNodesLineEdit.editingFinished.connect(self.updateSize)
        
        self.materialComboBox.addItems(list(CellMaterial().materials.keys()))
        self.materialComboBox.activated[str].connect(self.materialComboBoxActivated)
        
        self.updateCorePushButton.clicked.connect(self.updateCore)
        
        self.loadCorePushButton.clicked.connect(self.loadCore)
        self.saveCorePushButton.clicked.connect(self.saveCore)
        
    def materialComboBoxActivated(self,text):
        
        #Change selection in table to be material
        for item in self.coreTable.selectedItems():
            print('new material = ',text)
            item.set_material(int(CellMaterial().materials[text]))
        
    
    def saveCore(self):
        if dbg: print('CoreDockWidget.saveCore()')
        allRows = self.coreTable.rowCount()
        allColumns = self.coreTable.columnCount()
     
        filename = QtGui.QFileDialog.getSaveFileName(self)
          
        fn = '%s'%(filename)
        f = open(fn,'w')
        print(f)
        for i in range(allRows):
            for j in range(allColumns):
                item = self.coreTable.item(i,j)
                wstr = "%s,%s,%s\n"%(i,j,item.material)
                f.write(wstr) 
        f.close()

    def loadCore(self):
        
        filename = QtGui.QFileDialog.getOpenFileName()
        print(filename)
        if not filename: raise
        f = open(filename,'r')
        lines = f.readlines()
        f.close()
        core =[]
         
        ctable = QtGui.QTableWidget(self.m,self.n)
        for line in lines:
            l = line.split(',')
            print(l)
            i = l[0]
            j = l[1]

            core.append(NodeTableWidgetItem(i,j))
            core[i,j].set_material(m)
            
        return core
         
        if dbg: print('CoreDockWidget.loadCore()') 
        #item.set_material(int(CellMaterial().materials[text]))
    def drawCore(self,core = None):
        
        if dbg: print('CoreDockWidget.drawCore()')
        self.nodes = np.empty((self.m,self.n),dtype = object)
        layout = self.coreWidget.layout()
        #layout.addWidget(btn)

      	#Erase the current core
        removeWidgetsFromLayout(layout)
        
        tbl = QtGui.QTableWidget(self.m,self.n)
        # tbl.verticalHeader().setVisible(True)
        # tbl.horizontalHeader().setVisible(True)
        
        cellSize = 20
        
        allRows = tbl.rowCount()
        for row in range(0,allRows):
            tbl.setRowHeight(row,cellSize)
        
        allColumns = tbl.columnCount()
        for col in range(0,allColumns):
            tbl.setColumnWidth(col,cellSize)
        
        if core:
            print('Draw Core')
            for node in core:
                node.color()
                tbl.setItem(node.i,node.j,node)
        else:
            for i in range(allRows):
                for j in range(allColumns):
                    tbl.setItem(i,j, NodeTableWidgetItem(i,j))
                          
                    
        tbl.selectionModel().selectionChanged.connect(self.selectionChanged)
        
        layout.addWidget(tbl)
        
        self.coreTable = tbl

    def selectionChanged(self):
        if dbg: print('CoreDockWidget.selectionChanged()')
# 
#         for item in self.coreTable.selectedRanges():
#             print(item.leftColumn())

    def updateCore(self):
        if dbg: print('CoreDockWidget.updateCore()')
        self.updateSize()
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

 
    
    