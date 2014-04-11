from numpy import asarray,sum

class Node():
    def __init__(self,i,j,materials=None):
        self.i = i
        self.j = j
        self.materials = materials
        self.sigma_tr = self.get_sigma_tr()
        self.sigma_a = self.get_sigma_a()

    def get_sigma_tr(self):
        #Get array of the Sigma_tr of all the materials
        return asarray(list(material.Sigma_tr for material in self.materials),dtype="float")


    def get_sigma_a(self):
        #Get array of the Sigma_a of all the materials
        return asarray(list(material.Sigma_a for material in self.materials),dtype='float')


    def Sigma_a(self):
        #Macroscopic absorption cross section
        return sum(self.sigma_a)

    def __repr__(self):
        return "(%s,%s)"%(self.i,self.j)

    def Sigma_tr(self):
        #Macroscopic transient cross section
        return sum(self.sigma_tr)