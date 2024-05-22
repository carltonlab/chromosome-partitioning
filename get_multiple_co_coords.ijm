/* This script is used to get multiple crossover sites from straightened chromosomes with image file names ending in _str.tif

	The resulting csv file is saved with the same file name with the termination _co_coords.csv
	
	Run in the imagej script editor.
	
*/


//print that the script is running
print("The script get_multiple_co_coords.ijm is running...";

//set the expandable arrays
setOption("ExpandableArrays", true);
	
//set a string to filter the files
filter_string = "_str.tif";	

//get the main directory
main_dir = getDir("Select the directory with the files");

//get the file list
file_list = getFileList(main_dir);
	
//start the working file list\
working_file_list = newArray();

//start the working file list counter
working_file_list_counter = 0;	

//loop through the file list
for (a = 0; a < file_list.length; a++) {
	
	//if get the index of the sum_proj.tif
	index_of_alignment = indexOf(file_list[a], filter_string);
	
	//if the index is more than -1
	if (index_of_alignment > -1) {
	
		//add the file to the working file list
		working_file_list[working_file_list_counter] = file_list[a];
		
		//add one to the counter
		working_file_list_counter += 1;
	
	}
	
}


//loop through the working file list
for (a = 0; a < working_file_list.length; a++) {


	//close all images
	close("*");

	//clear the results
	run("Clear Results");
	
	//open the image
	open(main_dir + working_file_list[a]);
	
	//wait for user to select the crossover sites
	waitForUser("Select the crossover sites with the multiple point tool");
	
	//get the x point
	Roi.getCoordinates(xpoints, ypoints);
	
	//sort
	Array.sort(xpoints, ypoints);
	
	//loop through the x coords
	for (b = 0; b < xpoints.length; b++) {
	
		//get the floor of x
		xpoint_floor = floor(xpoints[b]);

		//get the floor of y
		ypoint_floor = floor(ypoints[b]);

		//set name in results
		setResult("name", b, (b+1));
		
		//set the x position
		setResult("x", b, xpoint_floor);
		
		//set the u position
		setResult("y", b, ypoint_floor);
		
		//set the z position
		setResult("z", b, 0.0);
		
		//set the z position
		setResult("c", b, 0.0);

	}
	
	//get the co_coords.csv
	csv_file_name = File.getNameWithoutExtension(working_file_list[a]);
	csv_file_name = csv_file_name + "_co_coords.csv";
	
	//save the results
	selectWindow("Results");
	
	//save them
	saveAs("results", main_dir + csv_file_name);

}

//print that the script has ended
print("The script get_multiple_co_coords.ijm has finished.");














