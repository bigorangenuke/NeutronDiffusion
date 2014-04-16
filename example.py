
import rx
import numpy as np


#If this module is executed as the main thread
if __name__=='__main__':

	#Generic reactor. 5x5 node pwr
	filename = 'default.core'

	#Create a Reactor object from the file
	myrx = rx.Reactor(file = filename)
	
	#List all of the nodes in place as a 2d numpy array
	#I use a 2d array because it is easier for me to think about
	print('*'*10,'Loop through ALL the nodes','*'*10)
	for (i,j),node in np.ndenumerate(myrx.nodes):
		print(i,j,node,node.material)


	#Convert to 1d array for doing calcs.
	#Don't call this every step. It is slow.
	linear_rx_nodes = myrx.convertToOneDimension()
	print('*'*10,'Loop through ALL the nodes as a linear array','*'*10)
	#Loop through all of the nodes in the linear array
	for i,node in np.ndenumerate(linear_rx_nodes):
		print(i[0],node)

	print('*'*10,'Convert 1D coordinate to 2D','*'*10)
	#Get the 2D coordinates for the node at index 10
	i,j = myrx.oneToTwo(11)
	print(i,j)
	print('*'*10,'Convert 2D coordinate to 1D','*'*10)
	#Get the 1D coordinates for the node at index (3,2)
	print(myrx.twoToOne(i,j))
	print('*'*10,'Access all of the group parameters for the material','*'*10)
	#Access all of the parameters for the second energy group at node 6
	print(linear_rx_nodes[6].material.groupConstants(1))
	print('*'*10,'Return a list of a particular parameter for all energy groups','*'*10)
	#Access a paramter at node 6 for every energy group
	#Check out materials.py to see all of the available attributes
	print(linear_rx_nodes[6].material.sigma_R)
	print('*'*10,'Access a particular parameter for a particular energy group','*'*10)
	#Access a parameter at node 6 for the first energy group
	print(linear_rx_nodes[6].material.sigma_R[0])

	print('*'*10,'Access a particular parameter for the thermal energy group','*'*10)
	#Access a parameter at node 6 for the thermal energy group
	print(linear_rx_nodes[6].material.sigma_R[-1])
	print('*'*10,'Convert back to 2D array for some reason or another','*'*10)
	#After you've done some math on it, convert back to 2d array for printing or plotting or whatever
	#This step is also slow. Don't use in main loop of calculation.  Only for displaying results.
	two_d_rx_nodes_again = myrx.convertToTwoDimensions(linear_rx_nodes)
	for (i,j),node in np.ndenumerate(two_d_rx_nodes_again):
		print(i,j,node,node.material)


	print('*'*10,'Create a [10,20] reactor without loading a file for 4 energy groups','*'*10)
	new_rx = rx.Reactor(size = [10,20],groups=4)
	print(new_rx)
	print('*'*10,'Access a list of sigma_f values for energy groups','*'*10)
	print(new_rx.nodes[5,1].material.sigma_f)



	


