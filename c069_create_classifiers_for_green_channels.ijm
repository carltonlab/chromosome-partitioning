//scritp to batch get the classifiers for a directory

/*
This will get a directory selected by the user.

After that, it'll get a file list with all the files in the directory.

Those files will be filtered to get the ones that have the the termination "_green.tif" (green channel images).

It'll then open each of the files one at a time, give you the chance to delete any autoflorescence from the worm, then open trainable weka segmentation
and ask you to set up the labels. Set the label 1 to the background (Red color) and the actual signal to the label 2
(green color). After setting the labels, it will train the classifier and save it to the correct name. It will also created
the mask with the composite image accordingly. 

It'll later proceed to work on the next file until all the green images in the directory are processed.  
 
*/

//get the script name
script_name = "c069_create_classifiers_for_green_channels.ijm";

//start the log system
current_log = log_start(script_name);

//get the directory
main_dir = getDir("Select the directory with where you want to make the classifeirs");

//log the selected directory
current_log = log_add(current_log, "The selected main directory is: "+main_dir);

//set the expandable arrays
setOption("ExpandableArrays", true);

//log obtaining the file list
current_log = log_add(current_log, "Obtaining the file list...");

//get the file list
file_list = getFileList(main_dir);

//log that the list was obtained
current_log = log_add(current_log, "All files list obtained...");

//get the green channels file list
green_file_list = newArray();

//start a greend counter
green_file_list_counter = 0;

//log that you're filtering the list
current_log = log_add(current_log, "Getting a list for the green images only...");


//loop through the file list to get the greenchannels
for (a = 0; a < file_list.length; a++) {

	//get the index of _green.tif
	index_of_green = indexOf(file_list[a], "_green.tif");
	
	//if it is there, ( > -1), add it to the green list
	if (index_of_green > -1) {
		
		//add it
		green_file_list[green_file_list_counter] = file_list[a];
		
		//log that the green image was added
		current_log = log_add(current_log, "Green image found and added to the working list: "+green_file_list[green_file_list_counter]);
		
		//add one to the counter
		green_file_list_counter += 1;
		
	}

}

//log that all green images found
current_log = log_add(current_log, "All green imaged filtered...");

//log that you will start getting the classifiers
current_log = log_add(current_log, "Starting the loop to get the green classifiers...");

//log an empty space
current_log = log_add(current_log, "");

//now, looop through the file list
for (a = 0; a < green_file_list.length; a++) {
	
	//close all images
	close("*");
	
	//log the image you're working on
	current_log = log_add(current_log, "Working on file: "+green_file_list[a]);
	
	//getting the green classifier file name
	classifier_file_name = replace(green_file_list[a], "_green.tif", "_green_classifier.model");
	
	//find out if the classifier exists
	classifier_exists_flag = File.exists(main_dir + classifier_file_name);
	
	//start a flag to work on the classifier
	work_on_classifier = true;
	
	//if the classifier exists, log it
	if (classifier_exists_flag == true) {
	
		//log that it exists
		current_log = log_add(current_log, "The classifier file: "+classifier_file_name+" already exists. Asking for next step.");
		
		//Make a dialog
		Dialog.createNonBlocking("The classifier exists...");
		
		//add the dialog elements
		Dialog.addMessage("Classifier name: "+classifier_file_name);		
		Dialog.addCheckbox("Replace classifier", false);
		
		//show the dialog
		Dialog.show();
		
		//get the dialog elements
		work_on_classifier = Dialog.getCheckbox();
		
		//if it is true
		if (work_on_classifier == true) {

			//log that the classifier will be replaced
			current_log = log_add(current_log, "The classifier will be replaced with a new one...");

		}
		
		//if it is false
		if (work_on_classifier == false) {
	
			//log that the file will be skipped
			current_log = log_add(current_log, "A new classifier won't be created. Skipping file.");
			
		}
		
	}
	
	//if working is true
	if (work_on_classifier == true) {

		//log that you started work on the classifier
		current_log = log_add(current_log, "Opening image: "+green_file_list[a]);
		
		//open the image
		open(main_dir + green_file_list[a]);
		
		//log that the image was opened
		current_log = log_add(current_log, "The image was opened...");
		
		//get the image id and title
		working_image_id = getImageID();
		working_image_window_title = getTitle();
		
		//enhance the contrast
		run("Enhance Contrast", "saturated=0.35");
		
		//log that you're asking the user to delete any autofluorescence regions if there are any.
		current_log = log_add(current_log, "Asking user to set autofluorescence regions to 0s if there's any... ");
		
		//Start a dialog to ask the user to save the autofluorescence if there's any
		Dialog.createNonBlocking("Set autofluorescence regions to 0 if there's any.");
		
		//add the dialog elements
		Dialog.addCheckbox("Autofluorescence region deleted", false);
		
		//show the dialog
		Dialog.show();
		
		//get flag to know if the image has autofluorescence regions
		auto_region_flag = Dialog.getCheckbox();
		
		//if the flag is true
		if (auto_region_flag == true) {

			//log that auto fluorescence was detected and set to 0 by the user
			current_log = log_add(current_log, "Autofluorescence deleted by user.");
			
			//log that you will save the image now
			current_log = log_add(current_log, "Saving image without autofluorescence...");
			
			//log that you're saving the image
			selectImage(working_image_id);
			
			//save the image
			save(main_dir + green_file_list[a]);
			
			//log that the image was saved
			current_log = log_add(current_log, "Image was saved...");

		}
		
		if (auto_region_flag == false) {
			
			//log that there was no autofluorescence
			current_log = log_add(current_log, "No autofluorescence deleted by user.");
			
		}
		
		//log that the weka segmentation will start
		current_log = log_add(current_log, "Starting weka segmentation");
		
		//select the image
		selectImage(working_image_id);
		
		//start the weka segmentation
		run("Trainable Weka Segmentation");
		
		//wait for 100 ms
		wait(100);
		
		//get a flat to know if the image was done
		trainer_done_flag = false;
		
		//log that the labels are being set
		current_log = log_add(current_log, "Getting weka segmentation labels");
		
		//wait for user to set the labels
		waitForUser("Set the weka segmentation labels.\nDon't train the classifier or save it. Just click OK after label designation.");
		
		//set a while loop that ends when the classifier is done
		while (trainer_done_flag == false) {

			//log that the labels were set and the classifier will be trained
			current_log = log_add(current_log, "Labels set, training classifier now...");
			
			//call for the training
			call("trainableSegmentation.Weka_Segmentation.trainClassifier");
			
			//wait for 100 ms
			wait(100);
			
			//log that the classifer is finished
			current_log = log_add(current_log, "Training finished for this labels.");
			
			//log that you're verifying the result
			current_log = log_add(current_log, "User result verification underway...");
			
			//find out from user if the labels are correct
			//make a dialog for that
			Dialog.createNonBlocking("Verify the result");
			
			//add the element
			Dialog.addCheckbox("Result correct", true);
			
			//show the dialog
			Dialog.show();
			
			//get the flag
			trainer_done_flag = Dialog.getCheckbox();
			
			//if it is true
			if (trainer_done_flag == true) {
				
				//log that the result was verified.
				current_log = log_add(current_log, "Result correct.");
				
			}
			
			//if it is false, start the labels again
			if (trainer_done_flag == false) {
				
				//log that the result need tuning. 
				current_log = log_add(current_log, "Result needs tuning. Getting the new labels...");
				
				//wait for user to set the labels
				waitForUser("Set the weka segmentation labels.\nDon't train the classifier or save it. Just click OK after label designation.");

			}
			
		}
		
		//log that you'll save the classifier now
		current_log = log_add(current_log, "Saving the classifier...");
		
		//save the classifier
		call("trainableSegmentation.Weka_Segmentation.saveClassifier", main_dir + classifier_file_name);	
		
		//wait for 100 ms
		wait(100);
		
		//log that it was saved
		current_log = log_add(current_log, "Classifier saved...");	
		
		//get the mask name
		composite_mask_name = replace(green_file_list[a], "_green.tif", "_mask_composite.tif");
		
		//log that the composite image will be created
		current_log = log_add(current_log, "Creating composite mask...");	
		
		//creating the result
		call("trainableSegmentation.Weka_Segmentation.getResult");
		
		//wait 100 ms
		wait(100);
		
		//log that the mask was created
		current_log = log_add(current_log, "Mask created...");	
		
		//select the classified image
		selectWindow("Classified image");
		
		//set the scales
		run("Set Scale...", "distance=23.4752 known=1 unit=micron");
		
		//log that the classified image will be saved
		current_log = log_add(current_log, "Saving the mask...");	
		
		//save the mask after selecting 
		save(main_dir + composite_mask_name);
		
		//log that the mask was saved
		current_log = log_add(current_log, "Mask saved...");	

	}
	
	//log that the file is done and you're closing all images
	current_log = log_add(current_log, "File done, closing all images...");		
	
	//close all images
	close("*");
	
	//log an empty space
	current_log = log_add(current_log, "");		
	
}

//log that all files have been processed.
current_log = log_add(current_log, "All files processed.");

//end the log
end_log (current_log, script_name, main_dir)	










/////////////////////////////////// Methods ////////////////////////////////////////////

function log_start (script_name) {
	
	//get the current time
	time = time_log();
	
	//start the logging
	print( time + "Starting script: "+script_name);
	
	//add the new log
	new_log = time + "Starting script: "+script_name + "\n";
	
	//get the date and time
	getDateAndTime(year, month, dayOfWeek, dayOfMonth, hour, minute, second, msec);
	
	//get the on string
	on_string = "" + time_log() + "On: "+year+"/"+(month+1)+ "/" + dayOfMonth + " at " + hour + ":" + minute + ":" + second;
	
	//print the date and time
	print(on_string);
	
	//add to new log
	new_log = new_log + on_string + "\n";
	
	return new_log;
	
}

function log_add (current_log, logging) {
	
	//print the log
	print("" + time_log() + logging);
	
	//add the new log
	new_log = current_log + "" + time_log() + logging + "\n";
		
	return new_log;
	
}

function end_log (current_log, script_name, main_dir) {
	
	//get the script name without extension
	no_ex_script = File.getNameWithoutExtension(script_name);
	
	//get the date and time
	getDateAndTime(year, month, dayOfWeek, dayOfMonth, hour, minute, second, msec);
	
	//get the log file name
	log_file_name = no_ex_script + "_" + year + "_" + (month+1) + "_" + dayOfMonth + "_" + hour + "_" + minute + "_" + second + "_log.txt";
	
	//print that you're saving the log
	print("" + time_log() + "Saving the log: "+main_dir + log_file_name);
	
	current_log = current_log + "" + time_log() + "Saving the log: "+main_dir + log_file_name;
	
	//save the file
	File.saveString(current_log, main_dir + log_file_name);
	
	//print
	print("" + time_log() + "The script "+ script_name + " has finished running...");
	
	print("");
	
}

function time_log () {
	
	//get the date and time
	getDateAndTime(year, month, dayOfWeek, dayOfMonth, hour, minute, second, msec);
	
	//get the []
	time_string = "["+hour+":"+minute+":"+second+"] ";
	
	return time_string;
	
}





