/*

	This script will take the split chromosomes and will measure the short and long arms. 
	
	The file will look for all the _str files and then get the corresponding 
	"_str_split_co1_sum_proj.tif" and the "_str_split_co2_sum_proj.tif". It will then use the crossover c018_split_megasomes
	to generate the rois that include the co_site and the short and long arm square rois.
	It will measure the short and long arm rois average intensities for the pansyp1 channel and the syp1phos channel. 

	The final results are saved as a csv file with the following header:
	index, filename, short_arm_mean, long_arm_mean, short_arm_length, long_arm_length, chr_height, short_arm_area, long_arm_area, short_arm_int, long_arm_int

	The results filenames for the split images co1 and co2 terminates with: "_short_long_arm_measurements.csv"
	The rois filenames for the split images co1 and co2 terminates with: "short_long_arm_rois.zip"

	Run the script from the imagej script editor. 

	For it to work you need to have already measured the crosssover positions using the script
	"get_multiple_co_coords.ijm", split the megasomes using the "c018_split_megasomes.ijm" and have
	sum projected the images using the "c018_megaosmes_make_sum_projection.ijm"
	
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

	//priunt the image its working on
	print("Working on image: " + working_file_list[a]);

	//reset the results
	run("Clear Results");
	
	//reset the roi manager
	roiManager("reset");
	
	//close all images
	close("*");
	
	//get the co1 and co2 file names
	co1_filename = replace(working_file_list[a], "_str.tif", "_str_split_co1_sum_proj.tif");
	co2_filename = replace(working_file_list[a], "_str.tif", "_str_split_co2_sum_proj.tif");
	
	//get the roi file name
	roi_file_name = replace(working_file_list[a], "_str.tif", "_str_split_rois.zip");
	
	//open the main image
	open(main_dir + working_file_list[a]);
	
	//get the main image id
	main_image_id = getImageID();
	
	//set it to grayscale
	Stack.setDisplayMode("grayscale");
	
	//open the co1 filename
	open(main_dir + co1_filename);
	
	//get the co1_image_id
	co1_image_id = getImageID();
	
	Stack.setDisplayMode("grayscale");
	
	//get the co1 dimensions
	getDimensions(co1_width, co1_height, co1_channels, co1_slices, co1_frames);
	
	//open the co2 filename
	open(main_dir + co2_filename);
	
	//get the co2_imageid
	co2_image_id = getImageID();
	
	//set it to grayscale
	Stack.setDisplayMode("grayscale");
	
	//get the co2 dimensions
	getDimensions(co2_width, co2_height, co2_channels, co2_slices, co2_frames);
	
	//open the roi file
	roiManager("open", main_dir + roi_file_name);
	
	//select he main image
	selectImage(main_image_id);
	
	//select the index 0 of the roi manager
	roiManager("select", 0);
	
	//get the x points
	Roi.getCoordinates(co_xpoints, co_ypoints);
	
	//select none
	run("Select None");
	
	//select the roi 2
	roiManager("deselect");
	
	//get the mid point coordinate
	roiManager("select", 1);
	
	//get the coordinates
	Roi.getCoordinates(mid_xpoints, mid_ypoints);
	
	//select none
	run("Select None");
	
	//deselect the roi
	roiManager("deselect");
	
	//get the mid_point
	mid_point_pos = mid_xpoints[0];
	
	//get the co1 x relative coordinate
	co1_relative_pos = co_xpoints[0];
	
	//get the co2 x relative coordinate
	co2_relative_pos = ((co_xpoints[1])-(mid_point_pos));
	
	//get the y position
	y_position = co_ypoints[0];
	
	//reset the roi manager
	roiManager("reset");

	//get the chr1 roi file name
	co1_roi_filename = replace(working_file_list[a], "_str.tif", "_str_split_co1_sum_proj_short_long_arm_rois.zip");
			
	//select the co1 image
	selectImage(co1_image_id);
	
	//select the co site
	makePoint(co1_relative_pos, y_position);
	
	//add to the roi manager
	roiManager("add");
	
	//select the index 0 of the roi manager
	roiManager("select", 0);
	
	//rename to co_position
	roiManager("rename", "co_position");
	
	//deselect roi manager
	roiManager("deselect");
	
	//select none
	run("Select None");
	
	//get the half co1
	half_co1 = co1_width / 2;
	
	//set the short left
	short_left_flag = false;
	
	//if the co1_relative position is less than the half_co1
	if (co1_relative_pos <= half_co1) {
	
		short_left_flag = true;

	}
		
	//if the short_left_flag is true
	if (short_left_flag == true) {
	
		//set the short arm length
		short_arm_length = co1_relative_pos;
		
		//set the long arm length
		long_arm_length = ((co1_width)-(co1_relative_pos));
	
		//select the image id
		selectImage(co1_image_id);

		//make the left rectangle
		makeRectangle(0, 0, co1_relative_pos, co1_height);	
		
		//add it to the roi manager
		roiManager("add");
		
		//select it in the roi manager
		roiManager("select", 1);
		
		//rename it to short arm
		roiManager("rename", "short_arm");
		
		//deselect
		roiManager("deselect");
		
		//select none
		run("Select None");
		
		//get the long arm
		makeRectangle(co1_relative_pos, 0, ((co1_width)-(co1_relative_pos)), co1_height);
		
		//add it to the roi manager
		roiManager("add");
		
		//select it in the roi manager
		roiManager("select", 2);
		
		//rename it to short arm
		roiManager("rename", "long_arm");
		
		//deselect
		roiManager("deselect");
		
		//select none
		run("Select None");
					
	}
	
	else {
		
		//set the short arm length
		short_arm_length = ((co1_width)-(co1_relative_pos));
		
		//set the long arm length
		long_arm_length = co1_relative_pos;
		
		//select the image id
		selectImage(co1_image_id);
		
		//get the short arm
		makeRectangle(co1_relative_pos, 0, ((co1_width)-(co1_relative_pos)), co1_height);
		
		//add it to the roi manager
		roiManager("add");
		
		//select it in the roi manager
		roiManager("select", 1);
		
		//rename it to short arm
		roiManager("rename", "short_arm");
		
		//deselect
		roiManager("deselect");
		
		//select none
		run("Select None");
		
		//get the long arm
		makeRectangle(0, 0, co1_relative_pos, co1_height);	
		
		//add it to the roi manager
		roiManager("add");
		
		//select it in the roi manager
		roiManager("select", 2);
		
		//rename it to short arm
		roiManager("rename", "long_arm");
		
		//deselect
		roiManager("deselect");
		
		//select none
		run("Select None");
		
	}
			
	//save the roi manager
	roiManager("save", main_dir + co1_roi_filename);
	
	//select the image
	selectImage(co1_image_id);
	
	//get the short arm
	roiManager("select", 1);
	
	//clear the results
	run("Clear Results");
	
	//select the channel 1
	Stack.setChannel(1);
	
	//get the measure
	run("Measure");
	
	//get the mean
	co1_pansyp1_short_arm_mean = getResult("Mean", 0);
	
	//get the area
	co1_pansyp1_short_arm_area = getResult("Area", 0);
	
	//get the intensity
	co1_pansyp1_short_arm_intensity = getResult("RawIntDen", 0);
	
	//clear the results
	run("Clear Results");
	
	//get the syp1phos
	Stack.setChannel(2);
	
	//measure
	run("Measure");
	
	//get the mean
	co1_syp1phos_short_arm_mean = getResult("Mean", 0);
	
	//get the area
	co1_syp1phos_short_arm_area = getResult("Area", 0);
	
	//get the intensity
	co1_syp1phos_short_arm_intensity = getResult("RawIntDen", 0);
	
	//clear the results
	run("Clear Results");
	
	//select none
	run("Select None");
	
	//deselect the roi manager
	roiManager("deselect");
	
	//select the image agian
	selectImage(co1_image_id);
	
	//set the channel pansyp1
	Stack.setChannel(1);
		
	//get the long arm
	roiManager("select", 2);
	
	//measure
	run("Measure");
	
	//get the mean
	co1_pansyp1_long_arm_mean = getResult("Mean", 0);
	
	//get the area
	co1_pansyp1_long_arm_area = getResult("Area", 0);
	
	//get the intensity
	co1_pansyp1_long_arm_intensity = getResult("RawIntDen", 0);
	
	//clear the results
	run("Clear Results");
	
	//Set the syp1phos channel;
	Stack.setChannel(2);
	
	//measure
	run("Measure");
	
	//get the mean
	co1_syp1phos_long_arm_mean = getResult("Mean", 0);
	
	//get the area
	co1_syp1phos_long_arm_area = getResult("Area", 0);
	
	//get the intensity
	co1_syp1phos_long_arm_intensity = getResult("RawIntDen", 0);
	
	//clear the results
	run("Clear Results");
	
	//select none
	run("Select None");
	
	//deselect the roi manager
	roiManager("deselect");
	
	//make the results for the co1 image
	co1_results_filename = replace(working_file_list[a], "_str.tif", "_str_split_co1_sum_proj_short_long_arm_measurements.csv");
	
	//set the results file name
	setResult("filename", 0, co1_filename);
	setResult("filename", 1, co1_filename);
	
	//Set the results channel
	setResult("channel", 0, "pansyp1");
	setResult("channel", 1, "syp1phos");
	
	//set the short_arm_mean
	setResult("short_arm_mean", 0, co1_pansyp1_short_arm_mean);
	setResult("short_arm_mean", 1, co1_syp1phos_short_arm_mean);
	
	//set the long arm mean
	setResult("long_arm_mean", 0, co1_pansyp1_long_arm_mean);
	setResult("long_arm_mean", 1, co1_syp1phos_long_arm_mean);
	
	//set the short arm length
	setResult("short_arm_length", 0, short_arm_length);
	setResult("short_arm_length", 1, short_arm_length);
	
	//set the long arm length
	setResult("long_arm_length", 0, long_arm_length);
	setResult("long_arm_length", 1, long_arm_length);
	
	//set the chromosome height
	setResult("chr_height", 0, co1_height);
	setResult("chr_height", 1, co1_height);
	
	
	//set the short arm area
	setResult("short_arm_area", 0, co1_pansyp1_short_arm_area);
	setResult("short_arm_area", 1, co1_syp1phos_short_arm_area);
	
	//set the long arm area
	setResult("long_arm_area", 0, co1_pansyp1_long_arm_area);
	setResult("long_arm_area", 1, co1_syp1phos_long_arm_area);
	
	//set the short arm int
	setResult("short_arm_int", 0, co1_pansyp1_short_arm_intensity);
	setResult("short_arm_int", 1, co1_syp1phos_short_arm_intensity);
	
	//set the long arm int
	setResult("long_arm_int", 0, co1_pansyp1_long_arm_intensity);
	setResult("long_arm_int", 1, co1_syp1phos_long_arm_intensity);
	
	//save the results
	saveAs("results", main_dir + co1_results_filename);
	
	//clear the results
	run("Clear Results");
	
	//select none
	run("Select None");
	
	
	
	///////////////////////////////////////////////////////////////// Adapt to co2
	
	//reset the roi manager
	roiManager("reset");

	//get the chr1 roi file name
	co2_roi_filename = replace(working_file_list[a], "_str.tif", "_str_split_co2_sum_proj_short_long_arm_rois.zip");
			
	//select the co1 image
	selectImage(co2_image_id);
	
	//select none
	run("Select None");
	
	//select the co site
	makePoint(co2_relative_pos, y_position);
	
	//add to the roi manager
	roiManager("add");
	
	//select the index 0 of the roi manager
	roiManager("select", 0);
	
	//rename to co_position
	roiManager("rename", "co_position");
	
	//deselect roi manager
	roiManager("deselect");
	
	//select none
	run("Select None");
	
	//get the half co1
	half_co2 = co2_width / 2;
	
	//set the short left
	short_left_flag = false;
	
	//if the co1_relative position is less than the half_co1
	if (co2_relative_pos <= half_co2) {
	
		short_left_flag = true;

	}
		
	//if the short_left_flag is true
	if (short_left_flag == true) {
	
		//set the short arm length
		short_arm_length = co2_relative_pos;
		
		//set the long arm length
		long_arm_length = ((co2_width)-(co2_relative_pos));
	
		//select the image id
		selectImage(co2_image_id);

		//make the left rectangle
		makeRectangle(0, 0, co2_relative_pos, co2_height);	
		
		//add it to the roi manager
		roiManager("add");
		
		//select it in the roi manager
		roiManager("select", 1);
		
		//rename it to short arm
		roiManager("rename", "short_arm");
		
		//deselect
		roiManager("deselect");
		
		//select none
		run("Select None");
		
		//get the long arm
		makeRectangle(co2_relative_pos, 0, ((co2_width)-(co2_relative_pos)), co2_height);
		
		//add it to the roi manager
		roiManager("add");
		
		//select it in the roi manager
		roiManager("select", 2);
		
		//rename it to short arm
		roiManager("rename", "long_arm");
		
		//deselect
		roiManager("deselect");
		
		//select none
		run("Select None");
					
	}
	
	else {
		
		//set the short arm length
		short_arm_length = ((co2_width)-(co2_relative_pos));
		
		//set the long arm length
		long_arm_length = co2_relative_pos;
		
		//select the image id
		selectImage(co2_image_id);
		
		//get the short arm
		makeRectangle(co2_relative_pos, 0, ((co2_width)-(co2_relative_pos)), co2_height);
		
		//add it to the roi manager
		roiManager("add");
		
		//select it in the roi manager
		roiManager("select", 1);
		
		//rename it to short arm
		roiManager("rename", "short_arm");
		
		//deselect
		roiManager("deselect");
		
		//select none
		run("Select None");
		
		//get the long arm
		makeRectangle(0, 0, co2_relative_pos, co2_height);	
		
		//add it to the roi manager
		roiManager("add");
		
		//select it in the roi manager
		roiManager("select", 2);
		
		//rename it to short arm
		roiManager("rename", "long_arm");
		
		//deselect
		roiManager("deselect");
		
		//select none
		run("Select None");

		
	}
	
	//save the roi manager
	roiManager("save", main_dir + co2_roi_filename);
	
	//select the image
	selectImage(co2_image_id);
	
	//get the short arm
	roiManager("select", 1);
	
	//clear the results
	run("Clear Results");
	
	//select the channel 1
	Stack.setChannel(1);
	
	//get the measure
	run("Measure");
	
	//get the mean
	co2_pansyp1_short_arm_mean = getResult("Mean", 0);
	
	//get the area
	co2_pansyp1_short_arm_area = getResult("Area", 0);
	
	//get the intensity
	co2_pansyp1_short_arm_intensity = getResult("RawIntDen", 0);
	
	//clear the results
	run("Clear Results");
	
	//get the syp1phos
	Stack.setChannel(2);
	
	//measure
	run("Measure");
	
	//get the mean
	co2_syp1phos_short_arm_mean = getResult("Mean", 0);
	
	//get the area
	co2_syp1phos_short_arm_area = getResult("Area", 0);
	
	//get the intensity
	co2_syp1phos_short_arm_intensity = getResult("RawIntDen", 0);
	
	//clear the results
	run("Clear Results");
	
	//select none
	run("Select None");
	
	//deselect the roi manager
	roiManager("deselect");
	
	//select the image agian
	selectImage(co2_image_id);
	
	//set the channel pansyp1
	Stack.setChannel(1);
		
	//get the long arm
	roiManager("select", 2);
	
	//measure
	run("Measure");
	
	//get the mean
	co2_pansyp1_long_arm_mean = getResult("Mean", 0);
	
	//get the area
	co2_pansyp1_long_arm_area = getResult("Area", 0);
	
	//get the intensity
	co2_pansyp1_long_arm_intensity = getResult("RawIntDen", 0);
	
	//clear the results
	run("Clear Results");
	
	//Set the syp1phos channel;
	Stack.setChannel(2);
	
	//measure
	run("Measure");
	
	//get the mean
	co2_syp1phos_long_arm_mean = getResult("Mean", 0);
	
	//get the area
	co2_syp1phos_long_arm_area = getResult("Area", 0);
	
	//get the intensity
	co2_syp1phos_long_arm_intensity = getResult("RawIntDen", 0);
	
	//clear the results
	run("Clear Results");
	
	//select none
	run("Select None");
	
	//deselect the roi manager
	roiManager("deselect");
	
	//make the results for the co1 image
	co2_results_filename = replace(working_file_list[a], "_str.tif", "_str_split_co2_sum_proj_short_long_arm_measurements.csv");
	
	//set the results file name
	setResult("filename", 0, co2_filename);
	setResult("filename", 1, co2_filename);
	
	//Set the results channel
	setResult("channel", 0, "pansyp1");
	setResult("channel", 1, "syp1phos");
	
	//set the short_arm_mean
	setResult("short_arm_mean", 0, co2_pansyp1_short_arm_mean);
	setResult("short_arm_mean", 1, co2_syp1phos_short_arm_mean);
	
	//set the long arm mean
	setResult("long_arm_mean", 0, co2_pansyp1_long_arm_mean);
	setResult("long_arm_mean", 1, co2_syp1phos_long_arm_mean);
	
	//set the short arm length
	setResult("short_arm_length", 0, short_arm_length);
	setResult("short_arm_length", 1, short_arm_length);
	
	//set the long arm length
	setResult("long_arm_length", 0, long_arm_length);
	setResult("long_arm_length", 1, long_arm_length);
	
	//set the chromosome height
	setResult("chr_height", 0, co2_height);
	setResult("chr_height", 1, co2_height);
	
	
	//set the short arm area
	setResult("short_arm_area", 0, co2_pansyp1_short_arm_area);
	setResult("short_arm_area", 1, co2_syp1phos_short_arm_area);
	
	//set the long arm area
	setResult("long_arm_area", 0, co2_pansyp1_long_arm_area);
	setResult("long_arm_area", 1, co2_syp1phos_long_arm_area);
	
	//set the short arm int
	setResult("short_arm_int", 0, co2_pansyp1_short_arm_intensity);
	setResult("short_arm_int", 1, co2_syp1phos_short_arm_intensity);
	
	//set the long arm int
	setResult("long_arm_int", 0, co2_pansyp1_long_arm_intensity);
	setResult("long_arm_int", 1, co2_syp1phos_long_arm_intensity);
	
	//save the results
	saveAs("results", main_dir + co2_results_filename);
	
	//clear the results
	run("Clear Results");
	
	//clear the roi manager
	roiManager("reset");
	
	//close all images
	close("*");	

}






