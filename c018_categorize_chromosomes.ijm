/* 

This script will open the "_str_sum_proj.tif" files from the megasomes and will allow the user
to classify the files according to the "c018_chromosome_types_2022_2_7.png" file that is opened.
For the image to open, you need to have it in the same directory where your "_str_sum_proj.tif" files are located.

The results are saved as a .csv file with the termination: "_str_sum_proj_category.csv"



For it to work you need to have already straightened the megasomes and made sum projections from them using the
script: "c018_megasomes_make_sum_projection.ijm".

*/


//set the expandable arrays
setOption("ExpandableArrays", true);

//close all images
close("*");

//get the main directory that contains the meT7 chromosomes to be categorized.
main_dir = getDir("Select the directory with the iamges");

//get the chromosome types image
types_file_path = main_dir + "c018_chromosome_types_2022_2_7.png";

//get the directory file list to be sorted later
file_list = getFileList(main_dir);

//open the image to know what the categories are
open(types_file_path);

//set the location of the image to the right side of the screen
setLocation((screenWidth/3)*2, screenHeight/7);

//get a new file array that will hold the working files
working_file_list = newArray();

//set a counter for the previously mentioned file list
working_counter = 0;

//loop through the file list to filter the files you actually want to open
for (a = 0; a < file_list.length; a++) {

	//get the index of str_sum_proj.tif (You can change this to whatever termination you want for your files)
	index_of_common = indexOf(file_list[a], "_str_sum_proj.tif");
	
	//if the index is more than -1 add the file to the working file list
	if (index_of_common > -1) {

		//add it to the list
		working_file_list[working_counter] = file_list[a];
		
		//add one to the counter
		working_counter += 1;

	}

//end of the file list loop a
}

//print an empty space for clarity
print("");

//print the working file list lenth
print("The working file list lenght is:" + working_file_list.length);

//clear the results for the categorization
run("Clear Results");

//loop throught the working file list to categorize the files
for (a = 0; a < working_file_list.length; a++) {
	
	//open the image
	open(main_dir + working_file_list[a]);
	
	//get the image id to close and manage the image later
	current_image_id = getImageID();
	
	//get the file name 
	file_name_string = File.getName(working_file_list[a]);
	
	//set the display to color mode
	Stack.setDisplayMode("color");
	Stack.setChannel(2);
	
	//set the channel 2 to magenta
	run("Magenta");
	
	//set the channel to 3
	Stack.setChannel(3);
	
	//make it green
	run("Green");
	
	//set it to composite
	Stack.setDisplayMode("composite");
	
	//set it to composite mode for channels 2 and 3
	Stack.setActiveChannels("011");
	
	//make a dialog for the user to select the category
	Dialog.createNonBlocking("Select the category of the current chromosome");
	
	//make the array for the category types
	category_types = newArray();
	
	//loop through 7
	for (b = 0; b < 7; b++) {

		//set the category
		category_types[b] = b+1;

	}
	
	//add a choice
	Dialog.addChoice("Category: ", category_types, category_types[1]);
	
	//show the dialog
	Dialog.show();
	
	//get the category
	category = Dialog.getChoice();
	
	//remove the last two characters
	category = substring(category, 0, category.length - 2);
	
	//close the image
	selectImage(current_image_id);
	
	//close the image
	close();
	
	//make a new table
	Table.create("saving_table");
	
	//select the table
	selectWindow("saving_table");
	
	//add the filename,category
	Table.set("filename", 0, working_file_list[a]);
	
	//add the category to the table
	Table.set("category", 0, category);
	
	//update the table
	Table.update;
	
	//get the table file name
	table_file_name = File.getNameWithoutExtension(working_file_list[a]) + "_category.csv";
	
	//save the table
	Table.save(main_dir + table_file_name);
	
	//close the table
	close("saving_table");

// end of the loop of the working file list a
}






