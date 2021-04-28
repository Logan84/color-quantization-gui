# color-quantization-gui
This Python code uses an SOM to perform color quantization on an image. This also performs this task in a GUI that allows for easy decision for picking an image.

# Install Requirements 
In the directory with the file, run
` pip install -r requirement.txt `

# How to run code
` python SOMgui.py ` 

# How to use
The search bar will allow you to locate a folder that contains images. The image file names will be shown when the folder is selected. 
All variables (listed below) must be set before execution of the SOM:
> Width (int): Determines the shape of the SOM. This will create a square lattice.
> Learning Rate (float): Determines the starting learning rate of the SOM.
> Neighborhood Radius (float): Determines the starting neighborhood radius of the SOM.
> Epoch (int): Determines the number of epoch the SOM will run over the image. 
