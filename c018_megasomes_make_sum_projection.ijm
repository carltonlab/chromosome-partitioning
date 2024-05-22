/*
 * 
 * This script get the files and makes sum projections for them. Use specifically with the two-crossover megasomes as it has 
 *	some modifications to include the _str.tif, _co1.tif and the _co2.tif. 1
 *
 *	Run in imagej in the script editor
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
	index_of_co1 = indexOf(file_list[a], "_co1.tif");
	index_of_co2 = indexOf(file_list[a], "_co2.tif");
	
	//if the index is more than 0
	if (index_of_tif >= 0 || index_of_co1 >= 0 || index_of_co2 >= 0) {
	
		//set it
		working_file_list[working_counter] = file_list[a];
		
		//add one to the counter
		working_counter += 1;

	}

}

//loop throught the working file list
for (a = 0; a < working_file_list[a].length; a++) {
	
	//porint working on file
	print("Working on file: "+working_file_list[a]);
	
	//close all images
	close("*");
	
	//get the working image file name
	working_image_filename = working_file_list[a];
	
	//get the saving file name
	saving_file_name = File.getNameWithoutExtension(working_image_filename) + "_sum_proj.tif";
		
	//open the image
	open(working_image_filename);
	
	//get the image id
	working_image_id = getImageID();
	
	//select the image
	selectImage(working_image_id);
	
	//run the z projection
	run("Z Project...", "projection=[Sum Slices]");
	
	//get the projection image id
	projected_image_id = getImageID();
	
	//save the image
	selectImage(projected_image_id);
	
	//save
	save(main_dir + saving_file_name);
	
	//close all images
	close("*");
	
}

//ended
print("Script ended");



