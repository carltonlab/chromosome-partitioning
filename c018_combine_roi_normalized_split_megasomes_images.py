
#region ################################### DESCRIPTION ##########################################

"""

This script makes the combined image of the c018 megasome segments aligned by the crossover position.
The script looks for the files in the execution directory and finds the files terminating with "_sum_proj_short_long_arm_measurements.csv"

It will then get the normalized images of the chromosomes and align them by the crossover position.

For it to work you need to have measured the crossover positions in the megasomes, split the megasomes, made the
sum projections and normalized the images.

The script will then pad the images to the longest short arm and the longest long arm and make a combined image of the chromosomes aligned
by the crossover position.

The resulting file will be saved in the execution directory with the name "c018_megasome_split_chromosomes_combined_image.tif"


"""

#endregion ################################ END OF DESCRIPTION ###################################


#region ################################### IMPORTS ##############################################

import os
from matplotlib import pyplot as plt
import napari
import pandas as pd
import numpy as np
import tifffile
import roifile

#endregion ################################ END OF IMPORTS #######################################


#region ################################### GLOBALS ##############################################



#endregion ################################ END OF GLOBALS #######################################


#region ################################### FUNCTIONS ############################################



#endregion ################################ END OF FUNCTIONS #####################################


#region ################################### MAIN #################################################

#if name is main, print the script name
if __name__ == "__main__":

    #get the working directory
    working_directory = os.getcwd()

    #if the working directory does not end with a slash, add one
    if not working_directory.endswith("/"):
        working_directory += "/"

    #get the file list
    file_list = os.listdir(working_directory)

    #get the measurements.csv list
    file_list = [file for file in file_list if "_sum_proj_short_long_arm_measurements.csv" in file]

    #get the file dictionary
    file_dictionary = {}

    #variable for the longest short arm
    max_long_arm_length = 0

    #variable for the longest long arm
    max_short_arm_length = 0

    #loop through the file list
    for file_index, file_name in enumerate(file_list):

        #print a space
        print("")

        #print the file name
        print(f"Working on file: {file_name}")

        #add the working file name to the file dictionary
        file_dictionary[file_name] = {}

        #get the pandas data frame
        file_data_frame =  pd.read_csv(working_directory + file_name)

        #add the data frame
        file_dictionary[file_name]["data_frame"] = file_data_frame

        #get the pixel area
        pixel_area = (file_data_frame["short_arm_length"][0] + file_data_frame["long_arm_length"][0]) * file_data_frame["chr_height"][0]

        #add the pixel area to the file dictionary
        file_dictionary[file_name]["pixel_area"] = pixel_area

        #get the total pixel intensity
        pansyp1_total_pixel_intensity = file_data_frame["short_arm_int"][0] + file_data_frame["long_arm_int"][0]

        #get the syp1phos total pixel intensity
        syp1phos_total_pixel_intensity = file_data_frame["short_arm_int"][1] + file_data_frame["long_arm_int"][1]

        #get the syp1phos difference
        syp1phos_difference = file_data_frame["long_arm_int"][1] - file_data_frame["short_arm_int"][1]

        #get the syp1phos normalizing mean
        #if the syp1phos difference is greater than 0
        if syp1phos_difference > 0:

            #get the syp1phos normalizing mean
            syp1phos_normalizing_mean = file_data_frame["long_arm_int"][1] / (file_data_frame["long_arm_length"][0] * file_data_frame["chr_height"][0])

        #if the syp1phos difference is less than 0
        if syp1phos_difference <= 0:
        
            #get the syp1phos normalizing mean
            syp1phos_normalizing_mean = file_data_frame["short_arm_int"][1] / (file_data_frame["short_arm_length"][0] * file_data_frame["chr_height"][0])

        #add the syp1phos normalizing mean to the file dictionary
        file_dictionary[file_name]["syp1phos_normalizing_mean"] = syp1phos_normalizing_mean

        #set it in the dictionary
        file_dictionary[file_name]["total_pixel_intensity"] = {"pansyp1":pansyp1_total_pixel_intensity, "syp1phos":syp1phos_total_pixel_intensity}

        #add the chromosome mean to the file dictionary
        file_dictionary[file_name]["chromosome_mean"] = {"pansyp1":pansyp1_total_pixel_intensity / pixel_area, "syp1phos":syp1phos_total_pixel_intensity / pixel_area}

        #get the short arm ratio
        short_arm_long_arm_ratio = file_data_frame["short_arm_length"][0] / file_data_frame["long_arm_length"][0]

        #add the short arm ratio to the file dictionary
        file_dictionary[file_name]["short_arm_long_arm_ratio"] = short_arm_long_arm_ratio

        #get the rois file name
        rois_file_name = file_name.replace("_measurements.csv", "_rois.zip")

        #open the rois
        rois = roifile.roiread(working_directory + rois_file_name)

        #get the first roi coordinates
        roi_coordinates = rois[0].coordinates()

        #get the x coordinate
        co_coordinate = roi_coordinates[0][0] + 1

        #get the image file name
        image_file_name = file_name.replace("_sum_proj_short_long_arm_measurements.csv", "_roi_normalized_sum_proj.tif")

        #open the image with tifffile
        tifffile_image = tifffile.imread(working_directory + image_file_name)

        #get the image shape
        current_image_shape = tifffile_image.shape

        #get the metadata
        metadata = tifffile.TiffFile(working_directory + image_file_name).imagej_metadata

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

        #get the aproximage crossover intensity
        #get the crossover -5
        crossover_minus_5 = int(co_coordinate - 6)

        #if it is less than 0, set it to 0
        if crossover_minus_5 < 0:
            crossover_minus_5 = 0
        
        #get the crossover + 
        crossover_plus_5 = int(co_coordinate + 4)

        #if it is greater than the image length, set it to the image length
        if crossover_plus_5 > (tifffile_image.shape[-1]-1):
            crossover_plus_5 = (tifffile_image.shape[-1]-1)

        #get the number of pixels multiplied by the chromosome height
        co_pixel_area = (crossover_plus_5 - (crossover_minus_5 + 1)) * file_data_frame["chr_height"][0] 

        #get the nparray of the image at the co coordinate
        co_coordinate_image = tifffile_image[:,:,2:3,:,crossover_minus_5:crossover_plus_5+1]

        #get the sum of the co coordinate image
        co_coordinate_image = np.sum(co_coordinate_image, axis=(4,3,2,1,0))

        #set the co normalizing mean
        co_normalizing_mean = co_coordinate_image / co_pixel_area

        #set the co normalizing mean in the file dictionary
        file_dictionary[file_name]["co_normalizing_mean"] = co_normalizing_mean

        #get the image length
        image_length = tifffile_image.shape[-1]

        #get half the image length
        half_image_length = image_length / 2

        #restart the short arm to left bool
        short_arm_to_left_bool = True

        #if the co coordinate is greater than half the image length
        if co_coordinate > half_image_length:

            #set the short arm to left bool to false
            short_arm_to_left_bool = False

        #if it is true, continue
        if short_arm_to_left_bool:

            #set the short arm length to the co coordinate
            short_arm_length = co_coordinate

            #set the long arm length to the image length minus the co coordinate
            long_arm_length = image_length - co_coordinate

        #if the short arm is not to the left
        if not short_arm_to_left_bool:

            #flip the image
            tifffile_image = np.flip(tifffile_image, axis=-1)

            #set the short arm length to the image length minus the co coordinate
            short_arm_length = image_length - co_coordinate

            #set the long arm length to the co coordinate
            long_arm_length = co_coordinate

        #set the short arm length again
        file_dictionary[file_name]["short_arm_length"] = short_arm_length

        #set the long arm length again
        file_dictionary[file_name]["long_arm_length"] = long_arm_length

        #set the data
        file_dictionary[file_name]["data"] = tifffile_image

        #if the short arm length is greater than the max short arm length
        if short_arm_length > max_short_arm_length:

            #set the max short arm length to the current short arm length
            max_short_arm_length = short_arm_length

        #if the long arm length is greater than the max long arm length
        if long_arm_length > max_long_arm_length:

            #set the max long arm length to the current long arm length
            max_long_arm_length = long_arm_length

    #loop through the file dictionary to get the normalized data
    for file_index, file_name in enumerate(file_dictionary):

        #print a space
        print("")

        #print that you're getting teh sum of the data
        print(f"Getting the sum of the data for file: {file_name}")

        #get the data
        tifffile_image = file_dictionary[file_name]["data"]

        #get the length of the y axis
        y_axis_length = tifffile_image.shape[3]

        #sum the y axis
        tifffile_image = np.sum(tifffile_image, axis=3)

        #add an axis on the correct position
        tifffile_image = np.expand_dims(tifffile_image, axis=3)

        #divide the data by the chromosome height
        tifffile_image = tifffile_image / y_axis_length

        #set the normalized data to the file dictionary
        file_dictionary[file_name]["normalized_data"] = tifffile_image

    #get the list of the normalized data
    normalized_data_list = [file_dictionary[file_name]["normalized_data"] for file_name in file_dictionary]

    #get a list with the indexes of the normalized data list
    normalized_data_list_indexes = [index for index in range(len(normalized_data_list))]

    #get the ratio list
    short_arm_ratio_list = [file_dictionary[file_name]["short_arm_long_arm_ratio"] for file_name in file_dictionary]

    #get the short arm lenght list
    short_arm_length_list = [file_dictionary[file_name]["short_arm_length"] for file_name in file_dictionary]

    #get the long arm length list
    long_arm_length_list = [file_dictionary[file_name]["long_arm_length"] for file_name in file_dictionary]

    #get the file name list
    file_name_list = [file_name for file_name in file_dictionary]

    #print the short arm ratio list
    print(f"Short arm ratio list: {short_arm_ratio_list}")

    #print the short arm length list
    print(f"Short arm length list: {short_arm_length_list}")

    #print the long arm length list
    print(f"Long arm length list: {long_arm_length_list}")

    #print the file name list
    print(f"File name list: {file_name_list}")

    #print the normalized data list
    #print(f"Normalized data list: {normalized_data_list}")

    #get the length of the short arm ratio list
    short_arm_ratio_list_length = len(short_arm_ratio_list)

    #make a new background channel image and fill it with 50s
    background_channel_image = np.zeros((1,1,1,int(short_arm_ratio_list_length),int(max_long_arm_length+max_short_arm_length)))

    #set the first of the first pixel to 100
    background_channel_image[0,0,0,0,0] = 100

    #sort the lists by the short arm ratio list
    short_arm_ratio_list, normalized_data_list_indexes, short_arm_length_list, long_arm_length_list, file_name_list = zip(*sorted(zip(short_arm_ratio_list, normalized_data_list_indexes,short_arm_length_list, long_arm_length_list, file_name_list)))

    #flip all the lists
    short_arm_ratio_list = list(short_arm_ratio_list)[::-1]
    normalized_data_list_indexes = list(normalized_data_list_indexes)[::-1]
    short_arm_length_list = list(short_arm_length_list)[::-1]
    long_arm_length_list = list(long_arm_length_list)[::-1]
    file_name_list = list(file_name_list)[::-1]

    #make a new csv file to save the data
    with open(working_directory + "c018_megasome_split_chromosomes_names_and_ratios.csv", "w") as file:

        #loop through the file name list
        for file_index, file_name in enumerate(file_name_list):

            #write the file name and the short arm ratio
            file.write(f"{file_name},{short_arm_ratio_list[file_index]}\n")

    #loop through the file name list
    for file_index, file_name in enumerate(file_name_list):

        #print the current file name
        print(f"File name: {file_name}")

        #print the current short arm ratio
        print(f"Short arm ratio: {short_arm_ratio_list[file_index]}")

        #get the current short arm
        current_short_arm_length = short_arm_length_list[file_index]

        #get the current long arm
        current_long_arm_length = long_arm_length_list[file_index]

        #get the current normalized data
        current_normalized_data = normalized_data_list[normalized_data_list_indexes[file_index]]

        #get the short arm difference
        short_arm_difference = int(max_short_arm_length - current_short_arm_length)

        #get the long arm difference
        long_arm_difference = int(max_long_arm_length - current_long_arm_length)        

        #if the short arm difference is greater than 0
        if short_arm_difference > 0:

            #print the normalized data shape
            print(f"Normalized data shape: {current_normalized_data.shape}")

            #pad the normalized data
            current_normalized_data = np.pad(current_normalized_data, ((0,0),(0,0),(0,0),(0,0),(short_arm_difference,0)), mode='constant', constant_values=0)

            #loop through the short arm difference
            for short_arm_index in range(short_arm_difference):

                #set the pixel value to 0
                background_channel_image[0,0,0,file_index,short_arm_index] = 50

        #if the long arm difference is greater than 0
        if long_arm_difference > 0:

            #pad the normalized data
            current_normalized_data = np.pad(current_normalized_data, ((0,0),(0,0),(0,0),(0,0),(0,long_arm_difference)), mode='constant', constant_values=0)

            #loop through the long arm difference
            for long_arm_index in range(long_arm_difference):

                #set the pixel value to 0 in reverse
                background_channel_image[0,0,0,file_index,-(long_arm_index+1)] = 50

        #if the file index is 0
        if file_index == 0:

            #set the combined image
            combined_image = current_normalized_data

            #continue to the next file
            continue

        #else, add the image to the combined image
        else:

            #add the image to the combined image
            combined_image = np.concatenate((combined_image, current_normalized_data), axis=3)

    #get a copy of the combined image
    combined_image_copy = combined_image.copy()

    #concatenate the background channel image to the combined image copy
    combined_image_copy = np.concatenate((combined_image_copy, background_channel_image), axis=2)

    #cast it to float 32
    combined_image_copy = combined_image_copy.astype(np.float32)

    #reverse the y
    combined_image_copy = np.flip(combined_image_copy, axis=3)

    #print the combined image shape
    print(f"Combined image shape: {combined_image.shape}")

    #get the final image file name
    final_image_file_name = working_directory + "c018_megasome_split_chromosomes_combined_image2.tif"

    #set the backgrund channel image file name
    background_channel_image_file_name = working_directory + "c018_megasome_split_chromosomes_background_channel_image2.tif"

    #get the combined image and save it
    #tifffile.imwrite(final_image_file_name, combined_image, imagej=True, metadata={'axes': 'TZCYX'})

    #get the background channel image and save it
    tifffile.imwrite(background_channel_image_file_name, combined_image_copy, imagej=True, metadata={'axes': 'TZCYX'})

    exit()

    #make the napari viewer
    viewer = napari.Viewer()

    #loop through the channels
    for channel in range(combined_image.shape[2]):

        #get the channel data
        channel_data = combined_image[:,:,channel,:,:]

        #add it to the viewer
        image_layer = viewer.add_image(channel_data)

        #set the name
        image_layer.name = f"Channel {channel+1}"

        #set the mode to additive
        image_layer.blending = "additive"

    #run the viewer
    napari.run()

    exit()

#endregion ################################ END OF MAIN ##########################################


