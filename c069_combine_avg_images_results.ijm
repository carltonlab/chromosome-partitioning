/*

This script gets the resulting_avg_image from the photoconverted images and normalizes them, combined them and 
saves the combinging_co_points_image_rois.

You need to have all the "prebleach, t0min, t3min, t6min and t9min resutling images in a single directory.

It'll ask you to get the crossover mid points (Images will be aligned by this roi)

After getting the mid points, the images will be normalized and saved with the extension "_normalized.tif"

It'll also combine them vertically with 8 pixel separation and save the resulting image with the file name:
c069_resulting_avg_image_normalized_combined_time_points.tif

*/





//script to align the images based on their start and end crossover sites

//set up the expandable arrays
setOption("ExpandableArrays", true);

//set up the batch mode
setBatchMode(true);

//set up the time point order array
time_point_order = newArray();

time_point_order[0] = "prebleach";
time_point_order[1] = "t0min";
time_point_order[2] = "t3min";
time_point_order[3] = "t6min";
time_point_order[4] = "t9min";

//set the pixel separator
pixel_separator = 8;

//get the main directorynormalized.tif
main_dir = getDir("Select the main directory");

//get the file list
file_list = getFileList(main_dir);

//get the working file list
working_file_list = newArray();

//get a string for the combining co points
combining_co_points_file = "none";

//get a working counter
working_counter = 0;

//loop through the file list
for (a = 0; a < file_list.length; a++) {
	
	//close all images
	close("*");
	
	//get the index of positive
	index_of_positive = indexOf(file_list[a], "resulting_avg_image");
	
	//get the index of normalized
	index_of_normalized = indexOf(file_list[a], "normalized");
	
	//get the index of combining co points
	index_of_points = indexOf(file_list[a], "combining_co_points");
	
	//if it is more than -1
	if (index_of_positive > -1 && index_of_normalized == -1) {
		
		//add it to the working file list
		working_file_list[working_counter] = file_list[a];
		
		//if the working counter is 0
		if (working_counter == 0) {
	
			//open the file
			open(main_dir + file_list[a]);
			
			//get the dimensions
			getDimensions(original_width, original_height, original_channels, original_slices, original_frames);
			
			//close all images
			close("*");

		}
		
		//add one to the counter
		working_counter += 1;

	}
	
	//if combininb crossover points is more than -1
	if (index_of_points > -1) {

		//set the combininb poitns file
		combining_co_points_file = file_list[a];
	
	}

}


//start a new Array for the co centers
co_centers = newArray();

//get the right sides 
right_sides_length = newArray();

//reset the roi manager
roiManager("reset");

//if it is not nonce
if (combining_co_points_file != "none") {

	//reset the roi manager
	roiManager("reset");
	
	//open the file
	roiManager("open", main_dir + combining_co_points_file);
	
	//get the roi count
	roi_count = roiManager("count");
	
}

//loop through the working file list
for (a = 0; a < working_file_list.length; a++) {
	
	//close all images
	close("*");
	
	//reset the xpoints and ypoints just in case
	xpoints = 0;
	ypoints = 0;
	
	//open the image
	open(main_dir + working_file_list[a]);
	
	//get the dimensions
	getDimensions(current_width, current_height, current_channels, current_slices, current_frames);
	
	//if the points file is none
	if (combining_co_points_file == "none") {
		
		//set the batch mode to show
		setBatchMode("show");
		
		//wait for the user to set up the point
		waitForUser("Select the crossover mid point with the multiple point tool");
		
		//add the roi manager
		roiManager("add");
		
		//select the roi
		roiManager("select", a);
		
		//change the name
		roiManager("rename", working_file_list[a]);
					
		//get the point
		Roi.getCoordinates(xpoints, ypoints);
		
		//deselect the roi manager
		roiManager("deselect");
	
	}
	
	//if it is not nonce
	if (combining_co_points_file != "none") {
		
		//select the roi manager roi by loooping and finding the string
		for (b = 0; b < roi_count; b++) {
			
			//deselect the roi
			roiManager("deselect");
			
			//select the roi
			roiManager("select", b);
			
			//get the name
			roi_name = Roi.getName;
			
			//if the roi name and the working file are the same
			if (roi_name == working_file_list[a]) {
				
				//get the coordinates
				Roi.getCoordinates(xpoints, ypoints);

			}


		}

	}
	
	//deselect the roi manager
	roiManager("deselect");
	
	//add the crossover center
	co_centers[a] = xpoints[0];
	
	//get the right side length
	right_length = ((current_width) - (co_centers[a]));
	
	//add it to the array
	right_sides_length[a] = right_length;	
	
	//close all images
	close("*");

}

//if it is none for the co points file
if (combining_co_points_file == "none") {
	
	//get the file name
	co_points_filename = "c069_combining_co_points_image_rois.zip";
	
	//save the file
	roiManager("save", main_dir + co_points_filename);
	
	//reset the roi manager
	roiManager("reset");

}


//get the max left
Array.getStatistics(co_centers, co_min, co_max, co_mean, co_stdDev);

//get the max right
Array.getStatistics(right_sides_length, right_min, right_max, right_mean, right_stdDev);

//get the total length 
total_length = co_max + right_max;

//make the combining and combined just to speed the typing here
combining = "combining";
combined = "combined";

//get the prebleach stats for normalization
for (i = 0; i < working_file_list.length; i++) {
	
	//find out if it is a prebleach
	if (indexOf(working_file_list[i], "prebleach") > -1) {
		
		//open the image
		open(main_dir + working_file_list[i]);
		
		//set the channel to 1
		Stack.setChannel(1);
		
		//get the raw statistics
		getRawStatistics(nPixels, mean, min, max, std, histogram);
		
		//get the mean
		green_mean = mean;
		
		//close all images
		close("*");
		
	}

}

//get the base saving name

//now, loop through the time points to set up the image in order
for (a = 0; a < time_point_order.length; a++) {
	
	//get the current time point
	current_time_point = time_point_order[a];
	
	//loop through the working file list
	for (b = 0; b < working_file_list.length; b++) {
		
		
		
		//get the index of the current time point
		time_point_index = indexOf(working_file_list[b], current_time_point);
		
		//if the index is more than -1
		if (time_point_index > -1) {
			
			//get the current base name
			base_saving_name = replace(working_file_list[b], current_time_point + ".tif", "");
						
			//open the file
			open(main_dir + working_file_list[b]);
			
			//get the dimensions
			getDimensions(combining_width, combining_height, combining_channels, combining_slices, combining_frames);
			
			//rename the window to merging
			rename("combining");
			
			//get the raw statistics
			getRawStatistics(nPixels, mean, min, max, std, histogram);
			
			//get the ratio of the prebleach with this
			current_ratio = green_mean / mean;
			
			//get the merging window id as the current id
			combining_id = getImageID();
			
			//multiply the image
			run("Multiply...", "value="+current_ratio+" stack");
			
			//get the normalized image file name
			normalized_file_name = File.getNameWithoutExtension(working_file_list[b]) + "_normalized.tif";
			
			//save the normalized image
			save(main_dir + normalized_file_name);
			
			//rename to combining
			rename(combining);
			
			//get the id
			combining_id = getImageID();
			
			//get the left and right differences
			left_difference = ((co_max) - (co_centers[b]));
			right_difference = ((right_max) - (right_sides_length[b]));
			
			//if there's a difference for the left
			if (left_difference > 1) {
				
				//make the image
				newImage("left_image", "32-bit", left_difference, original_height, original_channels);
				
				//select the window
				selectWindow("left_image");
				
				//correct the channels
				run("Stack to Hyperstack...", "order=xyczt(default) channels=2 slices=1 frames=1 display=Grayscale");
				
				//combine the images
				run("Combine...", "stack1=left_image stack2=combining");
				
				//select the combined stacks window
				selectWindow("Combined Stacks");
				
				//rename to combining
				rename("combining");
				
				//get the image id
				combining_id = getImageID();
			
			}
			
			//now with the right difference
			if (right_difference > 1) {
			
				//make a new image for the right side
				newImage("right_image", "32-bit", right_difference, original_height, original_channels);
				
				//select the window
				selectWindow("right_image");
				
				//correct the channels
				run("Stack to Hyperstack...", "order=xyczt(default) channels=2 slices=1 frames=1 display=Grayscale");
				
				//combine the images
				run("Combine...", "stack1=combining stack2=right_image");

				//select the window
				selectWindow("Combined Stacks");				
				
				//rename to combining
				rename("combining");
				
				//get the id
				combining_id = getImageID();

			}
			
			//get the separator image
			newImage("sep", "32-bit", total_length, pixel_separator, original_channels);
			
			//get it into channels
			run("Stack to Hyperstack...", "order=xyczt(default) channels=2 slices=1 frames=1 display=Grayscale");
			
			//combine the images
			run("Combine...", "stack1=[combining] stack2=[sep] combine");
			
			//select the combined stacks window
			selectWindow("Combined Stacks");
			
			//rename to combining
			rename("combining");
			
			//get the ccombining id
			combining_id = getImageID();			
		
			//if it is the first time point
			if (a == 0) {
				
				//select the combining id
				selectImage(combining_id);
				
				//rename the window to combined
				rename("combined");
				
				//set the combined window id
				combined_id = getImageID();
				
			}
			
			//if it is not the first time point
			if (a > 0) {
				
				//combine the combined and combining
				run("Combine...", "stack1=[combined] stack2=[combining] combine");
				
				//select the combined stacks window
				selectWindow("Combined Stacks");
				
				//rename it to combined
				rename("combined");
				
				//get the combined id
				combined_id = getImageID();

			}
			

		}
		
		
	}
	
}

//set the scale
run("Set Scale...", "distance=23.4752 known=1 unit=micron");

//get the saving image file name
saving_filename = base_saving_name + "normalized_combined_time_points.tif";

//save the image
save(main_dir + saving_filename);

//close all images
close("*");

//end the batch mode
setBatchMode("exit and display");

//open the image
open(main_dir + saving_filename);

//print the the script is done running
print("script c069_combine_avg_images_results.ijm done running");









