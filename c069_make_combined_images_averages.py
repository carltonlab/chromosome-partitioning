#region ####################################### DESCRIPTION ###############################################

"""

This script is used to make the combined average image for every channel. 

The files of the "_avg_proj.tif" and the "_avg_proj_profile.csv" need to be in the same directory. 
The script looks for all the .tif files so it is important that only the files that are needed are in the directory.
It is also important to have the file with the time points calle: "c069_file_timepoint_sort_order.txt" in the same directory.

There's a dictionary with the data that is saved in the results directory as a pickle file.

The script will create a new image with the average of all the images in the directory.
Each time point will be saved separately and the resulting image will be saved in the results directory.


"""

#endregion #################################### END OF DESCRIPTION ########################################


import datetime
import json
import os
import pickle
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage import io
from tifffile import TiffFile
import tifffile
import tkinter as tk
from tkinter import filedialog

#start the tkinter
root = tk.Tk()
root.withdraw()

######################## Global Variables ###############################

#region variables

#get the script name
script_name = os.path.basename(__file__)

#get the script directory
scripts_dir = os.path.dirname(__file__) + "/"

#get the main directory
#get a directory using tkinter and set the starting directory
main_dir = filedialog.askdirectory() + "/"

#set the results directory
results_dir = main_dir + "results/"

#if the results directory doesn't exist, create it
if not os.path.exists(results_dir):
    
        #make the directory
        os.mkdir(results_dir)

#create the dictionary for the saving results
saving_results_dict = {}

#get the time points file path
time_points_file_path = results_dir + "c069_file_timepoint_sort_order.txt"

#read the time points file
time_points_file = open(time_points_file_path, "r")

#read the time points file
time_points_file_read = time_points_file.read()

#split the time points file
time_points_order = time_points_file_read.split(",")

#get the flag to know if the time points csv results are saved
time_points_csv_results_saved = False

#endregion variables

######################## Functions ###############################

#region functions

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

#endregion functions

######################## Main ###############################

#region main

#start the log
log_name = start_log(script_name, main_dir)

#add to the log
add_to_log(log_name, main_dir, "The main directory was set to: " + main_dir)

#log the time points
add_to_log(log_name, main_dir, "The time points are: " + str(time_points_order))

#add to the log that the file list is being obtained
add_to_log(log_name, main_dir, "Obtaining the .tif file list.")

#get the file list
file_list = [file for file in os.listdir(main_dir) if file.endswith(".tif")]

#log that the list was obtained
add_to_log(log_name, main_dir, "The .tif file list was obtained.")

#add the number of files to the saving results dictionary
saving_results_dict["Number of Files"] = len(file_list)

#log the number of files
add_to_log(log_name, main_dir, "The number of files is: " + str(len(file_list)))

#log that it was added to the results dictionary
add_to_log(log_name, main_dir, "The number of files was added to the results dictionary.")

#log that you will start creating the images
add_to_log(log_name, main_dir, "Creating the images.")

#loop through the time_points_order_exists
for time_point in time_points_order:

    #log that you're working on the time point
    add_to_log(log_name, main_dir, "Working on time point " + str(time_point))

    #add the time point file list to the saving results dictionary
    saving_results_dict[str(time_point)] = {}

    #add the file list
    saving_results_dict[str(time_point)]["file_list"] = []

    #total_length
    total_length = 0

    #total height
    total_height = 0

    #total channels
    total_channels = 0

    #get the max left
    max_left = 0

    #get the max right
    max_right = 0

    #get the co_start_list
    co_start_list = []

    #get the average co_start
    average_co_start = 0

    #get the average co_end
    average_co_end = 0

    #get the co_end_list
    co_end_list = []

    #get the average co_mid
    average_co_mid = 0

    #get the co_mid_list
    co_mid_list = []

    #loop through the files
    for file in file_list:

        #if the time point is in the file
        if str(time_point) in file:
        
            #make a list of the file specifications
            file_specs = {}
            
            #add the file to the file specs
            file_specs["image_file"] = file

            #log that the file was added to the process
            add_to_log(log_name, main_dir, "The file " + file + " was added to the process.")

            #get the csv file name
            current_csv_file = file.replace(".tif", "_profile.csv")
            
            #log that you're loading the csv
            add_to_log(log_name, main_dir, "Loading the csv file " + current_csv_file)

            #append the csv file to the file specs
            file_specs["csv_file"] = current_csv_file

            #load the csv to a pandas dataframe
            current_csv_df = pd.read_csv(main_dir + current_csv_file)

            #get the current co mid
            current_co_mid = current_csv_df["co_mid"][0]

            #log the current co mid
            add_to_log(log_name, main_dir, "The current co mid is: " + str(current_co_mid))

            #append the co mid to the file specs
            file_specs["co_mid"] = current_co_mid

            #get the current co start
            current_co_start = current_csv_df["co_start"][0]

            #log the current co start
            add_to_log(log_name, main_dir, "The current co start is: " + str(current_co_start))

            #append the co start to the file specs
            file_specs["co_start"] = current_co_start

            #get the current co end
            current_co_end = current_csv_df["co_end"][0]

            #log the current co end
            add_to_log(log_name, main_dir, "The current co end is: " + str(current_co_end))

            #append the co end to the file specs
            file_specs["co_end"] = current_co_end

            #get the number of rows 
            number_of_rows = current_csv_df.shape[0]

            #get the right length
            right_length = number_of_rows - current_co_mid

            #log the right length
            add_to_log(log_name, main_dir, "The right length is: " + str(right_length))

            #append the right length to the file specs
            file_specs["right_length"] = right_length

            #get the left length
            left_length = current_co_mid

            #log the left length
            add_to_log(log_name, main_dir, "The left length is: " + str(left_length))

            #append the left length to the file specs
            file_specs["left_length"] = left_length

            #if the current co mid is greater than the max left
            if current_co_mid > max_left:
                
                #log that a new max left was found
                add_to_log(log_name, main_dir, "A new max left was found: " + str(current_co_mid))

                #set the max left to the current co mid
                max_left = current_co_mid
            
            #if the right length is bigger than the max right
            if right_length > max_right:

                #log that a new max right was found
                add_to_log(log_name, main_dir, "A new max right was found: " + str(right_length))

                #set the max right to the right length
                max_right = right_length

            #add the file specs to the file list
            saving_results_dict[str(time_point)]["file_list"].append(file_specs)

    #log thyat you're recalculating the images
    add_to_log(log_name, main_dir, "Recalculating the images.")

    #get the new co_mid
    average_co_mid = max_left

    #get the new total length
    total_length = max_left + max_right

    #make the images list
    images_dict = {}

    #loop through the saving_results_dict[str(time_point)]["file_list"]
    for file_object in saving_results_dict[str(time_point)]["file_list"]:

        #log that you're recalculating this one
        add_to_log(log_name, main_dir, "Recalculating: " + file_object["image_file"])

        #get the left_difference
        left_difference = max_left - file_object["left_length"]

        #log the left difference
        add_to_log(log_name, main_dir, "The left difference is: " + str(left_difference))
        
        #get the right difference
        right_difference = max_right - file_object["right_length"]

        #log the right difference
        add_to_log(log_name, main_dir, "The right difference is: " + str(right_difference))

        #add the left start to the object
        file_object["left_start"] = left_difference

        #add the right end to the object
        file_object["right_end"] = max_left + file_object["right_length"]

        #log the new start
        add_to_log(log_name, main_dir, "The new left start is: " + str(file_object["left_start"]))

        #log the new end
        add_to_log(log_name, main_dir, "The new right end is: " + str(file_object["right_end"]))

        #get the new co start
        new_co_start = file_object["co_start"] + left_difference

        #log the new co start
        add_to_log(log_name, main_dir, "The new co start is: " + str(new_co_start))

        #add the new_co_start to the file object
        file_object["new_co_start"] = new_co_start

        #append the new co start to the co start list
        co_start_list.append(new_co_start)

        #get the new co end
        new_co_end = file_object["co_end"] + left_difference

        #log the new co end
        add_to_log(log_name, main_dir, "The new co end is: " + str(new_co_end))

        #append the new co end to the co end list
        co_end_list.append(new_co_end)

        #add the new_co_end to the file object
        file_object["new_co_end"] = new_co_end

        #get the new co mid
        new_co_mid = file_object["co_mid"] + left_difference

        #log the new co mid
        add_to_log(log_name, main_dir, "The new co mid is: " + str(new_co_mid))

        #append the new co mid to the co mid list
        co_mid_list.append(new_co_mid)

        #add the new_co_mid to the file object
        file_object["new_co_mid"] = new_co_mid

        #log that the image is done being recalculated
        add_to_log(log_name, main_dir, "Done recalculating: " + file_object["image_file"])


    #get the average co start
    average_co_start = int(np.mean(co_start_list))

    #log the average co start
    add_to_log(log_name, main_dir, "The average co start is: " + str(average_co_start))

    #get the average co end
    average_co_end = int(np.mean(co_end_list))

    #log the average co end
    add_to_log(log_name, main_dir, "The average co end is: " + str(average_co_end))

    #add them to the saving results dict
    saving_results_dict[str(time_point)]["average_co_start"] = average_co_start

    #add them to the saving results dict
    saving_results_dict[str(time_point)]["average_co_end"] = average_co_end

    #log that you're initiating the resulting image
    add_to_log(log_name, main_dir, "Initiating the resulting image.")

    #open the first image
    first_image = io.imread(main_dir + saving_results_dict[str(time_point)]["file_list"][0]["image_file"])

    #get the channels of the first image
    channels = first_image.shape[0]

    #get the height of the first image
    height = first_image.shape[1]

    #make a new image with the channels, height and length
    resulting_image = np.zeros((channels, height, total_length))

    #log that the resulting image has been initialized
    add_to_log(log_name, main_dir, "The resulting image has been initialized.")

    #log that you're loading the images
    add_to_log(log_name, main_dir, "Loading the images.")

    #loop through the file list
    for file_object in saving_results_dict[str(time_point)]["file_list"]:

        #get the number of images
        number_of_images = len(saving_results_dict[str(time_point)]["file_list"])

        #get the image name
        image_name = file_object["image_file"]

        #log that you're opening the image
        add_to_log(log_name, main_dir, "Opening the image: " + image_name)

        #open the image
        current_image = io.imread(main_dir + image_name)

        #log that the image has been opened
        add_to_log(log_name, main_dir, "The image has been opened.")

        #add it to the images dict
        images_dict[image_name] = current_image

    #log that the images have been loaded
    add_to_log(log_name, main_dir, "All images have been loaded.")

    #log that you're averaging the images
    add_to_log(log_name, main_dir, "Averaging the images.")

    #loop through the channels
    for channel in range(channels):

        #log the channel you're working on
        add_to_log(log_name, main_dir, "Working on channel: " + str(channel))

        #loop thourhg the height
        for y_coord in range(height):

            #loop through the total length
            for x_coord in range(total_length):
                
                #get the x_coord sum
                x_coord_sum = 0

                #get the x_coord_count
                x_coord_count = 0

                #loop through the image_dict
                for image_name in images_dict:

                    #loop through the file list
                    for file_object in saving_results_dict[str(time_point)]["file_list"]:

                        #if the image name is the same as the file object image file
                        if image_name == file_object["image_file"]:

                            #if the x_coord is greater than the left start and less than the right end
                            if x_coord >= file_object["left_start"] and x_coord < file_object["right_end"]:

                                #get the x_coord_in_image
                                x_coord_in_image = x_coord - file_object["left_start"]

                                #add the pixel value to the x_coord_sum
                                x_coord_sum += images_dict[image_name][channel][y_coord][x_coord_in_image]

                                #add one to the x_coord_count
                                x_coord_count += 1
                
                #if the x_coord_count is 0
                if x_coord_count == 0:

                    #set the average to 0
                    average = 0

                #otherwise
                else:
                    
                    #get the average
                    average = x_coord_sum / x_coord_count

                #add the average to the resulting image
                resulting_image[channel][y_coord][x_coord] = average

    #log that the images have been averaged
    add_to_log(log_name, main_dir, "The images have been averaged.")

    #log that you're saving the resulting image
    add_to_log(log_name, main_dir, "Saving the resulting image.")

    #get the resulting image name
    resulting_image_name = "c069_resulting_avg_image_" + str(time_point) + ".tif"

    #save the resulting image
    io.imsave(results_dir + resulting_image_name, resulting_image)

    #log that the resulting image has been saved
    add_to_log(log_name, main_dir, "The resulting image has been saved.")

    #log that you're done with the time point
    add_to_log(log_name, main_dir, "Done with time point: " + str(time_point))

    #log an empty space
    add_to_log(log_name, main_dir, "")

#log that you're saving the results dict
add_to_log(log_name, main_dir, "Saving the results dict.")

#save the results dict as pickle 
pickle.dump(saving_results_dict, open(results_dir + "c069_results_dict.pickle", "wb"))

#log that the results dict has been saved
add_to_log(log_name, main_dir, "The results dict has been saved.")

#end log
end_log(log_name, main_dir, script_name)

#endregion main


