/*

This script will do the following:

Create the masks for the red and green channels. 

Do the background subtraction. 

Crop the photoconverted nuclei. 

Save the relevant images and rois. 

You already need the green_classifier.model files coming from the script: "cc069_create_classifiers_for_green_channels.ijm"

This makes most of the work for the background subtraction. 

Run the script from the script editor in imagej.

*/


//you need to have the classifier.model for the images already in the directory. It'll take those as the basis for the image generation. 

//set the expandable arrays to true
setOption("ExpandableArrays", true);

//set the batchmode to on
setBatchMode(true);

//close all images
close("*");

//set the scales
//run("Set Scale...", "distance=23.4752 known=1 unit=micron");

//get the channel array
channels_array = newArray(2);

channels_array[0] = "green";
channels_array[1] = "red";

//set up the special backgrounds array
special_backgrounds_array = newArray(2);

special_backgrounds_array[0] = false;
special_backgrounds_array[1] = true;


//get the main directory
main_dir = getDir("Select the main directory");

//get the file list
file_list = getFileList(main_dir);

//set the model list
model_list = newArray();

//set a model count
model_count = 0;

//loop through the file and find the model ones to get the model lsit
for (a = 0; a < file_list.length; a++) {
	
	//get the index of model
	index_of_model = indexOf(file_list[a], "classifier.model");
	
	//if the model is in the string
	if (index_of_model > -1) {
	
		//add it tot he model list 
		model_list[model_count] = file_list[a];
		
		//add one to the count
		model_count += 1;

	}

}

//looop through the model list
for (z = 0; z < model_list.length; z++) {
	
	//close all images
	close("*");
	
	//get the image name
	current_image_name = replace(model_list[z], "_green_classifier.model", ".tif");
	
	//get the green image name
	green_image_name = replace(model_list[z], "_green_classifier.model", "_green.tif");
	
	//get the red image name
	red_image_name = replace(model_list[z], "_green_classifier.model", "_red.tif");
	
	//get the base name of the mask
	composite_mask_name = replace(model_list[z], "_green_classifier.model", "_mask_composite.tif");
	
	//get the name of the normal mask
	mask_name = replace(model_list[z], "_green_classifier.model", "_mask.tif");
		
	//find out if the composite image exists
	composite_exists_flag = File.exists(main_dir + composite_mask_name);
	
	//if the file doesn't exist
	if (composite_exists_flag == false) {
		
		//open the current image
		open(main_dir + green_image_name);
		
		//exit and display
		setBatchMode("exit and display");
		
		//run trainable weka segmentation
		run("Trainable Weka Segmentation");
		
		//wait for a bit
		wait(100);
		
		//load the classifier
		call("trainableSegmentation.Weka_Segmentation.loadClassifier", main_dir + model_list[z]);
		
		wait(100);
		
		//get the image title
		weka_title = getTitle();
		
		//get the result
		call("trainableSegmentation.Weka_Segmentation.getResult");
		
		//wait
		wait(100);
		
		//get the composite title
		composite_title = getTitle();
		
		//set the scales
		run("Set Scale...", "distance=23.4752 known=1 unit=micron");
		
		//select the weka image
		selectWindow(weka_title);
		
		//close the weka window	
		close();
		
		//select the composite mask
		selectImage(composite_title);
		
		//save it as the composite mask name
		save(main_dir + composite_mask_name);
		
		//close all images
		close("*");
		
	}
	
	//now open the mask 
	open(main_dir + composite_mask_name);
		
	//now rename it to the title
	rename("Classified image");
	
	//set the batch mode to true
	setBatchMode(true);
	
	//hide the image
	setBatchMode("hide");
	
	//make the image rgb
	run("RGB Color");
	
	//split the channels
	run("Split Channels");
	
	//select the red image and close it
	selectWindow("Classified image (red)");
	close();
	
	//select the blue iamge and close it
	selectWindow("Classified image (blue)");
	close();
	
	//select the green image
	selectWindow("Classified image (green)");
	
	//rename to mask
	rename("mask");
	
	//duplicate the image
	run("Duplicate...", "duplicate");
	
	//invert the image
	run("Invert", "stack");
	
	//select the mask
	selectWindow("mask");
	
	//set its values to 1
	run("Divide...", "value=255 stack");
	
	//set it to 32-bit
	run("32-bit");
	
	//enhance the contrast
	run("Enhance Contrast", "saturated=0.35");
	
	//save the image
	save(main_dir + mask_name);
	
	//get the image id
	final_mask_id = getImageID();
	
	final_mask_title = getTitle();
	
	//select the mask duplicate
	selectWindow("mask-1");
	
	//make it 1
	run("Divide...", "value=255 stack");
	
	//set to 32 bit
	run("32-bit");
	
	//enhance the contrast
	run("Enhance Contrast", "saturated=0.35");
	
	//get the image id
	final_mask_inverted_id = getImageID();
	
	//get the title of the inverted mask
	final_mask_inverted_title = getTitle();
	
	//get the number of channels
	number_of_channels = channels_array.length;
	
	//create a new array with the combined background substracted names
	background_substracted_names_array = newArray(number_of_channels);
	
	//loop through the number of channels
	for (a = 0; a < channels_array.length; a++) {
		
		//get the channel_file
		current_channel_file = replace(model_list[z], "_green_classifier.model", "_"+channels_array[a]+".tif");
		
		//get the segmented file name
		segmented_file_name = replace(current_channel_file, "_" + channels_array[a]+".tif", "_" + channels_array[a] + "_segmented.tif");
		
		//open the current channem image
		open(main_dir + current_channel_file);
	
		//get the current channel image id
		current_channel_image_id = getImageID();
		
		//get the current channel title
		current_channel_window_title = getTitle();
		
		//get the image calculator of the mask and channel
		imageCalculator("Multiply create stack", current_channel_window_title, final_mask_title);
		
		//get the calcualted image id
		segmented_id = getImageID();
		
		//save the segmented image
		save(main_dir + segmented_file_name);
		
		//get the segmented title
		segmented_title = getTitle();
		
		//get the background name
		background_file_name = replace(current_channel_file, "_" + channels_array[a]+".tif", "_" + channels_array[a] + "_background.tif");
		
		//if the special backgrounds array is false
		if (special_backgrounds_array[a] == false) {
			
			//get the image calculator for the background 
			imageCalculator("Multiply create stack", current_channel_window_title, final_mask_inverted_title);
			
			//get the background id
			background_id = getImageID();

		}
		
		//find out if the channel is red
		if (special_backgrounds_array[a] == true) {
			
			//select the segmented id
			selectImage(segmented_id);
			
			//duplicate the segmented image
			run("Duplicate...", "duplicate");
			
			//set this as the background id
			background_id = getImageID();
			
			//show the image
			setBatchMode("show");
			
			//find out if the current image is prebleach
			index_of_prebleach = indexOf(current_image_name, "_prebleach");
			
			//set the opening background image
			opening_raw_image = current_image_name;
			
			//if the current image of prebleach is more than -1
			if (index_of_prebleach > -1) {
				
				//get the opening background image
				opening_raw_image = replace(current_image_name, "_prebleach", "_t0min");

			}
			
			//open the opening background image
			open(main_dir + opening_raw_image);
			
			//get the opening raw image id
			raw_image_id = getImageID();
			
			//exit the batch mode
			setBatchMode("exit and display");
			
			//select the background id
			selectImage(background_id);
			
			//wait for user
			waitForUser("Delete the photo-converted nuclei from the background image.");
			
			//select the raw image
			selectImage(raw_image_id);
			
			close();
			
			//select the background id
			selectImage(background_id);
			
			//set the batchmode to true
			setBatchMode(true);
			
			//get the list of the image titles
			image_titles_list = getList("image.titles");
			
			//loop through the image titles list
			for (image_title_counter = 0; image_title_counter < image_titles_list.length; image_title_counter++) {
				
				//select the image title
				selectWindow(image_titles_list[image_title_counter]);
				
				//hide
				setBatchMode("hide");

			}

			
		}
		
		//select the background id
		selectImage(background_id);
		
		//get the 0s to nans
		setThreshold(0.00000001, 1000000);
		
		//set the stack to nan
		run("NaN Background", "stack");
		
		//set the scale
		run("Set Scale...", "distance=23.4752 known=1 unit=micron");
		
		//save the file
		save(main_dir + background_file_name);
		
		//select the segmented image id
		selectImage(segmented_id);
		
		//get the dimensions
		getDimensions(seg_width, seg_height, seg_channels, seg_slices, seg_frames);
		
		//loop throught he slices
		for (b = 0; b < seg_slices; b++) {
			
			//select the background image
			selectImage(background_id);
			
			//set the stackslice
			Stack.setSlice(b+1);
			
			//get the average of the slice
			getRawStatistics(slice_nPixels, slice_mean, slice_min, slice_max, slice_std, slice_histogram);
			
			//set the slice for the segmented
			selectImage(segmented_id);
			
			Stack.setSlice(b+1);
												
			//loop through the segmented width
			for (c = 0; c < seg_width; c++) {
				
				//loop through the segmented height
				for (d = 0; d < seg_height; d++) {
					
					//select the segmented id
					selectImage(segmented_id);
					
					//get the pixel value
					current_pixel_value = getPixel(c, d);
					
					//substract the slice_mean
					background_subs_pixel_value = ((current_pixel_value)-(slice_mean));
					
					//if the resulting value is less than 0
					if (background_subs_pixel_value < 0) {

						//set it to 0
						background_subs_pixel_value = 0;
						
					}
					
					//select the segmented image
					selectImage(segmented_id);
					
					//set the segmented image pixel to this substracted value
					setPixel(c, d, background_subs_pixel_value);				
					
				}
	
			}

		}
		
		//select the segmented_id
		selectImage(segmented_id);
		
		//get the segmented_background_substracted file name
		channel_backgroud_substracted_file_name = replace(current_channel_file, "_" + channels_array[a]+".tif", "_" + channels_array[a] + "_segmented_background_substracted.tif");
		
		//save it as segmented background substracted
		save(main_dir + channel_backgroud_substracted_file_name);
		
		//add the segmented backround substracted to the array
		background_substracted_names_array[a] = channel_backgroud_substracted_file_name;
		
		//select the segmented id
		selectImage(segmented_id);
		close();
		
		//select the current channel id
		selectImage(current_channel_image_id);
		close();
		
		//select background id
		selectImage(background_id);
		close();
	
	}
	
	//close all images
	close("*");
	
	//get the background substracted file name
	background_substracted_file_name = replace(model_list[z], "_green_classifier.model", "_background_substracted.tif");
	
	//get the length of the length of the background_substracted_names_array
	number_of_files_for_compose = background_substracted_names_array.length;
		
	//get a new array with the images ids
	images_ids = newArray(number_of_channels);
	
	//loop through the file list
	for (a = 0; a < number_of_files_for_compose; a++) {
	
		//open the file
		open(main_dir + background_substracted_names_array[a]);
		
		//get the id
		adding_id = getImageID();
		
		//add it to the images id
		images_ids[a] = adding_id;

	}
	
	//select the first image id
	selectImage(images_ids[0]);
	
	//get the dimensions
	getDimensions(comb_width, comb_height, comb_channels, comb_slices, comb_frames);
	
	//loop through the slices
	for (a = 0; a < comb_slices; a++) {
		
		//get the command for the concat
		concat_command = "";
		
		//loop through the images
		for (b = 0; b < images_ids.length; b++) {

			//select the image
			selectImage(images_ids[b]);
			
			//set the stack to the current slice
			Stack.setSlice(a+1);
			
			//get the image
			run("Duplicate...", "title=got_"+b);
			
			//update the concat command
			concat_command = concat_command + "image"+(b+1)+"=got_"+b+" ";
			
			//if it is not the last image
			if (b == ((images_ids.length)-(1))) {
				
				concat_command = concat_command + "image"+(b+2)+"=[-- None --]";

			}

		}
		
		//run the concat
		print(concat_command);
		
		//run the concat
		run("Concatenate...", "  title=merging " + concat_command);
		
		//if it is the first
		if (a == 0) {

			//set the title to merged
			rename("merged");
			
		}
		
		//if it is more than 0
		if (a > 0) {
			
			//concatenate the images once more
			run("Concatenate...", "  title=merged image1=merged image2=merging image3=[-- None --]");
		
		
		}
		


	}
	
	//get the merged_id
	merged_id = getImageID();
	
	//make it composite
	run("Stack to Hyperstack...", "order=xyczt(default) channels="+images_ids.length+" slices="+comb_slices+" frames=1 display=Grayscale");
	
	//get the complete background substracted name
	complete_background_substracted_name = replace(model_list[z], "_green_classifier.model", "_background_substracted.tif");
	
	//save it
	save(main_dir + complete_background_substracted_name);
	
	//close all images
	close("*");
	
	//exith the batch moce
	setBatchMode("exit and display");
	
	//open the complete again
	open(main_dir + complete_background_substracted_name);
	
	//get the image id
	complete_id = getImageID();
	
	//get the background substracted no ext
	complete_background_substracted_name_no_ext = File.getNameWithoutExtension(complete_background_substracted_name);
	
	//open the current image
	open(main_dir + current_image_name);
	
	//get the image id
	current_id = getImageID();
	
	//get the current image name no ext
	current_image_name_no_ext = File.getNameWithoutExtension(current_image_name);
	
	//reset the roi manager
	roiManager("reset");
	
	//get the sbs file name
	rois_file_name = replace(model_list[z], "_green_classifier.model", "_sbs_rois.zip");
	
	//if it is a prebleach
	index_of_prebleach_in_raw = indexOf(current_image_name, "prebleach");
	
	//if it is more than 0
	if (index_of_prebleach_in_raw > -1) {
		
		//get the t0min file name
		t0_filename = replace(current_image_name, "prebleach", "t0min");
		
		//print the opening
		print(main_dir + t0_filename);
		
		//open the image
		open(main_dir + t0_filename);
		
		//get the image id
		t0_id = getImageID();
		
	}
	
	//select the substracted
	selectImage(complete_id);
	
	//set the stack to 1
	Stack.setSlice(1);
	Stack.setChannel(1);
	
	//Asking to add the points until you're done
	Dialog.createNonBlocking("Select the photoconverted nuclei");
	Dialog.addMessage("Use the multiple points tool to designate photo-converted nuclei \n Try to do it in the center of the nucleus. \nIf this is a prebleach image, load the rois from the image t0min to know where are the nuclei.");
	Dialog.show();
	
	//add it to the roi manager
	roiManager("add");
	
	//if it is more than 0
	if (index_of_prebleach_in_raw > -1) {
		
		//select the image 
		selectImage(t0_id);
		close();
		
	}
	
	//check that there's only one roi
	roi_count = roiManager("count");
	
	//if it is on
	if (roi_count == 1) {
		
		//deselect
		roiManager("deselect");
		
		//roiManager select the first roi
		roiManager("select", 0);
		
		//rename it
		roiManager("rename", "sbs_coordinates");
		
		//get the coordinates
		Roi.getCoordinates(xpoints, ypoints);
		
		//now loop through the number of x poitns
		for (a = 0; a < xpoints.length; a++) {
	
			//set up the square
			makeRectangle(((xpoints[a])-(75)), ((ypoints[a])-(75)), 150, 150);
			
			//ask the user if this is ok
			waitForUser("Check the square");
			
			//add the selection to the roi manager
			roiManager("add");
			
			//select the roi
			roiManager("select", ((a+1)));
			
			//rename to the corresponding sbs
			roiManager("rename", "sbs"+(a+1)+"_square");
	
		};
		
		//loop through the sbs squares
		for (i = 0; i < xpoints.length; i++) {
	
			//select the main image
			selectImage(complete_id);
			
			//select none
			run("Select None");
			
			//select the square 1
			roiManager("select", ((i+1)));
			
			//duplicate it
			run("Duplicate...", "duplicate");
			
			//get the image id
			current_sbs_id = getImageID();
			
			//get the name for this sbs
			sbs_name = complete_background_substracted_name_no_ext + "_sbs" + (i+1) + ".tif";
			
			//save the sbs
			save(main_dir + sbs_name);
			
			//select the other main image
			selectImage(current_id);
			
			//select none
			run("Select None");
			
			//select the square 1
			roiManager("select", ((i+1)));
			
			//duplicate it
			run("Duplicate...", "duplicate");
			
			//get the image id
			current_sbs_id = getImageID();
			
			//get the name for this sbs
			sbs_name = current_image_name_no_ext + "_sbs" + (i+1) + ".tif";
			
			//save the sbs
			save(main_dir + sbs_name);
			
	
		};
		
	
	};
	
	//save the roi manager
	roiManager("deselect");
	
	//save
	roiManager("save", main_dir + rois_file_name);
	
	//close all images
	close("*");
	
	roiManager("reset");
	
}


print("Script is finished");


