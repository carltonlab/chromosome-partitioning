#region ####################################################### IMPORTS ##########################################################

import roifile
import tifffile
import numpy as np
import sys
import os

#endregion #################################################### IMPORTS ##########################################################

#region ####################################################### FUNCTIONS ########################################################

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

    #get the saving dictionary
    saving_dictionary = {}

    #set the max short arm length
    max_short_arm_length = 0

    #set the max long arm length
    max_long_arm_length = 0

    #loop through the files
    for file in working_file_list:

        #print the file you're working with
        print(f"Working with file: {file}")

        #add the file to the dictionary with an empty object as the value
        saving_dictionary[file] = {}

        #get the index of the last . in the file name
        last_dot_index = file.rfind(".")

        #get the file name without the extension
        file_name_no_ext = file[:last_dot_index]

        #get the rois file name
        rois_file_name = file_name_no_ext + "_rois.zip"

        #open the rois file
        rois_file = roifile.roiread(rois_file_name)

        #get the co position
        co_position = rois_file[0].subpixel_coordinates[0]

        #get the co position as integers
        co_position = (int(co_position[0]), int(co_position[1]))

        #add the co position to the dictionary
        saving_dictionary[file]["co_position"] = co_position

        #get the sum projected image file name
        sum_projected_file_name = file_name_no_ext + "_normalized_sum_proj.tif"

        #open the image with tifffile
        tifffile_image = tifffile.imread(sum_projected_file_name)

        #get the image shape
        current_image_shape = tifffile_image.shape

        #get the metadata
        metadata = tifffile.TiffFile(saving_directory + sum_projected_file_name).imagej_metadata

        #set the number of frames
        number_of_frames = 1

        #set the number of slices
        number_of_slices = 1

        #set the channels and slices to 1
        number_of_channels = 1

        #if there's frames in the metadata
        if "frames" in metadata:

            #get the number of frames
            number_of_frames = metadata["frames"]

        #if there's slices in the metadata
        if "slices" in metadata:

            #get the number of slices
            number_of_slices = metadata["slices"]
        
        #if there's channels in the metadata
        if "channels" in metadata:

            #get the number of channels
            number_of_channels = metadata["channels"]

        #get the two last dimensions of the image shape
        last_dimensions = current_image_shape[-2:]

        #get the expected image shape
        expected_image_shape = (number_of_frames, number_of_slices, number_of_channels, last_dimensions[0], last_dimensions[1])

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
            tifffile_image = np.expand_dims(tifffile_image, axis=adding_indexes)

            #print the new shape
            print(f"New shape: {tifffile_image.shape}")

        #make the summed y
        summed_y = np.sum(tifffile_image, axis=3)

        #expand the dimensions
        summed_y = np.expand_dims(summed_y, axis=3)

        #print the summed y shape
        print(f"Summed y shape: {summed_y.shape}")

        #get the halfway point
        mid_point = tifffile_image.shape[4] / 2

        #print the mid_point
        print(f"Mid point: {mid_point}")

        #get the short arm length
        if co_position[0] < mid_point:

            #get the short arm length
            short_arm_length = co_position[0]

            #long arm length
            long_arm_length = tifffile_image.shape[4] - co_position[0]

        #if the co position is greater than the mid point
        else:

            #get the short arm length
            short_arm_length = tifffile_image.shape[4] - co_position[0]

            #long arm length
            long_arm_length = co_position[0]

            #reverse the summed y
            summed_y = np.flip(summed_y, axis=4)

        #if the short arm length is greater than the max short arm length
        if short_arm_length > max_short_arm_length:

            #set the max short arm length
            max_short_arm_length = short_arm_length

        #set the short arm length
        saving_dictionary[file]["short_arm_length"] = short_arm_length

        #if the long arm length is greater than the max long arm length
        if long_arm_length > max_long_arm_length:

            #set the max long arm length
            max_long_arm_length = long_arm_length

        #get the short to long arm ratio
        short_to_long_arm_ratio = short_arm_length / long_arm_length

        #set the short to long arm ratio
        saving_dictionary[file]["short_to_long_arm_ratio"] = short_to_long_arm_ratio

        #set the long arm length
        saving_dictionary[file]["long_arm_length"] = long_arm_length

        #set the summed y
        saving_dictionary[file]["summed_y_image"] = summed_y

    #get a list of the keys
    keys = list(saving_dictionary.keys())

    #get a copy of the keys
    keys_copy = keys.copy()

    #get a list of the ratios
    ratios = [saving_dictionary[key]["short_to_long_arm_ratio"] for key in keys]

    #get the short arm lengths
    short_arm_lengths = [saving_dictionary[key]["short_arm_length"] for key in keys]

    #sort the ratios and keys by the ratios
    ratios, keys = zip(*sorted(zip(ratios, keys)))

    #sort the keys_copy and short_arm_lengths by the short arm lengths
    short_arm_lengths, keys_copy = zip(*sorted(zip(short_arm_lengths, keys_copy)))

    #make a copy of the saving dictionary
    saving_dictionary_copy = saving_dictionary.copy()

    #start a sorted directory
    sorted_dictionary = {}

    #make a sorted_by_short_arm_length directory
    sorted_by_short_arm_length = {}

    #loop through the keys
    for index, key in enumerate(keys):

        #get the sorted dictionary
        sorted_dictionary[key] = saving_dictionary[key].copy()

    #loop through the keys_copy
    for index, key in enumerate(keys_copy):

        #get the sorted by short arm length
        sorted_by_short_arm_length[key] = saving_dictionary_copy[key].copy()

    #get a counter
    counter = 0

    #loop through the dictionary
    for file in sorted_dictionary:

        #get the short arm length
        short_arm_length = sorted_dictionary[file]["short_arm_length"]

        #get the long arm length
        long_arm_length = sorted_dictionary[file]["long_arm_length"]

        #get the summed y image
        summed_y_image = sorted_dictionary[file]["summed_y_image"]

        #if the short arm length is not the max short arm length
        if short_arm_length != max_short_arm_length:

            #get the difference
            difference = max_short_arm_length - short_arm_length

            #get the padding
            padding = ((0, 0), (0, 0), (0, 0), (0, 0), (difference, 0))

            #pad the summed y image
            summed_y_image = np.pad(summed_y_image, padding)

        #if the long arm length is not the max long arm length
        if long_arm_length != max_long_arm_length:

            #get the difference
            difference = max_long_arm_length - long_arm_length

            #get the padding
            padding = ((0, 0), (0, 0), (0, 0), (0, 0), (0, difference))

            #pad the summed y image
            summed_y_image = np.pad(summed_y_image, padding)

        #set the summed y image
        sorted_dictionary[file]["summed_y_image"] = summed_y_image

        #if the counter is 0
        if counter == 0:

            #set the final summed y image
            final_summed_y_image = summed_y_image
        
        #if it is not 0
        else:

            #concatenate the summed y image to the final summed y image in axis 3
            final_summed_y_image = np.concatenate((final_summed_y_image, summed_y_image), axis=3)

        #add to the counter
        counter += 1

    #get the number of files in the sorted dictionary
    number_of_files = len(sorted_dictionary)

    #get the final summed y image shape
    final_summed_y_image_shape = final_summed_y_image.shape

    #get the final summed y file name
    final_image_file_name = "c012_normalized_sum_proj_aligned_by_crossover_y_summed.tif"

    #save the final summed y image
    tifffile.imwrite(saving_directory + final_image_file_name, final_summed_y_image, imagej=True, metadata={'axes': 'TZCYX'})

    #print the final summed y image shape
    print(f"Final summed y image shape: {final_summed_y_image_shape}")

    #get a copy counter
    copy_counter = 0

    #get a new max_length
    max_length = 0

    #loop through the sorted by short arm length dictionary
    for file in sorted_by_short_arm_length:

        #get the short arm
        short_arm_length = sorted_by_short_arm_length[file]["short_arm_length"]

        #get the long arm
        long_arm_length = sorted_by_short_arm_length[file]["long_arm_length"]

        #get the total
        total = short_arm_length + long_arm_length

        #if the total is greater than the max length
        if total > max_length:

            #set the max length
            max_length = total

    #make a new file for the sorted names
    sorted_names_files = 'aaa_sorted_names.txt'

    #open the file
    with open(saving_directory + sorted_names_files, 'w') as sorted_writing_file:

        #loop through the sorted by short arm length dictionary
        for indexis, file in enumerate(sorted_by_short_arm_length):

            #write the file name
            sorted_writing_file.write(f"{indexis}: {file}\n")

    #loop through the sorted by short arm length dictionary
    for file in sorted_by_short_arm_length:

        #print a space
        print("")

        #print the file you're working with
        print(f"Working with file: {file}")

        #get the short arm length
        short_arm_length = sorted_by_short_arm_length[file]["short_arm_length"]

        #get the long arm length
        long_arm_length = sorted_by_short_arm_length[file]["long_arm_length"]

        #get the summed y image
        summed_y_image = sorted_by_short_arm_length[file]["summed_y_image"]

        #get the total chromosome length
        total_chromosome_length = short_arm_length + long_arm_length

        #print the short arm length and the long arm length
        print(f"Short arm length: {short_arm_length}, Long arm length: {long_arm_length}")

        #print the max lenght and the total chromosome length
        print(f"Max length: {max_length}, Total chromosome length: {total_chromosome_length}")

        #if the total chromosome length is not eh max length
        if total_chromosome_length < max_length:

            #get the difference
            difference = max_length - total_chromosome_length

            #print the difference
            print(f"Difference: {difference}")

            #get the padding
            padding = ((0, 0), (0, 0), (0, 0), (0, 0), (0, difference))

            #pad the summed y image
            summed_y_image = np.pad(summed_y_image, padding)

            #print the new summed y image shape
            print(f"New summed y image shape: {summed_y_image.shape}")

        #set the summed y image
        sorted_by_short_arm_length[file]["summed_y_image"] = summed_y_image

        #if the copy counter is 0
        if copy_counter == 0:

            #set the final summed y image
            left_aligned_summed_image = summed_y_image

        #if it is not 0
        else:

            #concatenate the summed y image to the final summed y image in axis 3
            left_aligned_summed_image = np.concatenate((left_aligned_summed_image, summed_y_image), axis=3)

        #add to the copy counter
        copy_counter += 1

    #get the left aligned summed image shape
    left_aligned_summed_image_shape = left_aligned_summed_image.shape

    #get the left aligned summed image file name
    left_aligned_summed_image_file_name = "c012_normalized_sum_proj_sorted_by_short_arm_length_y_summed_left_aligned.tif"

    #save the left aligned summed image
    tifffile.imwrite(saving_directory + left_aligned_summed_image_file_name, left_aligned_summed_image, imagej=True, metadata={'axes': 'TZCYX'})

    #print a space
    print("")

    #get the total image count
    total_image_count = len(working_file_list)

    #print the total image count
    print(f"Total image count: {total_image_count}")

    #print that the left aligned image has been saved
    print(f"Left aligned summed image shape: {left_aligned_summed_image_shape}")





#endregion #################################################### FUNCTIONS ########################################################