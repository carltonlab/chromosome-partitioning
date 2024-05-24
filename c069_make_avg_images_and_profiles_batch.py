#region ######################################## DESCRIPTION ########################################

"""
This script will make the average projected images and the profiles of the newly generated images. 

It looks for the "_str.tif" files and then makes the average projections. 

It then calculates the average profiles for the channels and saves them in the "avg_profiles" directory.

The images have the term "_avg_proj.tif" and the profiles have the term "_proj_profile.csv".

You need to have the "_str_sum_proj.tif" and the "_proj_profile.csv" files in the same directory as the "_str.tif" files.

For this the script called "c069_str_files_flip_get_crossover_and_get_sum_profile.ijm" needs to be already run to
get the _reversed files if they exist. 
"""

#endregion ##################################### DESCRIPTION ########################################


import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage import io
from tifffile import TiffFile
import tifffile
import tkinter as tk
from tkinter import filedialog

#get the name of the script
script_name = os.path.basename(__file__)

#get the name only without the parent directories
script_name = script_name.split("/")[-1]

#set the functions for the log
#the function to start the log
def start_log(script_name, main_dir):
    #get the date and time
    date_and_time = datetime.datetime.now()

    #get the year
    year = str(date_and_time.year)

    #get the month
    month = str(date_and_time.month)

    #get the day
    day = str(date_and_time.day)

    #get the hour
    hour = str(date_and_time.hour)

    #get the minute
    minute = str(date_and_time.minute)

    #get the second
    second = str(date_and_time.second)    

    #get the script name without the extension
    script_name_no_ext = script_name.split(".")[0]

    #get the log name
    log_name = script_name_no_ext + "_"+year+"_"+month+"_"+day+"_"+hour+"_"+minute+"_"+second+"_log.txt"

    #get the prompt
    adding_string = f"[{year}-{month}-{day} {hour}:{minute}:{second}] {script_name} started"

    #write the adding prompt to the log file
    with open(main_dir + log_name, "w") as log_file:

        #write the prompt
        log_file.write(adding_string + "\n")

    #print the prompt
    print(adding_string)

    return log_name

#the function to add to the log
def add_to_log(log_name, main_dir, adding_string):

    #get the date and time
    date_and_time = datetime.datetime.now()

    #get the year
    year = str(date_and_time.year)

    #get the month
    month = str(date_and_time.month)

    #get the day
    day = str(date_and_time.day)

    #get the hour
    hour = str(date_and_time.hour)

    #get the minute
    minute = str(date_and_time.minute)

    #get the second
    second = str(date_and_time.second)

    #get the prompt
    adding_string = f"[{year}-{month}-{day} {hour}:{minute}:{second}] {adding_string}"

    #write the adding prompt to the log file
    with open(main_dir + log_name, "a") as log_file:

        #write the prompt
        log_file.write(adding_string + "\n")
    
    #print the prompt
    print(adding_string)

#the function to end the log
def end_log(log_name, main_dir, script_name):

    #get the date and time
    date_and_time = datetime.datetime.now()

    #get the year
    year = str(date_and_time.year)

    #get the month
    month = str(date_and_time.month)

    #get the day
    day = str(date_and_time.day)

    #get the hour
    hour = str(date_and_time.hour)

    #get the minute
    minute = str(date_and_time.minute)

    #get the second
    second = str(date_and_time.second)    

    #get the prompt
    adding_string = f"[{year}-{month}-{day} {hour}:{minute}:{second}] {script_name} finished"

    #write the adding prompt to the log file
    with open(main_dir + log_name, "a") as log_file:

        #write the prompt
        log_file.write(adding_string + "\n")

    #print the prompt
    print(adding_string)

np.set_printoptions(precision=4, suppress=True)

#get the path to the file
root = tk.Tk()
root.withdraw()

#get a directory using tkinter and set the starting directory 
main_dir = filedialog.askdirectory() + "/"

#start the log
log_name = start_log(script_name, main_dir)

#add to the log
adding_string = "The directory selected is: " + main_dir
add_to_log(log_name, main_dir, adding_string)

#get the saving directory string
saving_dir = main_dir + "avg_profiles/"

#find out if the avg_profiles directory exists
if not os.path.exists(saving_dir):

    #make the avg_profiles directory
    os.mkdir(saving_dir)

    #log that it has been created
    adding_string = "The avg_profiles directory has been created"

#get the file list that ends with _str.tif
file_list = [f for f in os.listdir(main_dir) if f.endswith("_str.tif")]

#add to the log
adding_string = "The file list is: " + str(file_list)
add_to_log(log_name, main_dir, adding_string)

#loop through the file list
for file in file_list:

    #add to the log
    adding_string = "The current file is: " + file
    add_to_log(log_name, main_dir, adding_string)

    #get the sum_proj.tif file
    sum_proj_file = file.replace("_str.tif", "_str_sum_proj.tif")

    #get the profile csv file
    profile_csv_file = sum_proj_file.replace("_proj.tif", "_proj_profile.csv")

    #find out if there's a reversed
    sum_proj_reversed_file = file.replace("_str.tif", "_str_sum_proj_reversed.tif")

    #get a flag for the reversed exists
    reversed_exists = False

    #find out if the sum_proj_reversed file exists
    if os.path.exists(main_dir + sum_proj_reversed_file):

        #rename the profile csv to the reversed
        profile_csv_file = profile_csv_file.replace("_proj_profile.csv", "_proj_reversed_profile.csv")

        #raise the flag
        reversed_exists = True
    
    #log that you are loading the csv
    add_to_log(log_name, main_dir, "Loading the csv file: "+ main_dir + profile_csv_file)

    #load the csv file inot a pandas array
    profile_csv = pd.read_csv(main_dir + profile_csv_file)

    #add to the log
    add_to_log(log_name, main_dir, "The csv file was loaded")

    #get the co_mid
    co_mid = profile_csv["co_mid"][0]

    #get the co_start
    co_start = profile_csv["co_start"][0]

    #get the co_end
    co_end = profile_csv["co_end"][0]

    #log that the parameters are obtained
    add_to_log(log_name, main_dir, "The parameters co_mid = " + str(co_mid) + ", co_start = " + str(co_start) + ", co_end = " + str(co_end) + " were obtained")

    #log that you're loading the image
    add_to_log(log_name, main_dir, "Loading the image: " + main_dir + sum_proj_file)

    #load the current image
    current_image = io.imread(main_dir + file)

    #add to the log
    adding_string = "The image was read"
    add_to_log(log_name, main_dir, adding_string)

    #get the meta data
    with TiffFile(main_dir + file) as tif:
        tif_metadata = tif
    
    #add to the log
    adding_string = "The metadata was read"

    #get the imagej_metadata
    imagej_metadata = tif_metadata.imagej_metadata

    #add to the log
    adding_string = "The imagej metadata was read"
    add_to_log(log_name, main_dir, adding_string)

    #get the number of images
    image_number = imagej_metadata["images"]

    #find out if it has pixel units
    if "unit" in imagej_metadata:
        #get the pixel units
        pixel_units = imagej_metadata["unit"]
    else:
        #set the pixel units to none
        pixel_units = None

    #find out if there's pixel size
    if "spacing" in imagej_metadata:
        #get the pixel size
        z_size = imagej_metadata["spacing"]
    else:
        #set the pixel size to none
        z_size = None

    #find out if there's channels
    if "channels" in imagej_metadata:
        #get the channels
        channels = imagej_metadata["channels"]
    else:
        #set the channels to none
        channels = None

    #find out if there's slices
    if "slices" in imagej_metadata:
        #get the slices
        slices = imagej_metadata["slices"]
    else:
        #set the slices to none
        slices = None

    def _xy_voxel_size(tags, key):

        assert key in ['XResolution', 'YResolution']

        if key in tags:

            num_pixels, units = tags[key].value
            return units/num_pixels
        
        return 1

    #get the tags
    tags = tif_metadata.pages[0].tags

    #get the x voxel size
    x_pixel_size = _xy_voxel_size(tags, 'XResolution')

    #get the y voxel size
    y_pixel_size = _xy_voxel_size(tags, 'YResolution')

    #get the height based on the current image shape
    height = current_image.shape[2]

    #get the width based on the current image shape
    width = current_image.shape[3]

    #get the dictionary with the number of slices
    slice_dictionary = {}

    #populate the dictionary
    for i in range(0, slices):

        #add the slice to the dictionary (first is the slices, then its the channels)
        slice_dictionary[i] = {0:[],1:[]}

    #loop through the slices
    for i in range(0, slices):

        #loop through the channels
        for j in range(0, channels):

            #get the current slice
            slice_dictionary[i][j] = current_image[i][j]

    #log that you will create the new image to hold the avg projection
    add_to_log(log_name, main_dir, "Creating the new image to hold the avg projection")

    #Get a multi dimensional array of the images
    avg_images = np.zeros((channels, height, width))  

    #log that the avg_proj image was created
    add_to_log(log_name, main_dir, "The avgerage proj image was created")

    #log that you're averaging the images
    add_to_log(log_name, main_dir, "Averaging the original images")

    #loop through the  width
    for i in range(0,width):

        #loop through the height
        for j in range(0,height):

            #get the new values
            channel1_sum_value = 0
            channel1_not_zero = 0

            channel2_sum_value = 0
            channel2_not_zero = 0

            channel1_avg_value = 0
            channel2_avg_value = 0

            #loop through the slices
            for k in range(0, slices):       

                #set the channel 1 current value
                channel1_current_value = slice_dictionary[k][0][j][i]

                #set the channel 2 current value
                channel2_current_value = slice_dictionary[k][1][j][i]

                #find out if the current value is not zero
                if channel1_current_value != 0:

                    #add to the sum
                    channel1_sum_value += channel1_current_value

                    #add to the not zero
                    channel1_not_zero += 1

                #find out if the current value is not zero
                if channel2_current_value != 0:

                    #add to the sum
                    channel2_sum_value += channel2_current_value

                    #add to the not zero
                    channel2_not_zero += 1
            
            #find out if the channel 1 not zero is not zero
            if channel1_not_zero != 0:

                #get the average
                channel1_avg_value = channel1_sum_value / channel1_not_zero
            else:
                #set the average to zero
                channel1_avg_value = 0


            #find out if the channel 2 not zero is not zero
            if channel2_not_zero != 0:

                #get the average
                channel2_avg_value = channel2_sum_value / channel2_not_zero
            else:
                #set the average to zero
                channel2_avg_value = 0
            
            #set the new values
            avg_images[0][j][i] = channel1_avg_value
            avg_images[1][j][i] = channel2_avg_value
    
    #log that the image was averaged
    add_to_log(log_name, main_dir, "The images were averaged")

    #get the filename without extension
    filename_without_extension = os.path.splitext(file)[0]

    #add the saving file
    saving_file = filename_without_extension + "_avg_proj.tif"

    #set the new imagej metadata
    imagej_metadata["images"] = 2
    imagej_metadata["unit"] = pixel_units
    imagej_metadata["spacing"] = x_pixel_size
    imagej_metadata["channels"] = 2

    #log that the image will be saved
    add_to_log(log_name, main_dir, "The image will be saved at: " + main_dir + saving_file)

    avg_images_32 = avg_images.astype(np.float32)

    #save the image with a new metadata set
    tifffile.imwrite(main_dir + saving_file, avg_images_32, imagej=True, metadata={'axes': 'CYX', 'unit': imagej_metadata["unit"], 'spacing': imagej_metadata["spacing"], 'channels': imagej_metadata["channels"]})

    #log that the image was saved
    add_to_log(log_name, main_dir, "The image was saved")

    #if the reversed exists flag is raised
    if reversed_exists:
        
        #log that because there was a reversed image, it will now be reverse
        add_to_log(log_name, main_dir, "There was a reversed version of the original image, reversing the new one too.")
        
        #get the reversed projection file
        reversed_projection_file = saving_file.replace("_avg_proj.tif", "_avg_proj_reversed.tif")

        #get loop through the height
        for i in range(0, height):

            #reverse the corresponding row
            avg_images[0][i] = avg_images[0][i][::-1]
            avg_images[1][i] = avg_images[1][i][::-1]

        #log that the image was reversed
        add_to_log(log_name, main_dir, "The image was reversed")

        #log that the image will be saved
        add_to_log(log_name, main_dir, "The reversed image will be saved at: " + main_dir + reversed_projection_file)

        #save the image with a new metadata set
        tifffile.imsave(main_dir + reversed_projection_file, avg_images)

        #log that the reversed image was saved
        add_to_log(log_name, main_dir, "The reversed image was saved")
    
    #log that the dataframe profile will be created
    add_to_log(log_name, main_dir, "The dataframe profile will be created")

    #get a new pandas dataframe with the number of rows set to the width
    df = pd.DataFrame(index = range(0, width), columns = ["channel1", "channel2", "co_mid","co_start","co_end"])

    #log that the dataframe was created
    add_to_log(log_name, main_dir, "The dataframe was created")

    #loop through the width
    for i in range(0, width):

        #start the new avg_values for profile
        channel1_current_profile_point = 0
        channel2_current_profile_point = 0

        #start the new counts for the profiel points
        channel1_profile_count = 0
        channel2_profile_count = 0

        #start the new avg_values for profile
        channel1_profile_avg_value = 0
        channel2_profile_avg_value = 0

        #loop through the height
        for j in range(0, height):    

            #get the current channel 1 value
            channel1_current_value = avg_images[0][j][i]

            #get the current channel 2 value
            channel2_current_value = avg_images[1][j][i]

            #find out if the current value is not zero
            if channel1_current_value != 0:

                #add to the sum
                channel1_current_profile_point += channel1_current_value

                #add to the not zero
                channel1_profile_count += 1

            #find out if the current value is not zero
            if channel2_current_value != 0:

                #add to the sum
                channel2_current_profile_point += channel2_current_value

                #add to the not zero
                channel2_profile_count += 1
            
        #find out if the channel 1 not zero is not zero
        if channel1_profile_count != 0:

            #get the average
            channel1_profile_avg_value = channel1_current_profile_point / channel1_profile_count
        else:
            #set the average to zero
            channel1_profile_avg_value = 0
        
        #find out if the channel 2 not zero is not zero
        if channel2_profile_count != 0:
                
            #get the average
            channel2_profile_avg_value = channel2_current_profile_point / channel2_profile_count
        else:
            #set the average to zero
            channel2_profile_avg_value = 0
        
        #set the values
        df["channel1"][i] = channel1_profile_avg_value
        df["channel2"][i] = channel2_profile_avg_value
        df["co_mid"][i] = co_mid
        df["co_start"][i] = co_start
        df["co_end"][i] = co_end
    
    #log that the dataframe was filled
    add_to_log(log_name, main_dir, "The dataframe was filled")

    #get the saving file
    profile_saving_file = saving_file.replace("_proj.tif", "_proj_profile.csv")

    #if there's a reversed
    if reversed_exists:

        #set the new profile saving file
        profile_saving_file = profile_saving_file.replace("_proj_profile.csv", "_proj_reversed_profile.csv")

    #log that the dataframe will be saved
    add_to_log(log_name, main_dir, "The dataframe will be saved at: " + saving_dir + profile_saving_file)

    #save the data frame
    df.to_csv(saving_dir + profile_saving_file, index = False)

    #log that the dataframe was saved
    add_to_log(log_name, main_dir, "The dataframe was saved")

    #log that you're done with the file
    add_to_log(log_name, main_dir, "Done with the file: " + file)

    #log an empty space
    add_to_log(log_name, main_dir, "")

#log that the script has finished
print("The script has finished running....")




    




