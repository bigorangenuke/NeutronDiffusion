from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt
dbg = True
forceResize = True

#Represents the matplotlib figure
class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = plt.figure()
        
        sp = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                               QtGui.QSizePolicy.Expanding)

        FigureCanvas.__init__(self,self.fig)
        FigureCanvas.setSizePolicy(self,sp)
        FigureCanvas.updateGeometry(self)
        

    
class MplWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui=None
        #init the figure
        self.canvas = MplCanvas()
        
        
        sp = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sp.setHeightForWidth(True)
        sp.setWidthForHeight(True)
        self.setSizePolicy(sp)
        
        
        #add the figure to a layout
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        #delegate layout to the vb layout
        self.setLayout(self.vbl)
        
    def hasHeightForWidth(self):
        return True
    def heightForWidth(self,width):
        print("yay")
        return width
    
    def resizeEvent(self,event):
        if forceResize:
            
            #print event.oldSize(),event.size()
    
            #print self.layout().size()
            nw=event.size().width()
            nh=event.size().height()
            ow=event.size().width()
            oh=event.size().height()
            print( self.layout().geometry(),nw,nh,ow,oh)
            if nw>0 and nh>0:
                #print nw,nh
                if nw>nh:
                    self.resize(nh,nh)
                else: self.resize(nw,nw)
                
                
      

        
    def resizeIntercept(self):
        print ('Resize intercept')
        
    def widthForHeight(self,height):
        return height
    

        

        