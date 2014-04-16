from PyQt4 import QtGui,QtCore

import os
#from mplwidget import MplWidget as mpl
from PyQt4 import uic
import jtools

dbg = True

#Default size values for the reactor.
DEFAULT_M_NODES = 5
DEFAULT_N_NODES = 5
DEFAULT_X_SIZE = 1.
DEFAULT_Y_SIZE = 1.

#Pixel height/width for QTableWidgetItems
CELL_SIZE = 20



class CellMaterial():
    #Dictionary of possible cell materials
    def __init__(self):
        self.materials = {'None': 0,'PWR':1,'Water':2,'Graphite':3}
        self.none = 0
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
    #Custom TableWidgetItemType
    #Holds a reference to its location
    #Method for coloring
    def __init__(self,i,j,material=None,parent = None):
        super(NodeTableWidgetItem,self).__init__()
        
        if dbg: print ('gui.init NodeTableWidgetItem')
        
        if not material:
            material = 0
            

        self.i = int(i)
        self.j = int(j)
        if dbg:print('Material = ',material)
        self.set_material(material)
        

    def set_material(self,material):
        #if dbg: print('NodeTableWidgetItem.set_material()')
        self.material = material
        self.color()
        
        
    def color(self):
        if dbg: print('gui.NodeTableWidgetItem.color()')
        color = QtGui.QColor(255,255,255)
        #print('material = ', self.material)
        if self.material==1:
            color = QtGui.QColor(255,0,0)
        elif self.material==2:
            color=  QtGui.QColor(0,0,255)
        elif self.material==3:
            color = QtGui.QColor(60,60,60)
        brush = QtGui.QBrush(color)
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.setBackground(brush)
 
    def __repr__(self):
        return self.row,self.column,self.material
    
class CoreWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        
        if dbg: print('gui.CoreWidget.__init__()')
        #Load the core widget
        QtGui.QDockWidget.__init__(self,parent)
        uic.loadUi(path_to('corewidget.ui'),self)
        
        #Give some initial values for the size attributes
        self.set_reactor_parameters(DEFAULT_M_NODES,DEFAULT_N_NODES,DEFAULT_X_SIZE,DEFAULT_Y_SIZE)

        core = self.loadBlankCoreTable()
        self.coreTable = core
        self.drawCore(core)
        #Connect actions and signal to UI
        self.hookupUI()
    
    #===============================================================================
    # Parameters
    #===============================================================================
        
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
        
    def updateSize(self):
        if dbg: print('gui.CoreDockWidget.updateSize()')
        self.m = int(self.mNodesLineEdit.text())
        self.n = int(self.nNodesLineEdit.text())
        self.xsize = float(self.mNodesLineEdit.text())
        self.ysize = float(self.ySizeLineEdit.text())
    
    def updateSizeFields(self):
        if dbg: print('gui.CoreDockWidget.updateSizeFields')
        self.mNodesLineEdit.setText(str(self.m))
        self.nNodesLineEdit.setText(str(self.n))
        self.xSizeLineEdit.setText(str(self.xsize))
        self.ySizeLineEdit.setText(str(self.ysize))    

    #===============================================================================
    # GUI
    #===============================================================================
    def hookupUI(self):
        if dbg: print('gui.CoreDockWidget.hookupUI()')
        self.xSizeLineEdit.editingFinished.connect(self.updateSize)
        self.ySizeLineEdit.editingFinished.connect(self.updateSize)
        self.mNodesLineEdit.editingFinished.connect(self.updateSize)
        self.nNodesLineEdit.editingFinished.connect(self.updateSize)
        
        self.materialComboBox.addItems(list(CellMaterial().materials.keys()))
        self.materialComboBox.activated[str].connect(self.materialComboBoxActivated)
        
        self.updateCorePushButton.clicked.connect(self.updateCoreButtonIsPressed)
        
        self.loadCorePushButton.clicked.connect(self.loadCoreButtonIsPressed)
        self.saveCorePushButton.clicked.connect(self.saveCore)
        
        self.reactorComboBox.addItems(jtools.filesInDirectoryWithExtension(jtools.currentDirectory(), '*.core'))
        
        self.reactorComboBox.activated[str].connect(self.reactorComboBoxActivated)
        
    def reactorComboBoxActivated(self,text):
        if dbg: print('gui.CoreDockWidget.reactorComboBoxActivated')
        
        
        
        
    def materialComboBoxActivated(self,text):
        if dbg: print ('gui.CoreDockWidget.materialComboBoxActivated')
        #Change selection in table to be material
        
        for item in self.coreTable.selectedItems():
            print('new material = ',text)
            item.set_material(int(CellMaterial().materials[text]))
        
        self.saveCore('_currentcore')
        
    #===========================================================================
    # Core management
    #===========================================================================
    def saveCore(self,filename= None):
        
        #Save the core configuration to a file
        if dbg: print('gui.CoreDockWidget.saveCore()')
        
        
        allRows = self.coreTable.rowCount()
        allColumns = self.coreTable.columnCount()
        
        if not filename:
            filename = QtGui.QFileDialog.getSaveFileName(self, 'Save Core to File', filter='*.core')


        f = open(filename,'w')
    
        for i in range(allRows):
            for j in range(allColumns):
                item = self.coreTable.item(i,j)
                wstr = "%s,%s,%s\n"%(i,j,item.material)
                f.write(wstr) 

        f.close()

    
    def defaultCore(self):
        self.updateSize()
        return self.loadBlankCoreTable()
    
    def loadCoreButtonIsPressed(self):          
        core = self.loadCoreTableFromFile()
        self.drawCore(core)
    
    def loadBlankCoreTable(self):
        core = QtGui.QTableWidget(self.m,self.n)
        for i in range(self.m):
            for j in range(self.n):
                core.setItem(i,j,NodeTableWidgetItem(i,j,1))  
        
        self.coreTable = core
        return core    
        #self.drawCore(core)
           
    def loadCoreTableFromFile(self,filename=None):

        if not filename: 
            filename = QtGui.QFileDialog.getOpenFileName(filter='*.core')
        if not filename: raise
        
        f = open(filename,'r')
        lines = f.readlines()
        f.close()
        
        maxi = 0
        maxj = 0
        
        for line in lines:
            l = line.split(',')
            i = int(l[0])
            j = int(l[1])
            if i>maxi: maxi=i
            if j>maxj: maxj=j
        
        self.m = maxi+1
        self.n = maxj+1
        
        self.updateSizeFields()

        ctable = QtGui.QTableWidget(self.m,self.n)
        for line in lines:
            l = line.split(',')
            i = int(l[0])
            j = int(l[1])
            m = int(l[2].strip())
            ctable.setItem(i,j,NodeTableWidgetItem(i,j,m))
        print(ctable)
        
        return ctable

    
       
    def drawCore(self,core = None):
        
        if dbg: print('CoreDockWidget.drawCore()')
        
        if not core:
            core = self.defaultCore()
            print('core is empty')
        else:
            print('core is not empty')
        assert(core)

         
        #Get a pointer to the widget's layout in the gui
        layout = self.coreWidget.layout()
        
        #Erase the current core from the layout
        removeWidgetsFromLayout(layout)
         
        #Connect self.selectionchanged to the selectionChanged event on the table
        #core.selectionModel().selectionChanged.connect(self.selectionChanged)
        
        #Add it to the gui
        layout.addWidget(core)
    
        #Resize and save it
        self.coreTable = jtools.resizeTableCells(core,20)
    
    
    def updateCoreButtonIsPressed(self):
        if dbg: print('CoreDockWidget.updateCoreButtonIsPressed()')
        self.updateSize()
        core = self.loadBlankCoreTable()
        self.drawCore(core)
        


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

def setupMainWindow():

    #graphDockWidget = GraphDockWidget()
    #mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea,graphDockWidget)
    coreWidget = CoreWidget()
    mainWindow.setCentralWidget(coreWidget)
    #mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea,coreDockWidget)
    

    

if __name__=='__main__':
    
    app = QtGui.QApplication([])
    mainWindow = MainWindow()
    setupMainWindow()
    mainWindow.show()

    app.exec_()

 
    
    