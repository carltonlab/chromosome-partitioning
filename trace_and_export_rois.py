#This script is used to trace and export the traces as rois used as part of the process of 
#straightening chromosomes. 

#For it to work, you need to have SNT plugin installed and running in Fiji.
#Then open the script in the fiji script editor and run it.
#No image should be open.
#The script will open the image, wait for the user to trace the chromosome and then export 
#the traces as rois. 

#the output will be a .traces file (used in SNT) and a .zip file with the rois.

#@ SNTService snt

#getting the libraries
import ij
from ij import WindowManager, IJ as win_man, IJ
from sc.fiji.snt import (Path, SNT, Tree, PathAndFillManager, SNTService)
from sc.fiji.snt.analysis import RoiConverter
from ij.gui import Roi, WaitForUserDialog
from ij.plugin.frame import RoiManager
from os.path import dirname, basename, splitext

#getting the path and fill manager
path_manager = snt.getPathAndFillManager()

#clearing the path manager
path_manager.clear()

#make a list with the possible colors
color_list = ["red", "cyan", "green", "magenta", "orange", "pink", "blue", "white", "yellow"]

#Get the file path
image_path = IJ.getFilePath("Select the file")

#get the file parent directory
image_parent = dirname(image_path) + "/"

#get the traces filename
image_filename = basename(image_path)
image_filename_split = splitext(image_filename)

#Get the traces filename
traces_filename = image_filename_split[0] + ".traces"

#get the rois filename
rois_file_name = image_filename_split[0] + "_rois.zip"

#get the traces save path
traces_save_path = image_parent + traces_filename

#get the rois filename path
rois_filename_path = image_parent + rois_file_name

#open the image
image_instance = IJ.openImage(image_path)
image_instance.setC(1)
image_instance.show()

#get the image window
image_window = image_instance.getWindow()

#initialize SNTService using the image
snt.initialize(image_instance, True)

#making a wait for user dialog
wait1 = WaitForUserDialog("Waiting for tracing", "Trace the image using SNT now")
wait1.show()

#Get the collection of paths after tracing
path_collection = snt.getPaths()

#declaring roi manager
RM = RoiManager()

#puting it into object
rm = RM.getRoiManager()

#getting the number of rois
number_of_rois = rm.runCommand("Count")

#clearing if needed
if number_of_rois > 0:
	#clearing the roi manager
	rm.runCommand("Deselect")
	rm.runCommand("Delete")

#now, loop through the paths and change the names
#making a counter
path_counter = 1
for a in path_collection:
	current_name = "chr" + str(path_counter)
	a.setName(current_name)
	path_counter += 1

#now, get the tree
current_tree = snt.getTree()

#saving the tree
current_tree.save(traces_save_path)

for a in path_collection:
	roi_converter_constructor = RoiConverter(a, image_instance)
	current_rois = roi_converter_constructor.getROIs(a)
	
	for b in current_rois:
		rm.addRoi(b)

#clearing the path manager
path_manager.clear()

#updating viewers
snt.updateViewers()

#deselect the rois
rm.deselect()


#save the rois
rm.save(rois_filename_path)

#reset the roi manager
rm.runCommand("Deselect")
rm.runCommand("Delete")

#close the image 
image_instance.close()

#close the window
image_window.close()