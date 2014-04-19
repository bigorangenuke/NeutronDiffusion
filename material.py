from numpy import sqrt
dbg = False
class Material():
    
    def __init__(self,material,groups=2):

        fn = None

        self.name = None

        if not groups==2 and not groups ==4:
            print('material.Material.__init__ group number not recognized')
            assert(False)

        if material==1:
            self.name = 'Fuel'
            if dbg: print('Material = Fuel')
            if groups==2:
                fn = 'pwr_2_group_fuel.txt'
            elif groups==4:
                fn = 'pwr_4_group_fuel.txt'
        elif material==2:
            self.name = 'Water'
            print('material.Material.__init__ material data for material %s not found'%(material))
            if dbg: print('Material = Water')
            if groups==2:
                fn = 'pwr_2_group_water.txt'
            elif groups==4:
                fn = 'pwr_4_group_water.txt'
        elif material==3:
            self.name = 'MOX'
            print('material.Material.__init__ material data for material %s not found'%(material))
            if dbg: print('Material = MOX')
            if groups==2:
                fn = 'pwr_2_group_MOX.txt'
            elif groups==4:
                fn = 'pwr_4_group_MOX.txt'
        elif material==4:
            self.name = 'DU'
            print('material.Material.__init__ material data for material %s not found'%(material))
            if dbg: print('Material = DU')
            if groups==2:
                fn = 'pwr_2_group_nou235.txt'
            elif groups==4:
                fn = 'pwr_4_group_nou235.txt'
            
        else:
            print('Material number %s not recognized'%(material))
            assert(False)

        f = open(fn,'r')
        lines = f.readlines()
        f.close()



        self.nuSigma_f =    []
        self.sigma_f =      []
        self.sigma_a =      []
        self.sigma_R =      []
        self.d=             []
    

        #Slow group is last
        #Load data for an arbitary number of groups
        for i,line in enumerate(lines):
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
    def __repr__(self):
        return self.name

#     def L(self):
#         #Extrapolation Length
#         s_tr = self.Sigma_tr
#         s_a= self.Sigma_a
#         return 1/sqrt(3*s_tr*s_a)*(1+0.4*s_a/s_tr)        
# 
#     def D(self):
#         #Diffusion coefficient
#         return 1./(3.*self.Sigma_tr())