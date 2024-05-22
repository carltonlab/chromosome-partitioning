#region ##################################### DESCRIPTION #############################################

"""
This script is used to measure the arm differences of the straightened chromosomes after:

1. The crossover sites have been obtained (c012_get_straightened_chromosomes_co_position.ijm)
2. The chromosomes have been sum projected and normalized (c012_normalize_straightened_chromosomes_by_channel.py)

The script will measure the average intensity of the short and long arms of the chromosomes and calculate the difference between them.
It will also plot the differences and save the plot as a .png and .pdf file.

It will create a csv file with the following values:
    1)file_name
    2)short_arm_lenth
    N)channel_short_arm_average_intensity
    N)channel_long_arm_average_intensity
    *The N depends on the number of channels being measured. It will do all channels in the image. 

The script will also save a pickle file that can be read as a dictionary in python with many
parameters for the images. Could be useful for further analysis.

The script will get the directory where it is located and get all the files that end with _str.tif

Make sure that the _str_rois.zip files are in the same directory as the _str.tif files.
Make sure that the _str_sum_proj.tif files are in the same directory as the _str.tif files.
Make sure that the _str_normalized_sum_proj.tif files are in the same directory as the _str.tif files.

"""

#endregion ################################## END DESCRIPTION #########################################


#region ##################################### IMPORTS #################################################

from matplotlib import pyplot as plt
import pandas
import roifile
import tifffile
import numpy as np
import sys
import os
import pickle

#endregion ################################## END IMPORTS #############################################


#region ##################################### FUNCTIONS ###############################################

#function to save the csv file
def save_csv_file(saving_directory, saving_dictionary, saving_file_name):

    #make the file list
    sav_file_list = []

    #make the short arm list
    sav_short_arm_list = []

    #make the long arm list
    sav_long_arm_list = []

    #make a list for the short arm lengths
    sav_short_arm_length_list = []

    #make the channel list
    sav_channel_list = []

    file_counter = 0

    #loop through the pickle data
    for file_name in saving_dictionary:
        
        #append the file name to the file list
        sav_file_list.append(file_name)

        #start the short arm list
        current_short_arm_list = []

        #start the long arm list
        current_long_arm_list = []

        #if the file counter is 0
        if file_counter == 0:

            #loop through the values in the pickle data
            for channel in saving_dictionary[file_name]:

                #get the channel name
                channel_name = saving_dictionary[file_name][channel]['name']

                #print the pickle data
                print(f'the pickle data is: {saving_dictionary[file_name][channel]}')

                #add the channel name to the channel list
                sav_channel_list.append(channel_name)

                #print the channel name
                print(f'the channel name is: {channel_name}')

                #add one to the file counter
                file_counter += 1

        for channel_i, channel in enumerate(saving_dictionary[file_name]):

            #if the channel index is 0
            if channel_i == 0:

                #get the short arm length
                short_arm_length = saving_dictionary[file_name][channel]['short_arm_length']

                #append the short arm length to the short arm length list
                short_arm_length_list.append(short_arm_length)
            
            #get the short arm value
            short_arm_value = saving_dictionary[file_name][channel]['short_arm_average_intensity']

            #get the long arm value
            long_arm_value = saving_dictionary[file_name][channel]['long_arm_average_intensity']

            #append the short arm value to the current short arm list
            current_short_arm_list.append(short_arm_value)

            #append the long arm value to the current long arm list
            current_long_arm_list.append(long_arm_value)

        #append the current short arm list to the short arm list
        sav_short_arm_list.append(current_short_arm_list)

        #append the current long arm list to the long arm list
        sav_long_arm_list.append(current_long_arm_list)

    #make the header of the csv file
    header = ['file_name', 'short_arm_lenth']

    #loop through the channel list
    for channel in sav_channel_list:

        #add the channel name to the header
        header.append(f'{channel}_short_arm_average_intensity')

        #add the channel name to the header
        header.append(f'{channel}_long_arm_average_intensity')

    #get the universal list
    universal_list = []

    #loop through the header and apppend an empty list to the universal list
    for header_name in header:

        #append an empty list to the universal list
        universal_list.append([])

    #loop through the file list
    for file_index, file in enumerate(sav_file_list):

        #set the universal list counter
        universal_list_counter = 0

        #append the file name to the universal list
        universal_list[universal_list_counter].append(file)

        #add one to the universal list counter
        universal_list_counter += 1

        #append the short arm length to the universal list
        universal_list[universal_list_counter].append(short_arm_length_list[file_index])

        #add one to the universal list counter
        universal_list_counter += 1

        #loop through the channel list
        for channel_index, channel in enumerate(sav_channel_list):

            #append the short arm value to the universal list
            universal_list[universal_list_counter].append(sav_short_arm_list[file_index][channel_index])

            #add one to the universal list counter
            universal_list_counter += 1

            #append the long arm value to the universal list
            universal_list[universal_list_counter].append(sav_long_arm_list[file_index][channel_index])

            #add one to the universal list counter
            universal_list_counter += 1

    #make a new data frame with the file name column
    data_frame = pandas.DataFrame(universal_list[0], columns=[header[0]])

    #add the short arm length column to the data frame
    data_frame[header[1]] = universal_list[1]

    #loop through the header list minus the first item
    for header_name in header[2:]:

        #add the header name to the data frame
        data_frame[header_name] = universal_list[header.index(header_name)]

    #get the index of the last . in the file path
    last_dot_index = saving_file_name.rfind('.')

    #get the file path without extension
    file_name_without_extension = saving_file_name[:last_dot_index]

    #make the saving csv file path
    saving_csv_file_path = f'{saving_directory}{file_name_without_extension}_with_short_arm.csv'

    #save the data frame to a csv file
    data_frame.to_csv(saving_csv_file_path, index=False)

#endregion ################################## END FUNCTIONS ###########################################1




#region ##################################### GLOBAL VARIABLES ########################################

#set the plotting channels and their names
plotting_channels = {0:{"name":"DAPI", "plotting":True}, 1:{"name":"GFP", "plotting":False}, 2:{"name":"SYP-1(T452A)", "plotting":True}}

#set the saving file name for the dictionary with the values
saving_file_name = "c012_short_long_arm_differences_gfpcosa1_t452a_r3.pkl"

#saving figure name declaration
saving_figure_name = "c012_arm_differences_shuffled"

#save dictionary flag
save_dictioanry = True

#save figure flag
save_figure = False

#endregion ################################## END GLOBAL VARIABLES ####################################



#region ##################################### FUNCTIONS ###############################################



#endregion ################################## END FUNCTIONS ###########################################



#region ##################################### MAIN ####################################################

#if name is main
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

    #start the sving dictioanry322 qa   =
    saving_dictionary = {}

    #loop through the files
    for working_file in  working_file_list:

        #add the file to the saving dictionary
        saving_dictionary[working_file] = {}

        #print a space
        print("")

        #print the file you're working with
        print(f"Working with file: {working_file}")

        #get the sum_proj.tif file name
        sum_proj_file_name = working_file.replace("_str.tif", "_str_normalized_sum_proj.tif")

        #print the sum proj file name
        print(f"Sum proj file name: {sum_proj_file_name}")

        #get the rois file name
        rois_file_name = working_file.replace("_str.tif", "_str_rois.zip")

        #print the rois file name
        print(f"Rois file name: {rois_file_name}")

        #open the rois file
        rois_file = roifile.roiread(saving_directory + rois_file_name)

        #get the subpixel coordinates
        co_coords = rois_file[0].subpixel_coordinates[0]

        #get the short arm roi
        short_arm_roi = rois_file[1]

        #get the rois top, bottom, left and right coords
        short_arm_top = short_arm_roi.top
        short_arm_bottom = short_arm_roi.bottom
        short_arm_left = short_arm_roi.left
        short_arm_right = short_arm_roi.right

        #get the long arm roi
        long_arm_roi = rois_file[2]

        #get the rois top, bottom, left and right coords
        long_arm_top = long_arm_roi.top
        long_arm_bottom = long_arm_roi.bottom
        long_arm_left = long_arm_roi.left
        long_arm_right = long_arm_roi.right

        #set them to ints
        co_coords = [int(co_coord) for co_coord in co_coords]

        #print the co_coords
        print(f"Co coords: {co_coords}")

        #get the sum_proj_image data
        sum_proj_image = tifffile.imread(saving_directory + sum_proj_file_name)

        #get the shape of the sum_proj_image
        current_image_shape = sum_proj_image.shape

        #print it
        print(f"Current image shape: {current_image_shape}")

        #get the metadata
        metadata = tifffile.TiffFile(saving_directory + sum_proj_file_name).imagej_metadata

        #print the metadata
        print(f"Metadata: {metadata}")

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
            sum_proj_image = np.expand_dims(sum_proj_image, axis=adding_indexes)

            #print the new shape
            print(f"New shape: {sum_proj_image.shape}")

        #loop through the channels
        for channel_object in plotting_channels:

            #get the channel
            channel = channel_object

            #get if the channel is plotting
            plotting = plotting_channels[channel]["plotting"]
            
            #print if the channel is plotting
            print(f"Plotting channel: {plotting_channels[channel]['plotting']}, for channel {channel}")

            #if you need to plot this channel
            if plotting:

                #print that the channel was added
                print(f"Channel {channel} was added")

                #add the file and the channel
                saving_dictionary[working_file][channel] = {"name":plotting_channels[channel]["name"]}

                #print the saving dictionary
                print(f"Saving dictionary: {saving_dictionary}")

                #print the channel name
                print(f"Channel name: {plotting_channels[channel]['name']}")

                #get the current channel to a new array
                current_channel = sum_proj_image[:, :, channel, :, :].copy()

                #add the dimension
                current_channel = np.expand_dims(current_channel, axis=2)

                #print the channel shape
                print(f"Channel shape: {current_channel.shape}")

                #get the total intensity
                total_intensity = np.sum(current_channel)

                #print the total intensity
                print(f"Total intensity: {total_intensity}")

                #get the number of pixels
                number_of_pixels = current_channel.shape[3] * current_channel.shape[4]

                #get the chr average intensity
                chr_average_intensity = total_intensity / number_of_pixels

                #add the chr average intensity to the saving dictionary
                saving_dictionary[working_file][channel]["chr_average_intensity"] = chr_average_intensity

                #print the chr average intensity
                print(f"Chr average intensity: {chr_average_intensity}")

                #get the short arm averate intensity
                short_arm_average_intensity = np.sum(current_channel[:, :, :, short_arm_top:short_arm_bottom, short_arm_left:short_arm_right]) / ((short_arm_bottom - short_arm_top) * (short_arm_right - short_arm_left))

                #add the short arm average intensity to the saving dictionary
                saving_dictionary[working_file][channel]["short_arm_average_intensity"] = short_arm_average_intensity

                #get the long arm averate intensity
                long_arm_average_intensity = np.sum(current_channel[:, :, :, long_arm_top:long_arm_bottom, long_arm_left:long_arm_right]) / ((long_arm_bottom - long_arm_top) * (long_arm_right - long_arm_left))

                #add the long arm average intensity to the saving dictionary
                saving_dictionary[working_file][channel]["long_arm_average_intensity"] = long_arm_average_intensity

                #get the long arm minus short arm
                long_arm_minus_short_arm = long_arm_average_intensity - short_arm_average_intensity

                #add the long arm minus short arm to the saving dictionary
                saving_dictionary[working_file][channel]["long_arm_minus_short_arm"] = long_arm_minus_short_arm

                #get the normalized long arm minus short arm
                normalized_long_arm_minus_short_arm = long_arm_minus_short_arm / chr_average_intensity

                #add the normalized long arm minus short arm to the saving dictionary
                saving_dictionary[working_file][channel]["normalized_long_arm_minus_short_arm"] = normalized_long_arm_minus_short_arm

                #get the long arm length
                long_arm_length = long_arm_right - long_arm_left

                #add the long arm length to the saving dictionary
                saving_dictionary[working_file][channel]["long_arm_length"] = long_arm_length

                #get the short arm length
                short_arm_length = short_arm_right - short_arm_left

                #add the short arm length to the saving dictionary
                saving_dictionary[working_file][channel]["short_arm_length"] = short_arm_length

                #get the ratio
                ratio = short_arm_length / long_arm_length

                #add the ratio to the saving dictionary
                saving_dictionary[working_file][channel]["long_to_short_arm_ratio"] = ratio

    #print the saving dictionary for the first file
    print(f"Saving dictionary for {working_file}: {saving_dictionary[working_file]}")

    #if the save dictionary flag is true
    if save_dictioanry:

        #save the dictionary
        with open(saving_directory + saving_file_name, "wb") as f:
            pickle.dump(saving_dictionary, f)

    #save the csv file
    save_csv_file(saving_directory, saving_dictionary, saving_file_name)


    #print a space
    print("")

    #get the list of plotting channels
    plotting_channel_list = [channel for channel in plotting_channels if plotting_channels[channel]["plotting"]]

    #make the plot
    fig, axs = plt.subplots(len(plotting_channel_list), 1, figsize=(10, len(plotting_channel_list)*10))

    #get a plot counter
    plot_counter = 0

    #loop through the plotting channels
    for plotting_channel in plotting_channel_list:

        #get the list of all the normalized long arm minus short arm values
        normalized_long_arm_minus_short_arm_list = [saving_dictionary[working_file][plotting_channel]["normalized_long_arm_minus_short_arm"] for working_file in saving_dictionary]

        #get the list of the short arm lengths
        short_arm_length_list = [saving_dictionary[working_file][plotting_channel]["short_arm_length"] for working_file in saving_dictionary]

        #get a list of the names
        name_list = [working_file for working_file in saving_dictionary]

        #sort the lists by the short arm lengths
        short_arm_length_list, normalized_long_arm_minus_short_arm_list, name_list = zip(*sorted(zip(short_arm_length_list, normalized_long_arm_minus_short_arm_list, name_list)))

        #loop through the normalized long arm minus short arm list
        for index, value in enumerate(normalized_long_arm_minus_short_arm_list):

            #if the value is greater than 0
            if value > 0:

                #plot the value with a blue color
                axs[plot_counter].scatter(value, index, color="blue", edgecolors="black")

                #if the channel is 3
                if plotting_channel == 3:
                    
                    #evaluated list
                    evaluated_list = ["20160217_cosa1gfp_GFPSYP1P2SYP1_eg_01_5_R3D.dv_add_decon.zs_R3_sbs_03.STR_chr6_cut_str.tif","20160217_cosa1gfp_GFPSYP1P2SYP1_eg_01_5_R3D.dv_add_decon.zs_R3_sbs_03.STR_chr1_cut_str.tif", "20160217_cosa1gfp_GFPSYP1P2SYP1_eg_01_5_R3D.dv_add_decon.zs_R3_sbs_03.STR_chr5_cut_str.tif","20160211_cosa1gfp_DAPI_GFP_SYP1phos1_SYP1_g1_5_R3D.dv_add_decon.zs_R3_sbs_01_chr1_str.tif","20160217_cosa1gfp_GFPSYP1P2SYP1_eg_01_5_R3D.dv_add_decon.zs_R3_sbs_04.STR_chr1_cut_str.tif","20160211_cosa1gfp_DAPI_GFP_SYP1phos1_SYP1_g1_5_R3D.dv_add_decon.zs_R3_sbs_09.STR_chr1_cut_str.tif","20160217_cosa1gfp_GFPSYP1P2SYP1_eg_01_5_R3D.dv_add_decon.zs_R3_sbs_03.STR_chr4_cut_str.tif","AS5-4_20180307_gfpcosa1_GFP_SYP1phos_panSYP1_g4_01_3_R3D.dv_add_decon.zs_R3_sbs_01.STR_chr4_cut_str.tif", "AS5-4_20180307_gfpcosa1_GFP_SYP1phos_panSYP1_g4_01_3_R3D.dv_add_decon.zs_R3_sbs_09.STR_chr1_cut_str.tif"]

                    #if the name is in the evaluated list
                    if not name_list[index] in evaluated_list:

                        #print the nam,e
                        print(f"Name: {name_list[index]}, value: {value}")

            #if the value is less than 0
            else:

                #plot the value with a red color
                axs[plot_counter].scatter(value, index, color="magenta", edgecolors="black")

        #set the 0 to a vertical line
        axs[plot_counter].axvline(0, color="green", linestyle="--")

        #set the ax channel title
        axs[plot_counter].set_title(plotting_channels[plotting_channel]["name"])

        #add one to the plot
        plot_counter += 1
    
    #loop through the axs
    for ax in axs:

        #set the x limit
        ax.set_xlim(-4, 4)

    #if the save figure flag is true
    if save_figure:

        #save the figure
        plt.savefig(saving_directory + saving_figure_name + ".png", dpi=300)

        #save the figure
        plt.savefig(saving_directory + saving_figure_name + ".pdf", dpi=300)

#endregion ################################## END MAIN ################################################




