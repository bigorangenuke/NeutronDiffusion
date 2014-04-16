NeutronDiffusion(WIP)
================


To generate a reactor configuration:
	Run gui.py
	Make changes to the gui
	Make use of ctrl and shift for fast selecting.
	Save the reactor with the "save" button

To use the generated reactor configuration:
	Look at the example in example.py

To decrease the amount of things that are printed, set dbg to false in the modules that are annoying you.
I labeled where many of the print statements are coming from


Code structure:
	Reactor object: contains Nodes
	Node object: contains references to its location in the reactor and the material of which it is made
	Material object: contains the properties of the material

