import numpy as np
import material,node

MINIMUM_REACTOR_DIMENSION = 4
dbg = True

def fileToReactor(filename):
	if dbg: print('rx.fileToReactor(%s)'%(filename))
	f = open(filename,'r')
	lines = f.readlines()
	f.close()
	

	#Get maximum values of i and j
	maxi = 0
	maxj = 0

	m = 0
	n = 0
	for line in lines:
		l = line.split(',')
		i = int(l[0])
		j = int(l[1])
		if i > maxi: maxi = i
		if j > maxj: maxj = j

	m = maxi+1
	n = maxj+1

	for line in lines:
		l = line.split(',')
		i = int(l[0])
		j = int(l[1])

	rx = Reactor(size=[m,n])


class Reactor():
	def __init__(self,**kwargs):
		if dbg: print('rx.Reactor.__init__')
		#default values of size
		self.m = 5
		self.n = 5
		self.numGroups = 2
		if "size" in kwargs:
			sz = kwargs["size"]
			#Check if any dimensions are less than the minimum dimensions
			if not any(s<MINIMUM_REACTOR_DIMENSION for s in sz):
				self.m = sz[0]
				self.n = sz[1]
			else: 
				print ("BAD TROUBLE. One or more reactor dimensions below MINIMUM_REACTOR_DIMENSION = %s"%(MINIMUM_REACTOR_DIMENSION))
				assert(False)
		else:print('')

		if 'groups' in kwargs:
			gg = kwargs['groups']
			assert(gg==2 or gg==4)
			self.numGroups = gg

		self.nodes = None

		#Check if a file is passed, otherwise, load a blank pwr code of dimension m x n
		if 'file' in kwargs:
			self.loadFileToReactor(kwargs['file'])
			print('load file stuff')
		else: self.loadBlankFileToReactor(self.m,self.n)

	def loadBlankFileToReactor(self,m,n):
		#Create a reactor of arbitrary dimension consisting entirely of PWR
		thenodes = np.empty((self.m,self.n),dtype = object)
		for i in range(m):
			for j in range(n):
				print(i,j)
				thenodes[i,j] = node.Node(i,j,material.Material(1,groups=self.numGroups))
		self.nodes = thenodes


	def loadFileToReactor(self,file):
		if dbg: print('rx.Reactor.loadFileToReactor(%s)'%(file))

		f = open(file,'r')
		lines = f.readlines()
		f.close()

		#Get maximum values of i and j
		maxi = 0
		maxj = 0
		m = 0
		n = 0
		for line in lines:
			l = line.split(',')
			i = int(l[0])
			j = int(l[1])
			if i > maxi: maxi = i
			if j > maxj: maxj = j

		self.m = maxi+1
		self.n = maxj+1

		thenodes = np.empty((self.n,self.m),dtype=object)

		for line in lines:
			l = line.split(',')
			i = int(l[0])
			j = int(l[1])
			m = int(l[2].strip())
			mat = material.Material(m,groups = self.numGroups)
			thenodes[i,j] = node.Node(i,j,mat)
		self.nodes = thenodes


	def convertToOneDimension(self):
		return np.reshape(self.nodes,self.m*self.n)

	def convertToTwoDimensions(self,oneDimensionRx):
		return np.reshape(oneDimensionRx,[self.m,self.n])


	def load_materials(self,**kwargs):
		if dbg: print('rx.Reactor.load_materials()')
		g = 2
		#Pull out of text file and load line by line to materials
		if 'groups' in kwargs:
			g = kwargs['groups']
		if g == 2:
			if dbg: print('Two Group')
			self.materials.append(material.Material(self.load_file('pwr_2_group.txt')))
		elif g == 4:
			if dbg: print('Four Group')
			self.materials.append(material.Material(self.load_file('pwr_4_group.txt')))
		else: print('ERROR. No data for %s groups'%(g))

	def oneToTwo(self,index):
		i = int(index)/self.n
		j = index - self.n*i
		if dbg: print('rx.Reactor.oneToTwo(%s) = (%s,%s)'%(index,i,j))
		return i,j

	def twoToOne(self,i,j):
		if dbg: print('rx.Reactor.twoToOne(%s,%s) = %s'%(int(i),int(j),int(i*self.n+j)))
		assert(i>=0 and j>=0)
		return int(i*self.n + j)

	def __repr__(self):
		return "Rx \tNodes = (%s,%s)"%(self.m,self.n)

if __name__=='__main__':
	reactor = Reactor(groups = 2,file = 'default.core')
	print(reactor)
	#reactor = Reactor(size = [5,5])
	
	




