import numpy.sqrt

class Material():
    
    def __init__(self,material):
        lines = material.split(',')
        lines=list((line.strip() for line in lines))
        #print(lines)
        self.name=                  lines[0]
        self.Sigma_tr =             lines[1]
        self.Sigma_a =              lines[2]
        self.nuSigma_f =            lines[3]
        self.relative_absorption =  lines[4]
        self.atomic_mass =          lines[5]

    def L(self):
        #Extrapolation Length
        s_tr = self.Sigma_tr
        s_a= self.Sigma_a
        return 1/numpy.sqrt(3*s_tr*s_a)*(1+0.4*s_a/s_tr)        

    def D(self):
        #Diffusion coefficient
        return 1./(3.*self.Sigma_tr())