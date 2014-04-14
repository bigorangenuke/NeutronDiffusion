import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

def chi(energy):
	return 0.453*np.exp(-1.036*energy)*np.sinh(np.sqrt(2.29*energy))

c1 = 1e-6
c2 = 220e-6
c3 = 48400e-6
c4 = 10648000e-6


e2 = np.linspace(c1,c2,1e5)
chi2 = chi(e2)

e3 = np.linspace(c2,c3,1e5)
chi3 = chi(e3)

e4 = np.linspace(c3,c4,1e5)
chi4 = chi(e4)

#print(E)

e = np.logspace(-6,1,10000)
x = chi(e)
ax = plt.subplot(111)



a_chi2= integrate.simps(chi2,e2)/(c2-c1)#/(np.log(c2-np.log(c1)
a_chi3= integrate.simps(chi3,e3)/(c3-c2)
a_chi4= integrate.simps(chi4,e4)/(c4-c3)




print('a_chi2 = ',a_chi2)
print('a_chi3 = ',a_chi3)
print('a_chi4 = ',a_chi4)
#plt.xkcd()
plt.plot(e,x)

cc = []
cc.append(c2)
cc.append(c3)
cc.append(c4)

chh = []
chh.append(chi(c2))
chh.append(chi(c3))
chh.append(chi(c4))

plt.plot(cc,chh,ls = 'None',marker='o')


#ax.set_yscale('log')
ax.set_xscale('log')
plt.show()


