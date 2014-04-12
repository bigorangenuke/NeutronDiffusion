import numpy as np
import material,node

MINIMUM_REACTOR_DIMENSION = 4
dbg = True
class Reactor():
	def __init__(self,**kwargs):
		#default values of size
		self.m = 5
		self.n = 5
		
		if "size" in kwargs:
			sz = kwargs["size"]

			if not any(s<MINIMUM_REACTOR_DIMENSION for s in sz):
				self.m = sz[1]
				self.n = sz[0]
			else: print ("BAD TROUBLE. One or more reactor dimensions below MINIMUM_REACTOR_DIMENSION = %s"%(MINIMUM_REACTOR_DIMENSION))
		
		self.materials = []
		
		self.load_materials(groups = 2)

		thenodes = np.empty((self.n,self.m),dtype=object)

		for j in range(self.m):
			for i in range(self.n):
				thenodes[i,j] = node.Node(i,j,self.materials)

		self.nodes = thenodes

	def load_materials(self,**kwargs):
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

	
	def load_file(self,file):
		f = open(file)
		lines = f.readlines()
		f.close()
		return lines
		
	def __repr__(self):
		return "Rx \tNodes = (%s,%s)"%(self.m,self.n)


if __name__=='__main__':
	reactor = Reactor(size = [5,5])




