#region ################################# DESCRIPTION ########################################

"""
This script normalizes the straightened sum projection of chromosomes by channel. 

The script takes the directory where it is running from and looks for files that end with _str.tif.
It then looks for the corresponding _str_sum_proj.tif file and normalizes the sum projection by channel.
This means that in order to run the script, you first need to run the straigthen_traced_chromosomes.ijm script
Also, you need to have the sum projection of the straightened chromosomes. You can do this manually or
have the images generated as a by-product of running the c012_get_straightened_chromosomes_co_position.ijm script.

It will produce a new file with the same name as the original file but with _normalized_sum_proj.tif at the end.
"""


#endregion ################################# DESCRIPTION #####################################








import roifile
import tifffile
import numpy as np
import sys
import os

#the name = main
if __name__ == "__main__":

    #get the main directory
    saving_directory = os.getcwd()

    #if it doesn't end with /
    if not saving_directory.endswith("/"):
        #add the /
        saving_directory += "/"

    #get the file list in the directory for the files that are _cut_str.tif
    working_file_list = [file for file in os.listdir(saving_directory) if file.endswith("_str.tif")]

    #if there are no files
    if len(working_file_list) == 0:
        #print that there are no files
        print("No files to align by crossover. Make sure your files end with _str.tif")
        #exit the program
        sys.exit(0)

    #loop through the files
    for file in working_file_list:

        #print the file you're working with
        print(f"Working with file: {file}")

        #get the sum_proj.tif file name
        sum_proj_file_name = file.replace("_str.tif", "_str_sum_proj.tif")

        #get the sum_proj.tif file
        sum_proj_image = tifffile.imread(sum_proj_file_name)

        #get the shape of the sum_proj_image
        current_image_shape = sum_proj_image.shape

        #get the expected shape
        expected_image_shape = (1, 1, current_image_shape[0], current_image_shape[1], current_image_shape[2])

        #set a list for the adding indexes
        adding_indexes = []

        #loop for the first three dimensions of the expected image shape
        for dimension_index, dimension in enumerate(expected_image_shape[:3]):

            #if the dimension is 1
            if dimension == 1:

                #add the dimension index to the adding indexes
                adding_indexes.append(dimension_index)

        #make the adding indexes a tuple
        adding_indexes = tuple(adding_indexes)

        #print the current image shape
        print(f"Current image shape: {current_image_shape}")

        #print the expected image shape
        print(f"Expected image shape: {expected_image_shape}")

        #print the adding indexes
        print(f"Adding indexes: {adding_indexes}")

        #if the adding indexes is not empty
        if adding_indexes:

            #print the new shape
            print("expanding dimensions..")

            #add the dimensions
            sum_proj_image = np.expand_dims(sum_proj_image, axis=adding_indexes)

            #print the new shape
            print(f"New shape: {sum_proj_image.shape}")

        #get the number of channels
        number_of_channels = sum_proj_image.shape[2]

        #get the normalized image as a copy of the sum_proj_image
        normalized_image = sum_proj_image.copy()

        #loop through the channels
        for channel in range(number_of_channels):

            #get the current channel to a new array
            current_channel = sum_proj_image[:, :, channel, :, :].copy()

            #add the dimension
            current_channel = np.expand_dims(current_channel, axis=2)

            #get the total intensity
            total_intensity = np.sum(current_channel)

            #print it
            print(f"Total intensity for channel {channel}: {total_intensity}")

            #get the number of pixels
            number_of_pixels = current_channel.shape[3] * current_channel.shape[4]

            #print the number of pixels
            print(f"Number of pixels for channel {channel}: {number_of_pixels}")

            #get the average intensity
            average_intensity = total_intensity / number_of_pixels

            #print it
            print(f"Average intensity for channel {channel}: {average_intensity}")

            #normalize the channel
            current_channel = current_channel / average_intensity

            #set the normalized image to the normalized file name
            normalized_image[:, :, channel, :, :] = current_channel

        #get the normalized file name
        normalized_file_name = file.replace("_str.tif", "_str_normalized_sum_proj.tif")

        #save the normalized image
        tifffile.imwrite(normalized_file_name, normalized_image, imagej=True, metadata={"axes": "TZCYX"})

        #print that you're done
        print(f'Done normalizing file: {file}!')

    #print that you're done
    print("Done normalizing images!")