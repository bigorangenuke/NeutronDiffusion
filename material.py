from numpy import sqrt

class Material():
    
    def __init__(self,material):
                #print(lines)
#         self.name=                  lines[0]
#         self.Sigma_tr =             lines[1]
#         self.Sigma_a =              lines[2]
#         self.nuSigma_f =            lines[3]
#         self.relative_absorption =  lines[4]
#         self.atomic_mass =          lines[5]
#         self.Sigma_R =              lines[6]

        self.nuSigma_f = []
        self.sigma_f = []
        self.sigma_a = []
        self.sigma_R = []
        self.d=[]
        #Slow group is last
        #Load data for an arbitary number of groups
        for i,line in enumerate(material):
            line = line.split(',')
            line = list((l.strip() for l in line))
            print(line)
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
        

#     def L(self):
#         #Extrapolation Length
#         s_tr = self.Sigma_tr
#         s_a= self.Sigma_a
#         return 1/sqrt(3*s_tr*s_a)*(1+0.4*s_a/s_tr)        
# 
#     def D(self):
#         #Diffusion coefficient
#         return 1./(3.*self.Sigma_tr())