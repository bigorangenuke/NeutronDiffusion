from numpy import sqrt
dbg = False
class Material():
    
    def __init__(self,material):

        self.nuSigma_f =    []
        self.sigma_f =      []
        self.sigma_a =      []
        self.sigma_R =      []
        self.d=             []
        
        #Slow group is last
        #Load data for an arbitary number of groups
        for i,line in enumerate(material):
            line = line.split(',')
            line = list((l.strip() for l in line))
            if i == 0:
                for l in line[1:]:
                    self.nuSigma_f.append(float(l)) 
            if i == 1:
                for l in line[1:]:
                    self.sigma_f.append(float(l)) 
            if i == 2:
                for l in line[1:]:
                    self.sigma_a.append(float(l)) 
            if i == 3:
                for l in line[1:]:
                    self.d.append(float(l)) 
            if i == 4:
                for l in line[1:]:
                    self.sigma_R.append(float(l)) 
        if dbg: print("Group 1 constants = ",self.groupConstants(1))
        
    def groupConstants(self,group):
        return self.nuSigma_f[group],self.sigma_f[group],self.sigma_a[group],self.sigma_R[group],self.d[group]  
    
    def diffusionLength(self,group):
        return sqrt(self.d[group]/self.sigma_a[group])
    
#     def L(self):
#         #Extrapolation Length
#         s_tr = self.Sigma_tr
#         s_a= self.Sigma_a
#         return 1/sqrt(3*s_tr*s_a)*(1+0.4*s_a/s_tr)        
# 
#     def D(self):
#         #Diffusion coefficient
#         return 1./(3.*self.Sigma_tr())