/*
* This will split the megasome into individual chromosomes. 
	Use this only when there's two crossovers in the megasome.
	
	In order to run this, you need the co_coords.csv files from the megasomes, meaning you
	need to already have run the "get_multiple_co_coords.ijm" script on the _str.tif files.

	This script will produce the images and rois used to create the split megasomes with terminations:
	_str_split_co1.tif
	_str_split_co2.tif
*/
 
//set the batch mode
setBatchMode(true);
 
//set the expandable arrays
setOption("ExpandableArrays", true);
 
//get the main directory
main_dir = getDir("Select the directory with the .csv files and the .tif files");
 
//get the file list
file_list = getFileList(main_dir);

//get the working file list
working_file_list = newArray();

//get the counter
working_counter = 0;

//close all images
close("*");

//loop throuhg the flie list
for (a = 0; a < file_list.length; a++) {
	
	//get the index of _str.tif
	index_of_tif = indexOf(file_list[a], "_str.tif");
	
	//if the index is more than 0
	if (index_of_tif >= 0) {
	
		//set it
		working_file_list[working_counter] = file_list[a];
		
		//add one to the counter
		working_counter += 1;

	}

}

//loop through the working file list
for (a = 0; a < working_file_list.length; a++) {
	
	//close all images
	close("*");
	
	//reset the results
	run("Clear Results");
	
	//clear the roi manager
	roiManager("reset");
	
	//restart the current roi index
	current_roi_index = 0;
	
	//get the csv file
	csv_filename = replace(working_file_list[a], "_str.tif", "_str_co_coords.csv");
	
	//open the csv file
	open(main_dir + csv_filename);
	
	//get the co_array
	co_position_array = newArray(2);
	
	//get the table
	co_position_array[0] = Table.get("x", 0);
	co_position_array[0] = floor(parseInt(co_position_array[0]));
	co_position_array[1] = Table.get("x", 1);
	co_position_array[1] = floor(parseInt(co_position_array[1]));
	
	//if the co_position_array[0] if bigger than 1
	if (co_position_array[0] > co_position_array[1]) {

		//flip them
		x_original_1 = co_position_array[0];
		x_original_2 = co_position_array[1];
		
		//set them
		co_position_array[0] = x_original_2;
		co_position_array[1] = x_original_1;

	}
		
	//close the table
	close(csv_filename);
	
	//open the image
	open(main_dir + working_file_list[a]);
	
	//get the original image id
	original_image_id = getImageID();
	
	//get the dimensions
	getDimensions(image_width, image_height, image_channels, image_slices, image_frames);
	
	//get the mid y
	mid_y = floor(image_height/2);
	
	//make the y points
	y_points = newArray(2);
	y_points[0] = mid_y;
	y_points[1] = mid_y;
	
	//set the points
	makeSelection("points", co_position_array, y_points);
		
	//get the selection into the roi manager
	roiManager("add");
	
	//select the first roi in the manager
	roiManager("select", current_roi_index);
	
	//rename it to
	roiManager("rename", "co_coords");
		
	//get the first roi
	roiManager("deselect");
	
	//select non
	run("Select None");
	
	//add one to the current roi index
	current_roi_index += 1;
	
	//get the mid point
	mid_point = floor(((co_position_array[1] - co_position_array[0]) / 2) + co_position_array[0]);
	
	//make the selection
	makePoint(mid_point, mid_y);
	
	//add the point to the roi manager
	roiManager("add");
	
	//select the roi
	roiManager("select", current_roi_index);
	
	//rename it to mid point
	roiManager("rename", "mid_point");
	
	//deselect the roi manager
	roiManager("deselect");
	
	//select none
	run("Select None");
	
	//add one to the current roi index
	current_roi_index += 1;
	
	//make the first chromosome rectangle
	makeRectangle(0, 0, mid_point, image_height);
	
	//add it to the roi manager
	roiManager("add");	
	
	//select the roi
	roiManager("select", current_roi_index);
	
	//rename it
	roiManager("rename", "chr1_roi");
	
	//duplicate the iamge
	run("Duplicate...", "duplicate");
	
	//get the duplicate image id
	duplicate_image_id = getImageID();
	
	//get the chromosome 1 file name
	co1_filename = replace(working_file_list[a], "_str.tif", "_str_split_co1.tif");
	
	//save the image
	selectImage(duplicate_image_id);
		
	//save it
	save(main_dir + co1_filename);
	
	//close the image
	close();
	
	//deselect it
	roiManager("deselect");
				
	//select the original image
	selectImage(original_image_id);
	
	//select none
	run("Select None");
	
	//add one to the counter
	current_roi_index += 1;
		
	//make the second chr2 roi
	makeRectangle(mid_point, 0, ((image_width)-(mid_point)), image_height);
	
	//add the roi manager
	roiManager("add");
	
	//select it
	roiManager("select", current_roi_index);
	
	//rename it to chr2_roi
	roiManager("rename", "chr2_roi");
	
	//duplicate the iamge
	run("Duplicate...", "duplicate");
	
	//get the image id
	duplicate_image_id = getImageID();
	
	//get the chromosome 2 file name
	co2_filename = replace(working_file_list[a], "_str.tif", "_str_split_co2.tif");
	
	//select the image
	selectImage(duplicate_image_id);
	
	//save it
	save(main_dir + co2_filename);
	
	//close the image
	close();
	
	//deselect the roi manager
	roiManager("deselect");
	
	//select the original image
	selectImage(original_image_id);
	
	//select none
	run("Select None");
	
	//add one to the index
	current_roi_index += 1;
		
	//get the roi file name
	roi_file_name = replace(working_file_list[a], "_str.tif", "_str_split_rois.zip");
	
	//save the roi manager
	roiManager("save", main_dir + roi_file_name);
	
	//close all images
	close("*");
	
	//clear the roi
	roiManager("reset");
	
}