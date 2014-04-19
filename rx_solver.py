import rx
import numpy as np

dbg = True

class RxSolver():
	def __init__(self,the_rx):
		print('stuff')
		self.reactor = the_rx
		self.m = self.reactor.m
		self.n = self.reactor.n
		m = self.m
		n = self.n
		self.numGroups = self.reactor.numGroups
		g = self.numGroups
		print('m = %s, n = %s, num groups = %s'%(m,n,g))
		self.mx = np.zeros((m*n*g,m*n*g))#,dtype = object)
		
		self.phi = np.ones((m*n*g))
		self.k = 1
		self.source = np.zeros((m*n*g))

		self.a = self.a_matrix()
		self.b = self.b_matrix()

	def a_matrix(self):
		a = np.zeros_like(self.mx)
		m = self.m
		n = self.n

		for (i,j),node in np.ndenumerate(self.reactor.nodes):
			for gg in range(self.numGroups):
				if dbg:print(i,j)
				if i ==0 or j ==0 or i==m-1 or j == n-1:
					if dbg:print('%s,%s,edge'%(i,j))
				else:
					a[i*n+gg*m*n+j,:] = self.reactor.getRowForNode(node,gg)
					print('i=',i)
		return a

	def b_matrix(self):
		m= self.m
		n = self.n
		g = self.numGroups
		
		b = np.zeros(m*n*g)

		for (i,j),nd in np.ndenumerate(self.reactor.nodes):

			if j==0 or i ==0 or j==n-1 or i = m-1:
				if dbg: print('edge')
			else:
				for gg in g:
					h = (ggg for ggg in g if ggg>gg)
					for hh in h:

					k = self.twoToOne(i,j-1,gg)
					b[k] = nd.material.nuSigma_f
					



		return b











if __name__=='__main__':
	reactor = rx.Reactor(groups=2,size=[10,10],file = 'default.core')
	print('num groups',reactor.numGroups)
	rxs = RxSolver(reactor)

