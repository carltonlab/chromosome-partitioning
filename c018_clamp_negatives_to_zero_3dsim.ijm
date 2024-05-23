/*
 * 
 * This script will clamp the values of the megasomes recon to 0 when they're negative.
 *	It takes the 3D sim straightened megasomes and sets all negative values to 0
 * 
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
	
	close("*");
	
	//open the image
	open(main_dir + working_file_list[a]);
	
	//get image id
	main_image_id = getImageID();
	
	//get the dimensions
	getDimensions(main_width, main_height, main_channels, main_slices, main_frames);
	
	//select the image
	selectImage(main_image_id);

	
	//loop through the channels
	for (b = 0; b < main_channels; b++) {
		
		//set the channel
		Stack.setChannel(b+1);
		
		
		
		//loop through the slices
		for (c = 0; c < main_slices; c++) {
			
			//set the slice
			Stack.setSlice(c+1);
			
			//loopo throiuhg the width
			for (d = 0; d < main_width; d++) {
			
				//loopo through the height
				for (e = 0; e < main_height; e++) {
					
					//get pixel
					pixel_value = getPixel(d, e);
					
					//if the pixel is less than 0
					if (pixel_value < 0) {
					
						//set the pixel to 0
						setPixel(d, e, 0);
					
					}
					
		
				}
			
			}
	
		}

	}
	
	//get the new name
	saving_name = replace(working_file_list[a], "_str.tif", "_zero_clamped_str.tif");
	
	//save the image
	selectImage(main_image_id);
	
	//save it
	save(main_dir + saving_name);

}

//print tdon
print("Script done, clamped imaged to zero");
