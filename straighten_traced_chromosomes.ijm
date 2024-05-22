//This script uses the exported rois from the "trace_and_export_rois.py" to straighten the chromosomes.
//To run, open the script on the fiji script editor and run it. 
//It'll ask you for the file you with to straighten. Please note the the file names of the 
//image and the rois should match ("File should be a .tif image and the rois share the name
//of the image replacing the .tif extension with _rois.zip)

//to use the script make sure that the file extension is correct
sbs_file_extension = ".tif";

//get the file you're cutting to get name and directory
file_path = File.openDialog("Select the file you're using to save straightened files");

//open the file
open(file_path);

//filename without extension
no_extension_filename = File.getNameWithoutExtension(file_path);

//get the parent directory
parent_path = File.getParent(file_path)+"/";

//in case you need to background substract
roix = 0;
roiy = 0;
roiwidth = 0;
roiheight = 0;


//setting up a little dialog to get the number of chromosomes, the z-sections and width
Dialog.createNonBlocking("Set the parameters");

//adding the dialog components
Dialog.addNumber("Z-sections", 5);
Dialog.addNumber("Straighten width", 11);
Dialog.addCheckbox("Show str at the end", true);
Dialog.show();

//getting the dialog parameters into variables
z_section_number = Dialog.getNumber();
width_final = Dialog.getNumber();
show_flag = Dialog.getCheckbox();

//////////////////////////////////////////////////////////////////////////


//saving the roi manager
//roi_manager_filename = no_extension_filename+"_rois.zip";
//roiManager("save", parent_path+roi_manager_filename);

//////////////////////////////////////////////////////////////////////////

//This is to remake the straight
//get the roi manager file name
roi_manager_filename = no_extension_filename+"_rois.zip";

//open it
roiManager("open", parent_path+roi_manager_filename);


//getting the halves
z_final_halves = (z_section_number-1)/2;

//get the position m
position_m = z_final_halves+1;

//get the window title
window_title = getTitle();

//getting the dimensions
getDimensions(width, height, channels, slices, frames);

//count the roi manager
number_of_rois = roiManager("count");

//getting the number of chromosomes
//getting the last roi
roiManager("select", ((number_of_rois)-(1)));
last_roi_name = Roi.getName;

roiManager("deselect");

last_roi_start_index = indexOf(last_roi_name, "chr") + 3;

dash_roi_end_index = indexOf(last_roi_name, "-");

number_of_chromosomes = substring(last_roi_name, last_roi_start_index, dash_roi_end_index);

//getting an array to hold the number of segments for each chromosome
number_of_segments_per_chromosome_array = newArray(number_of_chromosomes);

//use the function to get the number of segments per chromosome in the array
number_of_segments_per_chromosome_array = get_segments_counted(number_of_segments_per_chromosome_array, number_of_rois, window_title);

//get an array to show the str at the end
if (show_flag == true) {

	//make the array 
	show_names_arrau = newArray(number_of_chromosomes);

};

//start making the straigthened and merged chromosome files
//first you need to loop through all of the chromosomes according to the count
//also, you need to make a small counter for the current roi
current_roi = 0;

//set the batch mode
setBatchMode(true);

setBatchMode("hide");

//looping
for (a = 0; a < number_of_chromosomes; a++) {

	//get a variable that restarts each chromosmoe and counts the current roi in the chromosome
	current_roi_in_chr = 0;

	//then, you need to loop through the each one of the segments per chromosome
	for (b = 0; b < number_of_segments_per_chromosome_array[a]; b++) {
				
		//if it is the first, then prepare the name of the file and other variables
		if (b == 0) {
						
			//prepare the names
			str_file_name = no_extension_filename + "_chr"+(a+1)+"_str.tif";
			
			proj_file_name =  no_extension_filename + "_chr"+(a+1)+"_str_sum_proj.tif";
			
			proj_nan_file_name = no_extension_filename + "_chr"+(a+1)+"_str_sum_proj_nan.tif";
			
		};		
		
		//select the main window
		selectWindow(window_title);
		
		//make the current roi selection with the roi manager
		roiManager("select", current_roi);
			
		//getting the roi position
		Roi.getPosition(roi_channel, roi_slice, roi_frame);
		Roi.getCoordinates(xpoints, ypoints);
		
		//selecting none
		run("Select None");
		
		//making a new polyline selection
		makeSelection("polyline", xpoints, ypoints);
		
		//add one to the roi in chr
		current_roi_in_chr += 1;
		
		//adding one to the roi 
		current_roi += 1;
		
		selectWindow(window_title);
										
		//run the straighten function
		straighten_segment(width, height, channels, slices, roi_slice, width_final, z_final_halves, a);	
				
		//run the combine function for multiple segments when needed
		combine_segments(current_roi_in_chr, number_of_segments_per_chromosome_array[a], str_file_name);

		
	};		
	
	//saving the name in the show array if it is selected
	if (show_flag == true) {

		show_names_arrau[a] = str_file_name;
		
	};
	
	//now, save the file
	selectWindow(str_file_name);
			
	//save the window
	save(parent_path+str_file_name);
		
	//make a sum projection
	run("Z Project...", "projection=[Sum Slices]");
	
	//get the sumed_image_id
	summed_image_id = getImageID();
	
	//save the projected image
	save(parent_path + proj_file_name);
	
	//select the projected image
	selectImage(summed_image_id);
	
	//close
	close();
	
	//select the str_filename
	selectWindow(str_file_name);
	
	close();
	
	//close the str file
	close(str_file_name);	
	
};

//show the str if flag is risen
if (show_flag == true) {

	//loop through the chromosomes and open them
	for (i = 0; i < number_of_chromosomes; i++) {
		
		//open
		open(parent_path+show_names_arrau[i]);
		
		//set the slice to the position middle
		setSlice(position_m);
		
		//set the location of the window
		setLocation((i*(screenWidth/((number_of_chromosomes)*(2)))), (screenHeight/3));
		
	};

};

setBatchMode("exit and display");




////////////////////////////////////////   FUNCTIONS      ////////////////////////////////////////////


//================ combine segments =====================================

//function to combine the segments when you need
function combine_segments(current_roi_in_chr, number_of_segments_in_chr, str_file_name) {
		
	//if it is the first segment in the chromosome then just rename the sbs_to_merged
	if (current_roi_in_chr == 1) {

		//select the window and just rename it
		selectWindow("str_concat");
		
		//rename it to merged
		rename("merged");

	};

	//if it is more than one and the current roi in chr is smaller than the total number of segmeents 
	//you need to combine the previous and the new one
	if (current_roi_in_chr > 1) {

		//get the previous and current images and combine them
		run("Combine...", "stack1=merged stack2=str_concat");
		
		//rename it to merged
		rename("merged");
		
	};
	
	//if it was the last one, then name it to the file name
	if (current_roi_in_chr == number_of_segments_in_chr) {

		//select the window
		selectWindow("merged");
		
		//rename it to the file name
		rename(str_file_name);

	};
	
};

roiManager("deselect");
roiManager("delete");









//================ get segments counted =====================================

//function to get the chromosome segments counted
function get_segments_counted(number_of_segments_per_chromosome_array, number_of_rois, window_title) {
		
	//make a loop through the rois
	for (b = 0; b < number_of_rois; b++) {
		
		//if it is the first roi, get some variables going to help the function
		if (b == 0) {
			
			//set up the previous chromosome variable
			previous_chromosome = (-2);
			
			//set up the current chromosome variable
			current_chr = (-1);

		};
		
		//selecting the window
		selectWindow(window_title);
				
		//selecting the current roi
		roiManager("select", b);
		
		//getting the roi name
		current_roi_name = Roi.getName;
		
		//getting the chromosome number for this roi
		current_roi_chr_number_string = substring(current_roi_name, 3, indexOf(current_roi_name, "-"));
		
		//getting the int form this string
		current_roi_int = parseInt(current_roi_chr_number_string);
		
		//compare the previous and current
		if (current_chr != (current_roi_int-1)) {
			
			//get the chrom
			previous_chromosome = current_chr;
						
			//if it is differenct, add one to the current chromosome 
			current_chr += 1;
		
			//populate the array with a 0
			number_of_segments_per_chromosome_array[current_chr] = 0;
			
		};
		
		//add one to the current chromosome
		number_of_segments_per_chromosome_array[current_chr] += 1;		
		
	};
	
	
	
	return number_of_segments_per_chromosome_array;
	
};



//================ straighten the segmens =====================================

//getting a function to strighten the segment and re arm it
function straighten_segment(str_width, str_height, str_channels, str_slices, str_roi_slice, width_final, z_halves,a) {
	
	//select the window
	selectWindow(window_title);
		
	//first, we need to get the str image
	run("Straighten...", "title=merging line="+width_final+" process");
		

	
			
	//making two different flags for substractions of zs later.... imagej is stupid....
	down_up_flags_real = newArray(2);
	
	//populating the array
	for (d = 0; d < 2; d++) {

		//with 0s
		down_up_flags_real[d] = 0;

	};
		
	//selecting the merging window
	selectWindow("merging"); 
	
	//set to 32-bit
	run("32-bit");
	
	//getting the dimensions of the window 
	getDimensions(new_width, new_height, new_channels, new_slices, new_frames);
	
	//Putting it back into the hyperstack
	run("Stack to Hyperstack...", "order=xyczt(default) channels="+str_channels+" slices="+str_slices+" frames=1 display=Grayscale");
	
	//getting the window title
	str_multi_title = getTitle();
	
	//declaring variables to start and end the keeping
	start_keep = 0;
	end_keep = 0;
	
	//if you need slices down
	substraction_result = str_roi_slice - z_halves;
	
	//if you need slices up
	adding_result = str_slices - (str_roi_slice + z_halves);
	
	//adding an array to hold the flags for up and down increases
	down_up_increase = newArray(2);
	
	//adding up an array to hold the window titles of all the combining images
	//it will be (down, str, up)
	combining_images_titles_array = newArray(3);
	
	//populating it
	combining_images_titles_array[0] = "extra_down";
	combining_images_titles_array[2] = "extra_up";
	
	//getting the variables to keep 
	//if you don't need to add to the lower part:
	if (substraction_result > 0) {
		
		//set the start at whatever z-section it is
		start_keep = substraction_result;
		
		//setting the flag to 0
		down_up_increase[0] = 0;
				
	};
	
	//if you need to add to the lower part:
	if (substraction_result <= 0) {
		
		//set the start at 1
		start_keep = 1;
		
		//set the flag to the number of slices you need
		down_up_increase[0] = abs(substraction_result)+1;
		
		real_down = down_up_increase[0];
		
		//if the depth = 1, then it is going to fail because imagej is stupid... adding one, raising the flag and then substracting...
		if (down_up_increase[0] == 1) {

			//set it to two... maybe will work...
			real_down = 2;
			
			//raise the flag....
			down_up_flags_real[0] = 1;
				
		};		
		
		//getting the down depth
		down_depth = real_down * str_channels;	
		
		//now, make the extra images
		newImage("extra_down", "32-bit", new_width, new_height, down_depth);
			
		//Putting it back into the hyperstack
		run("Stack to Hyperstack...", "order=xyczt(default) channels="+str_channels+" slices="+real_down+" frames=1 display=Grayscale");
		
		//getting the title
		down_title = getTitle();
		
	};
	
	//do the same with up
	if (adding_result >= 0) {
		
		//set the end at the adding result
		end_keep = str_roi_slice + z_halves;
		
		//set the flag to 0
		down_up_increase[1] = 0;
	
	};
	
	if (adding_result < 0) {
		
		//set the end at the max slice
		end_keep = str_slices;
		
		//set the flag to the number of extra slices you need
		down_up_increase[1] = abs(adding_result);
		
		//getting the real up
		real_up = down_up_increase[1];
		
		//if the up increase is just one, add one to the real up variable and raise the flag
		if (real_up == 1) {
	
			//adding one
			real_up = 2;
			
			//raising flag
			down_up_flags_real[1] = 1;

		};
		
		//getting the up increase in depth
		up_depth = real_up * str_channels;
		
		//now, make the extra images
		newImage("extra_up", "32-bit", new_width, new_height, up_depth);
		
		//Putting it back into the hyperstack
		run("Stack to Hyperstack...", "order=xyczt(default) channels="+str_channels+" slices="+real_up+" frames=1 display=Grayscale");
		
		//getting the title
		up_title = getTitle();
														
	};
	
	//selecting the window
	selectWindow(str_multi_title);
	
	//making the subset of the image to combine later
	run("Make Subset...", "channels=1-"+str_channels+" slices="+start_keep+"-"+end_keep);
	
	//renaming the subset to str_concat
	rename("str_concat");
	
	//get the title for this subset
	subset_title = getTitle();
	
	//close the original straightened image
	close(str_multi_title);
	
	//adding the title to the combining images title array
	combining_images_titles_array[1] = subset_title;
	
	//now check if you need to add up or down again
	for (b = 0; b < down_up_increase.length; b++) {
		
		//check if it is more than 0
		if (down_up_increase[b] > 0) {
			
			//combining them
			run("Concatenate...", "  title=str_concat open image1="+combining_images_titles_array[b]+" image2="+combining_images_titles_array[b+1]+" image3=[-- None --]");		

			//getting the dimensions of the current image
			getDimensions(conc_width, conc_height, conc_channels, conc_slices, conc_frames);

			//getting the title updated in the array
			combining_images_titles_array[1] = "str_concat";
			
			//removing the slices of up or down if the flag is active
			if (down_up_flags_real[b] == 1) {

				//if it is down, then remove one down
				if (b == 0) {
					
					//selectint the window
					selectWindow("str_concat");
										
					//keep the slices
					run("Make Subset...", "channels=1-"+str_channels+" slices=2-"+conc_slices);
					
					//getting the title
					new_conc_title = getTitle();
					
					//closeing the previously made concat
					close("str_concat");
					
					//selecting the new_conc
					selectWindow(new_conc_title);
					
					//renaming
					rename("str_concat");							

				};
				
				//now, if b == 1, then do the same for the upper
				if (b == 1) {
					
					//selecting the concat window
					selectWindow("str_concat");
					
					//keep the slices
					run("Make Subset...", "channels=1-"+str_channels+" slices=1-"+(conc_slices-1));
					
					//getting the title
					new_conc_title = getTitle();
					
					//closeing the previously made concat
					close("str_concat");
					
					//selecting the new_conc
					selectWindow(new_conc_title);
					
					//renaming
					rename("str_concat");										

				};	

			};
			
		};
		
	};	
									
};