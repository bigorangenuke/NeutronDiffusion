import numpy as np
import material,node
MINIMUM_REACTOR_DIMENSION = 4

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
			
			
		self.materials = self.load_materials()

		#self.sigma_tr = self.get_sigma_tr()
		#self.sigma_a = self.get_sigma_a()

		thenodes = np.empty((self.n,self.m),dtype=object)

		for j in range(self.m):
			for i in range(self.n):
				thenodes[i,j] = node.Node(i,j,self.materials)

		self.nodes = thenodes

	def load_materials(self):
		#Pull out of text file and load line by line to materials
		f = open('macroscopiccrosssections.txt')
		lines = f.readlines()
		f.close()

		mats=[]
		for line in lines:
			mats.append(material.Material(line))
		return mats

	def __repr__(self):
		return "Rx(m = %s, n =  %s)"%(self.m,self.n)


if __name__=='__main__':

	reactor = Reactor(size = [5,5],materials=None)
	x_bc = [[0,0],[reactor.n, 0]]
	y_bc = [[0,0],[reactor.m, 0]]




