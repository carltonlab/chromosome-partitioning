/*

This script will get the sum projected images from the photoconversion experiment and allow the user to select the
region COSA-1 region. The user will specify here too if the chromosomes need to be flipped. 

Notes: You need to have all the _sum_proj.tif files and the _str.tif files in the directory. 
It'll look for time point 0 and if it finds it, it will use it as the basis to know if it needs to flip the chromosomes. 

The script will create the crossover_roi.roi file contianing the roi with the rectangle roi correpsonding to the crossover.

It will also create the plot profiles used to get the diffusion of the photoconverted SC. 

*/

//set the expandable arrays
setOption("ExpandableArrays", true);

//close all images
close("*");

//do it in batch
setBatchMode(true);

//get the directory
main_dir = getDir("Select the directory");

//get the file list
file_list = getFileList(main_dir);

//start a new array that will hold all the _sum_proj cases
sum_proj_files = newArray();

//start a new array tha will hold all the fliped _sum_proj cases
fliped_list = newArray();

//counter of sum proj
counter_of_sums = 0;

//loop through the file list
for (a = 0; a < file_list.length; a++) {
	
	//get the idnex of _sum_proj
	index_of_sum = indexOf(file_list[a], "_str_sum_proj.tif");
	
	//if the index is different to -1
	if (index_of_sum >= 0) {

		//add it to the list
		sum_proj_files[counter_of_sums] = file_list[a];
		
		//add one to the counter
		counter_of_sums += 1; 

	}

}

//make a counter for the fliped list
fliped_counter = 0;


//loop through the sum_proj_files 
for (a = 0; a < sum_proj_files.length; a++) {
	
	//find out if the filiped version exists
	//get the flip name
	flip_name = replace(sum_proj_files[a], "proj.tif", "proj_reversed.tif");
	
	//if the flip doesn't exist
	if (!File.exists(main_dir + flip_name)) {

		//exists in list flag
		exists_flipped_flag = false;
		
		//get the base name
		current_base_name = get_base_name(sum_proj_files[a]);
		
		//get the chromosome_base_name
		chromosome_base_name = get_chromosome_base_name(sum_proj_files[a], current_base_name);
		
		
		//check if the filename exists on the flipped list
		//loop through the flipped list
		for (b = 0; b < fliped_list.length; b++) {
	
			//if the fliped_list is the same as the base_name:
			if (fliped_list[b] == chromosome_base_name) {
	
				//flip the flag
				exists_flipped_flag = true;
	
			}
	
		}
		
		//print if it exists
		print("File exists in array: "+exists_flipped_flag);
		
		//if the flipped flag is not true
		if (exists_flipped_flag == false) {
			
			//find out if it has the t0min substring
			t0_index = indexOf(sum_proj_files[a], "_t0min_");
			
			//if the index is more than 0, then flip it
			if (t0_index > 0) {

				//open the file
				open(main_dir + sum_proj_files[a]);
				
				//show the image
				setBatchMode("show");
				
				//get the image id
				sum_image_id = getImageID();
				
				//make the dialog to flip
				Dialog.createNonBlocking("Flip the chromosome?");
				
				Dialog.addCheckbox("Flip: ", false);
				
				Dialog.show();
				
				//get the result
				flip_flag = Dialog.getCheckbox();
				
				//close the image
				selectImage(sum_image_id);
				
				close();
				
				//if the flag has been set
				if (flip_flag == true) {
					
					//make a list of current base names
					current_base_name_files_array = newArray();
					
					//add the current base name to the flipped list
					fliped_list[fliped_counter] = chromosome_base_name;
					
					//add one to the fliped counter
					fliped_counter += 1;
					
					//get the list for all the files with the current base name
					for (c = 0; c < sum_proj_files.length; c++) {
						
						//get the base name of the sum_proj_file
						pre_compare_base_name = get_base_name(sum_proj_files[c]);
						
						compare_base_name = get_chromosome_base_name(sum_proj_files[c], pre_compare_base_name);
						
						//find out if they're the same
						if (compare_base_name == chromosome_base_name ) {
							
							//open the file
							open(main_dir + sum_proj_files[c]);
							
							//get the fliping image id
							fliping_image_id = getImageID();
							
							//flip the image
							run("Flip Horizontally", "stack");
							
							//get the filanem for the reversed image
							reversed_image_filename = replace(sum_proj_files[c], "sum_proj.tif", "sum_proj_reversed.tif");
							
							//if the reversed filename doesn't exist
							if (!File.exists(main_dir + reversed_image_filename)) {
	
								//save the image
								save(main_dir + reversed_image_filename);
			
							};
											
							//close all images
							close("*");
		
						}
		
					}
				
				
				}

			}
	
		}																	

	}
										
}


//loop through the sum files again
for (a = 0; a < sum_proj_files.length; a++) {
	
	//get a flag to know if the file is flipped
	flipped_flagging = false;
	
	//close all images
	close("*");
	
	//reset the roi manager
	roiManager("reset");
	
	//set up the working file name
	working_file_name = sum_proj_files[a];
	
	//get the reverse filename
	working_reversed_file_name = replace(sum_proj_files[a], "proj.tif", "proj_reversed.tif");
	
	//find out if the reversed file name exists
	if (File.exists(main_dir + working_reversed_file_name)) {

		working_file_name = working_reversed_file_name;
		flipped_flagging = true;

	}
	
	//get the crossover area name
	crossover_area_name = File.getNameWithoutExtension(working_file_name) + "_crossover_roi.roi";
	
	//if the crossover area name doesnt exist
	if (!File.exists(main_dir + crossover_area_name)) {
		
		//reset the roi manager
		roiManager("reset");
		
		print("Opening file: "+working_file_name);

		//open the file
		open(main_dir + working_file_name);

		//get the sum projection filename
		no_sum_proj_filename = replace(sum_proj_files[a], "_sum_proj.tif", ".tif");
		
		//open the sum proje file name
		open(main_dir + no_sum_proj_filename);
		
		//if the flipped_flagging is true
		if (flipped_flagging == true) {
			
			//flip the image
			run("Flip Horizontally", "stack");

		}
		
		//show the image
		setBatchMode("show");
		
		//set a flag to know if there's a square roi made
		square_roi_made = false;
		
		//do a while loop until the square roi is made
		while (square_roi_made == false) {
			
			//reset the roi manager
			roiManager("reset");
			
			//wait for the user to make the rectangle roi
			waitForUser("Make Rectangle Roi");
		
			//get the current roi
			roi_type = Roi.getType;
			
			//if the roi type is rectangle
			if (roi_type == "rectangle") {

				//add it to the roi manager
				roiManager("add");
				
				//select none
				run("Select None");
				
				//select the roi from the manager
				roiManager("select", 0);
				
				//rename it to co_area
				roiManager("rename", "co_area");
				
				//save the roi manager
				roiManager("save selected", main_dir + crossover_area_name);
				
				//close all images
				close("*");
				
				//reset the roi manager
				roiManager("reset");
				
				//set the flag to true
				square_roi_made = true;
				

			}
			
			//if the roi type is different to rectangle
			if (!(roi_type == "rectangle")) {

				//print the error
				showMessage("Roi Type Error", "The roi you created was not rectangle. Do it with a rectangle roi please.");
				
				//select none
				run("Select None");

			}	
	
		}

	}
	
}

//print that you're done
print("Finished c069_flip_get_crossover_area_profile.ijm");

/////////////// get the plot profiles //////////////////////////

//loop through the sum files again
for (a = 0; a < sum_proj_files.length; a++) {
	
	//reset the results
	run("Clear Results");
	
	//set up the working file name
	working_file_name = sum_proj_files[a];
	
	//get the reverse filename
	working_reversed_file_name = replace(sum_proj_files[a], "proj.tif", "proj_reversed.tif");
	
	//find out if the reversed file name exists
	if (File.exists(main_dir + working_reversed_file_name)) {

		working_file_name = working_reversed_file_name;

	}
	
	//get the final_plot_profile_name
	plot_profile_name = File.getNameWithoutExtension(working_file_name) + "_plot_profile.csv";
	
	//find out if the plot_profile_name exists
	if (!File.exists(main_dir + plot_profile_name)) {
	
		//open the working file name
		open(main_dir + working_file_name);
		
		//get the dimensions
		getDimensions(current_width, current_height, current_channels, current_slices, current_frames);
		
		//get the filename without extension
		no_ext_part = File.getNameWithoutExtension(working_file_name);
		
		//get the crossover roi file name
		crossover_roi_file_name = no_ext_part + "_crossover_roi.roi";
		
		//load the roi if it exists
		roiManager("reset");
				
		//load the file
		roiManager("open", main_dir + crossover_roi_file_name);
		
		//select the first roi
		roiManager("select", 0);
		
		//get the roi points
		Roi.getBounds(roi_x, roi_y, roi_width, roi_height);
		
		//set the starting
		co_start = roi_x;
		
		//get the co_end		
		co_end = roi_x + roi_width;
		
		//get the co_mid_point
		co_mid_point = co_start + Math.ceil((((co_end) - (co_start))/2));
		

		
		//select the roi
		
		//looop through the width
		for (b = 0; b < current_width; b++) {
		
			
			//loop through the channels
			for (c = 0; c < current_channels; c++) {
				
				//set the channel
				Stack.setChannel(c+1);
				
				//reset the sum
				current_channel_sum = 0;
				
				//loop through the height
				for (d = 0; d < current_height; d++) {
					
					//get the pixel value
					pixel_value = getPixel(b, d);
					
					//sum it to the current channel sum
					current_channel_sum = current_channel_sum + pixel_value;
					
				}
				
				//add it to the results
				setResult("channel"+(c+1), b, current_channel_sum);
		
			}
			
			//set the result
			setResult("co_start", b, co_start);
			setResult("co_end", b, co_end);
			setResult("co_mid", b, co_mid_point);

		}
		
		//close all the images
		close("*");
		
		//get the saving_plot_filename
		saving_plot_profile_file_name = no_ext_part + "_profile.csv";
		
		//select the results window
		selectWindow("Results");
		
		//save as
		saveAs("results", main_dir + saving_plot_profile_file_name);
		
		//reset results
		run("Clear Results");

	}
	
}


//function to get the base name
function get_base_name(current_name) {
	
	//get the index of gonad
	index_of_gonad = indexOf(current_name, "_gonad") + 6;
	
	//get the substring
	until_gonad_string = substring(current_name, 0, index_of_gonad);
	
	//get the after gonad
	after_gonad_string = substring(current_name, index_of_gonad);
	
	//get the index of the underscore
	underscore_index = indexOf(after_gonad_string, "_");
	
	//get the gonad number
	gonad_number = substring(after_gonad_string, 0, underscore_index);
	
	//get the returning base name
	base_name_returning = until_gonad_string + gonad_number;
	
	//return it
	return base_name_returning;
	
}

function get_chromosome_base_name(current_name, base_name) {
	
	//get the index of _sbs
	sbs_index = indexOf(current_name, "_sbs") + 4;
	
	//get everything after the "_sbs"
	after_sbs = substring(current_name, sbs_index);
	
	//get the index of the next _
	index_of_underscore = indexOf(after_sbs, "_");
	
	//get the sbs number
	sbs_number = substring(after_sbs, 0, index_of_underscore);
	
	//do the same with the chromosmoe number
	//get the index of _sbs
	chr_index = indexOf(current_name, "_chr") + 4;
	
	//get everything after the "_sbs"
	after_chr = substring(current_name, chr_index);
	
	//get the index of the next _
	index_of_underscore = indexOf(after_chr, "_");
	
	//get the sbs number
	chr_number = substring(after_chr, 0, index_of_underscore);
	
	//set the complete base name
	complete_base_name = base_name + "_sbs" + sbs_number + "_chr" + chr_number;
	
	return complete_base_name;
	
}










