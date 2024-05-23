/* Description

This script normalizes the sum projection of the straightened megasomes.
The files ending with "_str_sum_proj.tif" in a given directory will be obtained and opened,
letting the user go through each channel and get a threshold. The used will select the threshold of the
signal in the respective channel and the entire channel will be then normalized to the mean intensity on the 
selected area. This produces an image that is good for the aligned chromosomes as the phospho-SYP-1 or the GFP::COSA-1 foci
brightness will appear similar for all the straightened chromosomes. 

For this to work you need to have split the megasomes already using the script c018_split_megasomes.ijm and have prepared the sum projections for 
all the images running the script c018_megasomes_make_sum_projection.ijm.

*/





//set the expandable arrays
setOption("ExpandableArrays", true);

//get the main directory
main_dir = getDir("Select the main directory with the proj.tif images");

//get the file list
file_list = getFileList(main_dir);

//make the working file lsit
working_file_list = newArray();

//set the counter
working_counter = 0;

//loop throuhg the flie list
for (a = 0; a < file_list.length; a++) {
		
	//get the index of _sum_proj.tif
	index_of_sum_proj = indexOf(file_list[a], "_str_sum_proj.tif");
	
	//if the index if more than 01
	if (index_of_sum_proj > -1) {

		//add it tot he working file list
		working_file_list[working_counter] = file_list[a];
		
		//add oen to the counter
		working_counter += 1;

	}
	
}

//loop through the working file list
for (a = 0; a < working_file_list.length; a++) {

	//close all images
	close("*");
	
	//reset the roi manager
	roiManager("reset");
	
	//get the filename without extension
	no_ext_filename = File.getNameWithoutExtension(working_file_list[a]);
	
	no_ext_filename = replace(no_ext_filename, "str_sum_proj", "str");
	
	//loop through 2 time
	for (b = 0; b < 2; b++) {
		
		//close all images
		close("*");
		
		//reset the roi manager
		roiManager("reset");
		
		//get the current file name
		current_proj_filename = no_ext_filename + "_split_co" + (b+1) + "_sum_proj.tif";
		
		//print the file working on
		print("Working on file: " + current_proj_filename);
		
		//open the current image
		open(main_dir + current_proj_filename);
		
		//get the current image id
		current_image_id = getImageID();
		
		run("In [+]");
		run("In [+]");
		run("In [+]");
		
		//set the display mode to grayscale
		Stack.setDisplayMode("grayscale");
		
		//set the saturation
		run("Enhance Contrast", "saturated=0.35");
		
		//get the dimensions
		getDimensions(current_width, current_height, current_channels, current_slices, current_frames);
		
		//loop through the channels
		for (c = 0; c < current_channels; c++) {
			
			//select none
			run("Select None");
			
			//clear the results
			run("Clear Results");
			
			//select the current im age
			selectImage(current_image_id);
			
			//set the channel
			Stack.setChannel(c+1);
			
			//run threshold
			run("Threshold...");
			
			//wait for user
			waitForUser("Set the threshold to normalize to");
			
			//create the selection
			run("Create Selection");
			
			//set enhacned contrast again
			run("Enhance Contrast", "saturated=0.35");
			
			//add the roi
			roiManager("add");
			
			//select the current roi
			roiManager("select", c);
			
			//rename it
			roiManager("rename", "channel"+(c+1));	
			
			//measure
			run("Measure");
			
			//get the mean
			channel_selection_mean = getResult("Mean", 0);
			
			//select none
			run("Select None");
			
			//get the division
			run("Divide...", "value="+channel_selection_mean+" slice");

		}
		
		//get the roi filename
		roi_file_name = replace(current_proj_filename, "_proj.tif", "_normalizing_rois.zip");
		
		//print that the rois are saving
		print("Saving the normalizing rois: " + roi_file_name);
		
		//save the rois
		roiManager("save", main_dir + roi_file_name);
		
		//get the new image file name
		new_image_file_name = replace(current_proj_filename, "_sum_proj.tif", "_roi_normalized_sum_proj.tif");
		
		//select the image
		selectImage(current_image_id);
		
		//print that the image is being saved
		print("Saving new image: " + new_image_file_name);
		
		//save it
		save(main_dir + new_image_file_name);
		
		//close all images
		close("*");
		
		///reset the roi manager
		roiManager("reset");
		
		//clear results
		run("Clear Results");

	}
			
}

//log that it is done
print("Script finished");





//
//