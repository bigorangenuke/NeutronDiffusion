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
		self.dx = 0.
		self.dy = 0.

		self.numGroups = 2
		if "nodes" in kwargs:
			sz = kwargs["nodes"]
			#Check if any dimensions are less than the minimum dimensions
			if not any(s<MINIMUM_REACTOR_DIMENSION for s in sz):
				self.m = sz[0]
				self.n = sz[1]
			else: 
				print ("BAD TROUBLE. One or more reactor dimensions below MINIMUM_REACTOR_DIMENSION = %s"%(MINIMUM_REACTOR_DIMENSION))
				assert(False)
				a
		if 'size' in kwargs:
			sz = kwargs['size']
			if not any(s<=0 for s in sz):
				self.set_rx_size(sz)
			else:
				print("BAD TROUBLE. One or more reactor dimensions is less than zero")
				assert (False)

		if 'groups' in kwargs:
			gg = kwargs['groups']
			assert(gg==2 or gg==4)
			print('**************')
			print(gg)
			self.numGroups = gg

		self.nodes = None

		#Check if a file is passed, otherwise, load a blank pwr code of dimension m x n
		if 'file' in kwargs:
			self.loadFileToReactor(kwargs['file'])
			#print('load file stuff')
		else: self.loadBlankFileToReactor(self.m,self.n)

	def set_rx_size(self,size):
		self.xsize = size[0]
		self.ysize = size[1]
		self.dx = self.xsize/(self.m-1)**2
		self.dy = self.ysize/(self.n-1)**2


	def loadBlankFileToReactor(self,m,n):
		#Create a reactor of arbitrary dimension consisting entirely of PWR
		thenodes = np.empty((self.m,self.n),dtype = object)
		for i in range(m):
			for j in range(n):
				if dbg: print(i,j)
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
		#print(lines)

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
			#self.materials.append(material.Material(self.load_file('h20_2_group.txt')))
		elif g == 4:
			if dbg: print('Four Group')
			self.materials.append(material.Material(self.load_file('pwr_4_group.txt')))
			#self.materials.append(material.Material(self.load_file('h20_2_group.txt')))
		else: print('ERROR. No data for %s groups'%(g))

	def oneToTwo(self,index,g=False):
		i = int(index)/self.n
		j = index - self.n*i

		

		if dbg: print('rx.Reactor.oneToTwo(%s) = (%s,%s)'%(index,i,j))
		return i,j

	def twoToOne(self,i,j,g=None):
		if dbg: print('rx.Reactor.twoToOne(%s,%s) = %s'%(int(i),int(j),int(i*self.n+j)))
		assert(i>=0 and j>=0 and g>=0)
		if g:
			return int(self.m*self.n * g + i*self.n + j)
		else:
			return int(i*self.n + j)


	def getRowForNode(self,node,group):
		if dbg: print('rx.getrowForNode')
		dx = self.dx
		dy = self.dy
		if dbg: print("Node = ",node)

		i = node.i
		j = node.j

		n11 = self.nodes[i,j]
		n10 = self.nodes[i,j-1]
		n12 = self.nodes[i,j+1]
		n01 = self.nodes[i-1,j]
		n21 = self.nodes[i+1,j]

		d11 = n11.material.d
		d10 = n10.material.d
		d12 = n12.material.d
		d01 = n01.material.d
		d21 = n21.material.d

		sf11 = n11.material.sigma_f
		sf10 = n10.material.sigma_f
		sf12 = n12.material.sigma_f
		sf01 = n01.material.sigma_f
		sf21 = n21.material.sigma_f

		sa11 = n11.material.sigma_a
		sa10 = n10.material.sigma_a
		sa12 = n11.material.sigma_a
		sa01 = n01.material.sigma_a
		sa21 = n21.material.sigma_a

		snf11 = n11.material.nuSigma_f
		snf10 = n10.material.nuSigma_f
		snf12 = n11.material.nuSigma_f
		snf01 = n01.material.nuSigma_f
		snf21 = n21.material.nuSigma_f

		sr11 = n11.material.sigma_R
		sr10 = n10.material.sigma_R
		sr12 = n11.material.sigma_R
		sr01 = n01.material.sigma_R
		sr21 = n21.material.sigma_R

		rw = np.zeros(self.m*self.n*self.numGroups,dtype=object)
		g = group

		k = self.twoToOne(i,j,g)

		rw[k] = 2*d11[g]/dx + 2*d11[g]/dy + sa11[g]

		if j>1:
			k = self.twoToOne(i,j-1,g)
			rw[k] = -d10[g]/dy

		if j<self.n-1:
			k = self.twoToOne(i,j+1,g)
			rw[k] = -d12[g]/dy

		if i>1:
			k = self.twoToOne(i-1,j,g)
			rw[k] = -d01[g]/dx

		if i<self.m-1:
			k = self.twoToOne(i+1,j,g)
			rw[k] = -d21[g]/dx

		return rw

	# def bTermForNode(self,node,group):
	# 	m = self.m
	# 	n = self.n
	# 	g = group

	# 	i = node.i
	# 	j = node.j

	# 	n11 = self.nodes[i,j]
	# 	snf11 = n11.material.nuSigma_f[g]

	# 	b
	# 	for gg in range(g, self.numGroups):
	# 		snf11 = n11.material.nuSigma_f[gg]








	#Strip off the edge nodes of reactor matrix
	def stripEdges(self):
		return self.nodes[1:-1,1:-1]

	#Set all of the edges to zero
	def zeroEdges(self):
		self.nodes[0,:].value = 0
		self.nodes[-1,:].value = 0
		self.nodes[:,0].value = 0
		self.nodes[:,-1].value = 0
		return self.nodes
	
	def __repr__(self):
		return "Rx \tNodes = (%s,%s)"%(self.m,self.n)

if __name__=='__main__':
	reactor = Reactor(groups = 2,file = 'default.core')
	#print(reactor)
	nd = reactor.nodes[5,5]
	reactor.getRowForNode(nd)





	#print(reactor)
	#reactor = Reactor(size = [5,5])
	
	




