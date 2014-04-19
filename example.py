
import rx
import numpy as np

dbg = False

#If this module is executed as the main thread
if __name__=='__main__':

	#Generic reactor. 10x20 node pwrs

	filename = 'default.core'

	#Create a Reactor object from the file
	myrx = rx.Reactor(file = filename)
	
	#List all of the nodes in place as a 2d numpy array
	#I use a 2d array because it is easier for me to think about
	if dbg: print('*'*10,'Loop through ALL the nodes','*'*10)
	for (i,j),node in np.ndenumerate(myrx.nodes):
		if dbg: print(i,j,node,node.material)


	#Convert to 1d array for doing calcs.
	#Don't call this every step. It is slow.
	linear_rx_nodes = myrx.convertToOneDimension()
	if dbg: print('*'*10,'Loop through ALL the nodes as a linear array','*'*10)
	#Loop through all of the nodes in the linear array
	for i,node in np.ndenumerate(linear_rx_nodes):
		if dbg: print(i[0],node)

	#Get the 2D coordinates for the node at index 
	i,j = myrx.oneToTwo(11)
	if dbg: print(i,j)
	
	if dbg: print('*'*10,'Convert 2D coordinate to 1D','*'*10)
	#Get the 1D coordinates for the node at index (3,2)
	if dbg: print(myrx.twoToOne(i,j))
	if dbg: print('*'*10,'Access all of the group parameters for the material','*'*10)
	#Access all of the parameters for the second energy group at node 6
	if dbg: print(linear_rx_nodes[6].material.groupConstants(1))
	if dbg: print('*'*10,'Return a list of a particular parameter for all energy groups','*'*10)
	#Access a paramter at node 6 for every energy group
	#Check out materials.py to see all of the available attributes
	if dbg: print(linear_rx_nodes[6].material.sigma_R)
	if dbg: print('*'*10,'Access a particular parameter for a particular energy group','*'*10)
	#Access a parameter at node 6 for the first energy group
	if dbg: print(linear_rx_nodes[6].material.sigma_R[0])

	if dbg: print('*'*10,'Access a particular parameter for the thermal energy group','*'*10)
	#Access a parameter at node 6 for the thermal energy group
	if dbg: print(linear_rx_nodes[6].material.sigma_R[-1])
	if dbg: print('*'*10,'Convert back to 2D array for some reason or another','*'*10)
	#After you've done some math on it, convert back to 2d array for printing or plotting or whatever
	#This step is also slow. Don't use in main loop of calculation.  Only for displaying results.
	two_d_rx_nodes_again = myrx.convertToTwoDimensions(linear_rx_nodes)
	for (i,j),node in np.ndenumerate(two_d_rx_nodes_again):
		if dbg: print(i,j,node,node.material)

	if dbg: print('*'*10,'Create a [10,20] reactor without loading a file for 4 energy groups','*'*10)
	if dbg: new_rx = rx.Reactor(size = [10,20],groups=4)
	if dbg: print(new_rx)
	if dbg: print('*'*10,'Access a list of sigma_f values for energy groups','*'*10)
	if dbg: print(new_rx.nodes[5,1].material.sigma_f)

	if dbg: print('*'*10,'Strip off the edges of the reactor','*'*10)
	if dbg: print(new_rx.stripEdges())

	if dbg: print('*'*10,'Set edges of the reactor to zero','*'*10)
	if dbg: print(new_rx.zeroEdges())


	


