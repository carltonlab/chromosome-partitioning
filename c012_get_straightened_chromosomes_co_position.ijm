//############################# DESCRIPTION ###################################################

//This script will let you get the straightened chromosome crossover positions. 

//This is used for other scripts that require the crossover sites coordinates. 

//It will only work with files ending in _str.tif

//If multiple points are selected, only the first one is used, meaning it is only useful for single 
//CO chromosomes. 

//It will also flip the chromosome so that the short arm is aligned to the left. Be careful when using
//as it will replace the previous file. 

//The otuput is a file with the .tif extension replaced with _rois.zip

//It asks for a directory with the _str.tif files and then makes you process all of them in batch. 

//It also creates a sum projection of the image and saves it as _sum_proj.tif

//Open this script in the fiji script editor and run it to use. 

//############################# END DESCRIPTION ###############################################







//Script to get the crossover site position for the straightened chromosomes

//set the expandable arrays
setOption("ExpandableArrays", true);

//do it in batch
//get the directory
main_dir = getDir("Select working directory");

//get the file list
file_list = getFileList(main_dir);

//get a new array to hold the str files only
str_filename_array = newArray();

//start a new counter for the loop
str_loop_counter = 0;


//filter for the str
for (a = 0; a < file_list.length; a++) {

	str_index = indexOf(file_list[a], "_str.tif");
	
	//if str.tif is found, then add it to the list
	if (str_index >= 0) {

		str_filename_array[str_loop_counter] = file_list[a];
		
		str_loop_counter += 1;

	};
		
};

//get the list length
number_of_str_files = str_filename_array.length;

//loop through the current str_file list and get the co position filename
for (a = 0; a < number_of_str_files; a++) {
	
	//get the file name without extension
	filename_no_ext = File.getNameWithoutExtension(str_filename_array[a]);
	
	//reset results
	run("Clear Results");
	
	//clear the roi manager if needed
	roiManager("reset");
	
	//restart the flip flag
	flip_flag = false;
	
	//reset the average panSYP1 and syp1Phos 
	avg_pansyp1 = newArray();
	avg_syp1phos = newArray();
	
	//make a new table to set the results
	Table.create("fields");

	//open the image
	open(main_dir + str_filename_array[a]);
	
	run("In [+]");
	run("In [+]");
	run("In [+]");
	run("In [+]");


	
	//select none in case theres something hidden
	run("Select None");
	Overlay.clear;
	updateDisplay();
		
	//get the window id
	main_image_id = getImageID();
	
	//get the dimensions
	getDimensions(width, height, channels, slices, frames);
	
	//set the slice to 7
	Stack.setSlice(4);
	Stack.setChannel(2);
	run("Enhance Contrast", "saturated=0.35");
	
	//wait for user to set the position
	waitForUser("Mark the crossover position with a point Roi");
	
	//get the roi positions and floor them
	Roi.getCoordinates(xpoints, ypoints)
	x_coord = floor(xpoints[0]);
	y_coord = floor(ypoints[0]);
	
	//select none
	run("Select None");
	
	//make a new point with the floor 
	makePoint(x_coord, y_coord);
	
	//add the selection to the roi manager
	roiManager("add");
	
	//select none
	run("Select None");
	
	//deselect if anything is selected
	roiManager("deselect");
	
	//now select it again to get the points
	roiManager("select", 0);
	
	//rename the roi
	roiManager("rename", "co_position");
		
	//select none
	run("Select None");
		
	//get the midpoint of the chromosome
	half_length = floor(width/2);
	
	//finding out if you need to flip the chromosome
	if (x_coord > half_length) {

		flip_flag = true;

	};
	
	//if the flip is true, then calculate the new roi and flip the image
	if (flip_flag == true) {

		//select the window 
		selectImage(main_image_id);
		
		//flip the image
		run("Flip Horizontally", "stack");
		
		//now save the image
		save(main_dir + str_filename_array[a]);
		
		//calculate the new roi and reset the roi manager
		roiManager("reset");
	
		//getting the new x position
		new_x_position = (width)-(x_coord);
		
		//making the point
		makePoint(new_x_position, y_coord);
		
		//add it to the roi manager
		roiManager("add");
		
		//selecting and renaming
		roiManager("select", 0);
		roiManager("rename", "co_position");
		
		//rewrite the x_coord
		x_coord = new_x_position;	
		
	};
	
	//get the short and long arms length based on the positions
	chr_length = width;
	long_arm_length = (chr_length)-(x_coord);
	short_arm_length = x_coord;
	
	//now, make the projection
	/*
	selectImage(main_image_id);
	run("Z Project...", "projection=[Sum Slices]");
	
	//get the new image id
	projection_image_id = getImageID();
	
	//select the main image and close
	selectImage(main_image_id);
	close();
	
	//select the projection
	selectImage(projection_image_id);
	
	//get the new filename for the sum projection
	proj_filename = filename_no_ext + "_sum_proj.tif";
	
	//save it
	save(main_dir+proj_filename);
	*/
										
	//update the dimensions
	getDimensions(width, height, channels, slices, frames);
	
	//now making the rectangles of the short and long arms
	//getting the short arm rectangle
	makeRectangle(0,0, short_arm_length, height);
	
	//add the rectangle to the roi manager
	roiManager("add");
	roiManager("select", 1);
	roiManager("rename", "short_arm_area");
	roiManager("deselect");
	
	run("Select None");
			
	//getting the long arm rectangle
	makeRectangle(x_coord, 0, long_arm_length, height);
	
	//add the rectangle to the roi manager
	roiManager("add");
	roiManager("select", 2);
	roiManager("rename", "long_arm_area");
	roiManager("deselect");
	
	run("Select None");
	
	//save the roi manager
	roi_manager_filename = filename_no_ext + "_rois.zip";
	
	//save the roi manager
	roiManager("save", main_dir + roi_manager_filename);
	
	//clear the roi manager
	roiManager("reset");
	
	//close all image
	close("*");
	
	
};
print("");
print("Script c012_get_str_co_position.ijm done running.");