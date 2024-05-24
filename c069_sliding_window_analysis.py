#region ########################################## DESCRIPTION ##########################################

"""

This script will open the "avg_df_TIMEPONT.csv" files produced from the script "c069_plots_combine_by_time_point.py"
and make the sliding window analysis. It has some other analysis included too but the ones used for the paper are
the sliding window analysis.

To run, you need to pass the arguments. The first argument is the main directory where the files are located.

The second argument is the absolutes flag.

For the start to the left, in the paper we set it to 1 micron, to the right it was also set to 1 micron. 

The type must be set to crawl 

When you run the script, use the -h argument to get the possible parameters to set for the plot. 

When you run the script it should look something like this:

python c069_sliding_window_analysis.py -d DIR -a -ls 1 -re 1 -t crawl -cll 1 -crl 1

"""

#endregion ####################################### END DESCRIPTION ########################################








#region ////////////////// IMPORTS //////////////////////
import datetime
from math import ceil
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import sys
import argparse

#endregion ////////////////////// IMPORTS //////////////////////

#the command to run is: python3 ~/scripts/git/python/c069/c069_plot_avg_differences_from_combined_df_segment_specified.py $(pwd) abs(0/1) leftstart rightend ylim


#region ////////////////////// FUNCTIONS  //////////////////////

#the function to start the log
def start_log(script_name, main_dir, save_log_flag):
    
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

    #if the save log flag is true
    if save_log_flag == True:

        #write the adding prompt to the log file
        with open(main_dir + log_name, "w") as log_file:

            #write the prompt
            log_file.write(adding_string + "\n")

    #print the prompt
    print(adding_string)

    return log_name

#the function to add to the log
def add_to_log(log_name, main_dir, adding_string, save_log_flag):

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

    #if the save log flag is true
    if save_log_flag == True:

        #write the adding prompt to the log file
        with open(main_dir + log_name, "a") as log_file:

            #write the prompt
            log_file.write(adding_string + "\n")
    
    #print the prompt
    print(adding_string)

#the function to end the log
def end_log(log_name, main_dir, script_name, save_log_flag):

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

    #if the save log flag is true
    if save_log_flag == True:

        #write the adding prompt to the log file
        with open(main_dir + log_name, "a") as log_file:

            #write the prompt
            log_file.write(adding_string + "\n")

    #print the prompt
    print(adding_string)

#getting the custom ticks for the x axis
def get_custom_ticks(number_of_pixels, step_size, pixel_size):

    #set the ticks
    custom_ticks = []

    #set the labels
    custom_labels = []
    
    #get the total micron length
    total_micron_length = number_of_pixels * pixel_size

    #ceil the total micron length to the nearest jump size
    total_micron_length = ceil(total_micron_length / step_size) * step_size

    #get the number of steps
    number_of_steps = int(total_micron_length / step_size)

    #loop through the number of steps to set up the ticks and labels
    for i in range(0, number_of_steps + 1):

        #if it is 0
        if i == 0:

            #append the tick
            custom_ticks.append(i)

            #append the label
            custom_labels.append(0)
        
        #if it is more than 0 and less than the last
        if i > 0 and i < number_of_steps:

            #append the tick
            custom_ticks.append(i * step_size / pixel_size)

            #append the label
            custom_labels.append( round(i * step_size,1))
        
        #if it is the last
        if i == number_of_steps:

            #append the tick
            custom_ticks.append(i * step_size / pixel_size)

            #append the label
            custom_labels.append(round(total_micron_length,1))
        
    #get the together
    custom_ticks_and_labels = [custom_ticks, custom_labels]
    
    #return the values
    return custom_ticks_and_labels

#endregion ////////////////////// END FUNCTIONS  //////////////////////

#region ////////////////////// MAIN  //////////////////////

#if the arguments are more than 1
if len(sys.argv) > 1:

    #add the argument parser options
    parser = argparse.ArgumentParser(description='Plot the average differences from the combined dataframes.')

    #add the argument for the main directory
    parser.add_argument('main_dir', type=str, help='The main directory to use.')
    #add the argument for the absolutes flag that takes true or false
    parser.add_argument('-a', action='store_true', help='Use absolutes flag. If true, use absolutes, if false, do not use absolutes.')
    #add the argument for the left start
    parser.add_argument('-ls', type=float, help='The left start in microns from co start.')
    #add the argument for the right end
    parser.add_argument('-re', type=float, help='The right end in microns from co end.')
    #add the argument for the global y low limit
    parser.add_argument('-yl', type=float, help='The global y lower limit.')
    #add the argument for the global y high limit
    parser.add_argument('-yh', type=float, help='The global y higher limit.')
    #add the argument for the global x low limit
    parser.add_argument('-xl', type=float, help='The global x lower limit.')
    #add the argument for the global x high limit
    parser.add_argument('-xh', type=float, help='The global x higher limit.')
    #add an argument to use the auto x
    parser.add_argument('-ax', action='store_true', help='Use the auto x flag. If true, use the auto x, if false, do not use the auto x.')
    #add the argument for the save log flag
    parser.add_argument('-l', action='store_true', help='Save log flag. If true, save the log, if false, do not save the log.')
    #add an argument to normalize the points
    parser.add_argument('-np', action='store_true', help='Normalize the points above 0.')
    #add an argument to normalize the y axes
    parser.add_argument('-ny', action='store_true', help='Normalize the y axes.')
    #add an argument to normalize the y axis pr prebleach
    parser.add_argument('-nyp', action='store_true', help='Normalize the y axes in prebleach to t0.')
    #add an argument to get the type of plot
    parser.add_argument('-t', type=str, choices=["segment", "crawl"], help='The type of plot to make. Options are: "segment" or "crawl".')
    #add an argument to get crawl left length
    parser.add_argument('-cll', type=float, help='The crawl left length in microns.')
    #add an argument to get crawl right length
    parser.add_argument('-crl', type=float, help='The crawl right length in microns.')
    #add an optional argument for zoom start in plot
    parser.add_argument('-zs', type=float, help='The zoom start in microns.')
    #add an optional argument for zoom end in plot
    parser.add_argument('-ze', type=float, help='The zoom end in microns.')

    arguments = parser.parse_args()

#get the plot colors
plot_colors = ["royalblue", "blueviolet", "m", "y", "c", "m", "k"]

#get the pixel size
pixel_size = 0.042598146

#get the script file name
script_name = os.path.basename(__file__)

#initialize a flag to check if you require a main directory selection
main_dir_flag = True

#initialize the save log flag
save_log_flag = False

#set the left segment start to 0
left_segment_start_specified_flag = False

#set the left segment start to 0
left_segment_start = float(0)

#set a use absolutes flag
use_absolutes_flag = False

#set the right segment end specified flag
right_segment_end_specified_flag = False

#set the y lim specified flag
y_lim_specified_flag = False

#set the y limit
y_limits = [float(0), float(1)]

#set the x lim specified flag
x_lim_specified_flag = False

#set the x limit
x_limits = [float(0), float(1)]

#set the auto x flag
auto_x_flag = False

#set the normalize flag
normalize_points_flag = False

#set the normalize y axes flag
normalize_y_axes_flag = False

#set the normalize y axes prebleach flag
normalize_y_axes_prebleach_flag = False

#set the type of plot
plot_type = "segment"

#set the crawl left length
crawl_left_length = float(1)

#set the crawl right length
crawl_right_length = float(1)

#set the zoom flag
zoom_flag = False

#set the zoom start
zoom_start_length = None

#set the zoom end
zoom_end_length = None

#if there's more than one argument
if len(sys.argv) > 1:

    #get the arguments main_dir
    main_dir =  arguments.main_dir

    #if the first argument is a directory
    if os.path.isdir(main_dir):

        #lower the flag of the main_dir
        main_dir_flag = False

        #if the arguments ends with a /
        if main_dir.endswith("/"):

            main_dir = main_dir
        

        #if the argument does not end with a /
        else:
            
            #set the main directory to the first argument
            main_dir = main_dir + "/"
        
    #get the option for the absolutes flag
    if arguments.a:

        #set the use absolutes flag to true
        use_absolutes_flag = True
    
    #get the option for the log
    if arguments.l:
            
        #set the save log flag to true
        save_log_flag = True
    
    #if the left start exists
    if arguments.ls != None:

        #if the left start is 0 or less
        if arguments.ls <= 0:

            #print the error
            print("The left segment start must be greater than 0.")

            #exit
            exit()

        #raise the left segment start specified flag
        left_segment_start_specified_flag = True

        #set the left segment start to the argument
        left_segment_start = arguments.ls
    
    #if the right end exists
    if arguments.re != None:

        #if the right end is 0 or less
        if arguments.re <= 0:

            #print the error
            print("The right segment end must be greater than 0.")

            #exit
            exit()

        #raise the right segment end specified flag
        right_segment_end_specified_flag = True

        #set the right segment end to the argument
        right_segment_end = arguments.re
    
    #if the y low limit exists
    if arguments.yl != None:

        #flip the y limits flag
        y_lim_specified_flag = True

        #set the y low limit to the argument
        y_limits[0] = arguments.yl

    #if the y high limit exists
    if arguments.yh != None:

        #flip the y limits flag
        y_lim_specified_flag = True

        #set the y high limit to the argument
        y_limits[1] = arguments.yh

    #if the x low limit exists
    if arguments.xl != None:

        #flip the x limits flag
        x_lim_specified_flag = True

        #set the x low limit to the argument
        x_limits[0] = arguments.xl
    
    #if the x high limit exists
    if arguments.xh != None:

        #flip the x limits flag
        x_lim_specified_flag = True

        #set the x high limit to the argument
        x_limits[1] = arguments.xh

    #if the auto x limits flag is true
    if arguments.ax:

        #flip the x limits flag
        auto_x_flag = True

        #set the x low limit to 0
        x_limits[0] = 0

        #set the x high limit to 1
        x_limits[1] = 1

    #if the normalize flag is true
    if arguments.np:

        #set the normalize flag to true
        normalize_points_flag = True

    #if the normalize y axes flag is true
    if arguments.ny:

        #set the normalize y axes flag to true
        normalize_y_axes_flag = True
    
    #if the normalize y axes prebleach flag is true
    if arguments.nyp:

        #set the normalize y axes prebleach flag to true
        normalize_y_axes_prebleach_flag = True
    
    #set the plot type
    plot_type = arguments.t

    #if the type of plot is crawl
    if plot_type == "crawl":

        #if the crawl left length is specified
        if arguments.cll != None:

            #set the crawl left length to the argument
            crawl_left_length = arguments.cll

            #if the crawl left length is 0 or less
            if arguments.cll <= 0:

                #print the error
                print("The crawl left length must be greater than 0.")

                #exit
                exit()
        
        #if the crawl right length is specified
        if arguments.crl != None:

            #set the crawl right length to the argument
            crawl_right_length = arguments.crl

            #if the crawl right length is 0 or less
            if arguments.crl <= 0:

                #print the error
                print("The crawl right length must be greater than 0.")

                #exit
                exit()
    
    #if there's a zoom start or end
    if arguments.zs != None or arguments.ze != None:

        #set the zoom flag to true
        zoom_flag = True

        #if the zoom start is specified
        if arguments.zs != None:

            #set the zoom start to the argument
            zoom_start_length = arguments.zs

            #if the zoom start is less than 0
            if arguments.zs <= 0:

                #print the error
                print("The zoom start must be greater than 0.")

                #exit
                exit()
            
        #if the zoom end is specified
        if arguments.ze != None:

            #set the zoom end to the argument
            zoom_end_length = arguments.ze
        
            #if the zoom end is less than 0
            if arguments.ze <= 0:

                #print the error
                print("The zoom end must be greater or equal than 0.")

                #exit
                exit()    


#if the main_dir_flag is true
if main_dir_flag:
        
    ##get the path to the file
    root = tk.Tk()
    root.withdraw()

    #get a directory using tkinter and set the starting directory to the main directory at /extra_data
    main_dir = filedialog.askdirectory() + "/"

#start the log
log_name = start_log(script_name, main_dir, save_log_flag)

#get the saving directory
saving_dir = main_dir

#log the saving directory
add_to_log(log_name, main_dir, f"Saving directory: {saving_dir}", save_log_flag)

#log the plot type
add_to_log(log_name, main_dir, f"Plot type: {plot_type}", save_log_flag)

#if the log type is crawl
if plot_type == "crawl":

    #calculate the crawl_left_length_pixels
    crawl_left_length_pixels = int(crawl_left_length / pixel_size)

    #calculate the crawl_right_length_pixels
    crawl_right_length_pixels = int(crawl_right_length / pixel_size)

    #log the crawl left length
    add_to_log(log_name, main_dir, f"Crawl left length: {crawl_left_length}", save_log_flag)

    #log the crawl lef length pixels
    add_to_log(log_name, main_dir, f"Crawl left length (pixels): {crawl_left_length_pixels}", save_log_flag)

    #log the crawl right length
    add_to_log(log_name, main_dir, f"Crawl right length: {crawl_right_length}", save_log_flag)

    #log the crawl right length pixels
    add_to_log(log_name, main_dir, f"Crawl right length (pixels): {crawl_right_length_pixels}", save_log_flag)

#log the absolutes flag
add_to_log(log_name, main_dir, f"Use absolutes flag: {use_absolutes_flag}", save_log_flag)

#log the left segment start specified flag
add_to_log(log_name, main_dir, f"Left segment start specified flag: {left_segment_start_specified_flag}", save_log_flag)

#if it is true
if left_segment_start_specified_flag:

    #log the left segment start
    add_to_log(log_name, main_dir, f"Left segment start (microns): {left_segment_start}", save_log_flag)

#log the right segment end specified flag
add_to_log(log_name, main_dir, f"Right segment end specified flag: {right_segment_end_specified_flag}", save_log_flag)

#if it is true
if right_segment_end_specified_flag:

    #log the right segment end
    add_to_log(log_name, main_dir, f"Right segment end (microns): {right_segment_end}", save_log_flag)

#log the y limit specified flag
add_to_log(log_name, main_dir, f"Y limit specified flag: {y_lim_specified_flag}", save_log_flag)

#if it is true
if y_lim_specified_flag:

    #log the y limits
    add_to_log(log_name, main_dir, f"Y limits: {y_limits}", save_log_flag)

#log the normalize points flag
add_to_log(log_name, main_dir, f"Normalize points to 0 flag: {normalize_points_flag}", save_log_flag)

#log the normalize y axes flag
add_to_log(log_name, main_dir, f"Normalize y axes flag: {normalize_y_axes_flag}", save_log_flag)

#log the normalize y axes prebleach flag
add_to_log(log_name, main_dir, f"Normalize y axes prebleach flag: {normalize_y_axes_prebleach_flag}", save_log_flag)

#log the zoom flag
add_to_log(log_name, main_dir, f"Zoom flag: {zoom_flag}", save_log_flag)

#if it is true
if zoom_flag:

    #if the zs is specified
    if arguments.zs != None:

        #log the zoom start
        add_to_log(log_name, main_dir, f"Zoom start (microns): {zoom_start_length}", save_log_flag)
    
    #if the ze is specified
    if arguments.ze != None:

        #log the zoom end
        add_to_log(log_name, main_dir, f"Zoom end (microns): {zoom_end_length}", save_log_flag)

#log that the file list is being obtained
add_to_log(log_name, main_dir, "Obtaining file list...", save_log_flag)

#get the file list
file_list = [f for f in os.listdir(main_dir) if "average_df_" in f]

#log the file list obtained
add_to_log(log_name, main_dir, f"File list obtained: \n{file_list}",save_log_flag)

#log that you're getting the pickle file
add_to_log(log_name, main_dir, "Getting the pickle file: final_df_dict.pickle", save_log_flag)

#set the pickle file string
pickle_file_string = "final_df_dict.pickle"

#load it using pickle
with open(main_dir + pickle_file_string, "rb") as f:
    
        #load the pickle file
        final_df_dict = pickle.load(f)

#log that the picle file was loaded
add_to_log(log_name, main_dir, "Pickle file loaded", save_log_flag)

#log that the results dictionary is initialized
add_to_log(log_name, main_dir, "Initializing the results dictionary.", save_log_flag)

#start a new dictioary that will hold the results
results_dict = {}

#log that the file list is being looped through
add_to_log(log_name, main_dir, "Looping through the file list to load data frames.", save_log_flag)

#loop through the file list
for file_name in file_list:

    #log that the file is being loaded
    add_to_log(log_name, main_dir, f"Loading file: {file_name}", save_log_flag)

    #get the file name without the extension
    file_name_no_ext = file_name.split(".")[0]

    #get the time point based on the file name without the extension
    time_point = file_name_no_ext.split("_")[-1]

    #log the time point
    add_to_log(log_name, main_dir, f"Time point: {time_point}", save_log_flag)

    #get the data frame into the results dictionary
    results_dict[time_point] = {"data_frame":pd.read_csv(main_dir + file_name)}

    #set the time point name in the object
    results_dict[time_point]["time_point"] = time_point

    #log that the file was loaded
    add_to_log(log_name, main_dir, f"File loaded: {file_name}", save_log_flag)

#log that now you're creating the plots
add_to_log(log_name, main_dir, "Now calculating the points.", save_log_flag)

#get the number of time points
num_time_points = len(results_dict.keys())

#get first time point
first_time_point = list(results_dict.keys())[0]

#get the number of columns in the data frame of the first time point
num_columns = len(results_dict[first_time_point]["data_frame"].columns)

#log the number of time points
add_to_log(log_name, main_dir, f"Number of time points: {num_time_points}", save_log_flag)

#log the number of columns as number of channels
add_to_log(log_name, main_dir, f"Number of channels: {num_columns}", save_log_flag)

#log that you're initializing the plt figure
add_to_log(log_name, main_dir, "Initializing the plt figure.", save_log_flag)

#initialize the plt figure
fig, ax = plt.subplots(nrows=num_time_points, ncols=num_columns*2, figsize=(20, 10))

#log that the figure was initialized
add_to_log(log_name, main_dir, "Figure initialized.", save_log_flag)

#log that you're looping through the time points
add_to_log(log_name, main_dir, "Looping through the time points.", save_log_flag)

#if the zoom flag is true
if zoom_flag:

    #if the zoom_start_length is different to none
    if zoom_start_length != None:

        #now calculate the zoom in pixels
        zoom_start_length_pixel = int(zoom_start_length / pixel_size) 

        #log the zoom start pixel
        add_to_log(log_name, main_dir, f"Zoom start pixel length: {zoom_start_length_pixel}", save_log_flag)

    #if the zoom_end_length is different to none
    if zoom_end_length != None:

        #now calculate the zoom in pixels
        zoom_end_length_pixel = int(zoom_end_length / pixel_size) 

        #log the zoom end pixel
        add_to_log(log_name, main_dir, f"Zoom end pixel length: {zoom_end_length_pixel}", save_log_flag)

#get a time point counter
time_point_counter = 0

#loop through the time points
for time_point in results_dict:
    
    #get the zoom and and start pixels
    zoom_start_pixel = 0
    zoom_end_pixel = 0

    #log the time point
    add_to_log(log_name, main_dir, f"Time point: {time_point}", save_log_flag)

    #add the points object to the time point
    results_dict[time_point]["points"] = {}

    #get the object
    obj = results_dict[time_point]

    #get the co_start and co_end values for this plot
    co_start = final_df_dict[time_point][2][0]
    co_end = final_df_dict[time_point][2][1]

    #log the crossover start and end
    add_to_log(log_name, main_dir, f"Crossover start: {co_start}", save_log_flag)
    add_to_log(log_name, main_dir, f"Crossover end: {co_end}", save_log_flag)

    #get the row index of the first non-nan value in the channel1_norm column
    first_value_index = obj["data_frame"]["channel1_norm"].first_valid_index()

    #get a universal start index
    universal_start_index = first_value_index
           
    #if the left segment start specified flag is true and it is not the zoom 
    if left_segment_start_specified_flag == True:

        #get the number of pixels based on the pixel size and the left segment start
        left_num_pixels = int(left_segment_start/pixel_size)

        #log the left num pixels
        add_to_log(log_name, main_dir, f"Left num pixels: {left_num_pixels}", save_log_flag)

        #get the substraction
        substraction_start_minus_left = co_start - left_num_pixels

        #if the substraction is more or equal to the first value index
        if substraction_start_minus_left >= first_value_index:

            #set the first_value_index by substracting the left_num_pixels from the co_start
            first_value_index = substraction_start_minus_left

            #log that the first value index was changed
            add_to_log(log_name, main_dir, f"First value index was changed to {first_value_index} because of the left segment start.", save_log_flag)
        
        #if the substraction is less than the first value index
        else:

            #log that the first value index was not changed
            add_to_log(log_name, main_dir, f"First value index was not changed because the left segment start is too big.", save_log_flag)

    #log the first value index
    add_to_log(log_name, main_dir, f"First value index: {first_value_index}", save_log_flag)

    #if the zoom flag is true, calculate the zoom start pixel data
    if zoom_start_length != None:

        #if the crossover start minus zoom start pixels is less than the first value index
        if co_start - zoom_start_length_pixel < first_value_index:

            #set the substraction
            substraction = co_start - zoom_start_length_pixel

            #set the zoom_start_length_pixel to the first value index
            zoom_start_pixel = first_value_index

            #log that the zoom start pixel was changed to the first value index
            add_to_log(log_name, main_dir, f"Zoom start pixel was changed to the first value index ({zoom_start_pixel}) because it was too long for the data frame.", save_log_flag)

            #add to the logs of the substraction and the first value index
            add_to_log(log_name, main_dir, f"Zoom starting pixel was {substraction} but the first value index was {first_value_index}", save_log_flag)
        
        #if the crossover start minus zoom start pixels is more or equal to the first value index
        else:

            #set the zoom_start_pixel to the substraction
            zoom_start_pixel = co_start - zoom_start_length_pixel

            #log that the zoom start pixel was set
            add_to_log(log_name, main_dir, f"Zoom start pixel was set to {zoom_start_pixel}.", save_log_flag)
    
    #if zoom flag and arguments.zs is none
    if zoom_flag and arguments.zs == None:

        #set the zoom start pixel to the first value index
        zoom_start_pixel = first_value_index

        #log that the zoom start pixel was changed to the first value index as it was not specified by the user
        add_to_log(log_name, main_dir, f"Zoom start pixel was changed to the first value index ({zoom_start_pixel}) as it was not specified by the user.", save_log_flag)

    #get the row index of the last non-nan value in the channel1_norm column
    last_value_index = obj["data_frame"]["channel1_norm"].last_valid_index()

    #get a universal end index
    universal_end_index = last_value_index

    #if it is true
    if right_segment_end_specified_flag == True:

        #get the number of pixels based on the pixel size and the right segment end
        right_num_pixels = int(right_segment_end/pixel_size)

        #log the right num pixels
        add_to_log(log_name, main_dir, f"Right num pixels: {right_num_pixels}", save_log_flag)

        #get the last_value_index by adding the right_num_pixels to the co_end
        sumatory_end_plus_right_pixels = co_end + right_num_pixels

        #if the sumatory_end_plus_right_pixels is smaller or equal than the last_value_index
        if sumatory_end_plus_right_pixels <= last_value_index:

            #set the last_value_index to the sumatory_end_plus_right_pixels
            last_value_index = sumatory_end_plus_right_pixels

            #log that the last value index was changed
            add_to_log(log_name, main_dir, f"Last value index was changed to {last_value_index} because of the right segment end.", save_log_flag)
        
        #if the sumatory_end_plus_right_pixels is more than the last_value_index
        else:

            #log that the last value index was not changed
            add_to_log(log_name, main_dir, f"Last value index was not changed because the right segment end is too big.", save_log_flag)

    #log the last value index
    add_to_log(log_name, main_dir, f"Last value index: {last_value_index}", save_log_flag)

    #if there's a zoom end length
    if zoom_end_length != None:

        #if the zoom end length pixel plus co end is more than the last value index
        if zoom_end_length_pixel + co_end > last_value_index:

            #set the sum of the ends
            sum_of_ends = zoom_end_length_pixel + co_end

            #set the zoom end length pixel to the last value index minus the co end
            zoom_end_length_pixel = last_value_index - co_end

            #log that the zoom end length pixel was changed
            add_to_log(log_name, main_dir, f"Zoom end length pixel was changed to {zoom_end_length_pixel} because it was too long for the data frame.", save_log_flag)

            #log the previous zoom end length pixel
            add_to_log(log_name, main_dir, f"Previous zoom end length pixel was {sum_of_ends}", save_log_flag)

            #set the zoom end pixel
            zoom_end_pixel = last_value_index

            #log the zoom end pixel
            add_to_log(log_name, main_dir, f"Zoom end pixel: {zoom_end_pixel}", save_log_flag)
        
        #if the zoom end length pixel plus co end is less or equal than the last value index
        else:

            #set the zoom end pixel
            zoom_end_pixel = zoom_end_length_pixel + co_end

            #log the zoom end pixel
            add_to_log(log_name, main_dir, f"Zoom end pixel: {zoom_end_pixel}", save_log_flag)

    #if there's a zoom flag and the zoom end is not specified
    if zoom_flag == True and arguments.ze == None:

        #set the zoom end to the last value index
        zoom_end_length_pixel = last_value_index - co_end

        #get it in microns
        zoom_end_length = zoom_end_length_pixel * pixel_size

        #log that the zoom end pixel was changed to the last value index as it was not specified by the user
        add_to_log(log_name, main_dir, f"Zoom end pixel length was changed to ({zoom_end_length_pixel}) as it was not specified by the user. This is the same as the zoom end pixel length: {zoom_end_length_pixel}", save_log_flag)

        #set the zoom end pixel to the last value index
        zoom_end_pixel = last_value_index

        #log that the zoom end pixel was changed to the last value index
        add_to_log(log_name, main_dir, f"Zoom end pixel was changed to the last value index ({zoom_end_pixel}) because it was not specified by the user.", save_log_flag)
    
    #get the zoom difference start and end
    zoom_difference_start = zoom_start_pixel - first_value_index

    #log the zoom difference start
    add_to_log(log_name, main_dir, f"Zoom difference start: {zoom_difference_start}", save_log_flag)

    #get the zoom difference end
    zoom_difference_end = zoom_end_pixel - first_value_index

    #log the zoom difference end
    add_to_log(log_name, main_dir, f"Zoom difference end: {zoom_difference_end}", save_log_flag)

    #get the number of valid rows by substracting the last value index from the first value index
    num_valid_rows = (last_value_index - first_value_index) + 1

    #log the number of valid rows
    add_to_log(log_name, main_dir, f"Number of valid rows: {num_valid_rows}", save_log_flag)  

    #get the length of the new plot
    new_plot_length = num_valid_rows - 1

    #log the new plot length
    add_to_log(log_name, main_dir, f"New plot length: {new_plot_length}", save_log_flag)

    #calculate the new co_start and co_end values based on the valid rows
    new_co_start = co_start - first_value_index
    new_co_end = co_end - first_value_index

    #if the zoom is true
    if zoom_flag == True:

        #calculate the new co_start and co_end values based on the zoom pixels
        new_co_start = co_start - zoom_start_pixel
        new_co_end = co_end - zoom_start_pixel

    #add them to the results_dict
    results_dict[time_point]["co_start"] = new_co_start
    results_dict[time_point]["co_end"] = new_co_end

    #log the new co_start and co_end values
    add_to_log(log_name, main_dir, f"New co_start: {new_co_start}", save_log_flag)
    add_to_log(log_name, main_dir, f"New co_end: {new_co_end}", save_log_flag)

    #get a channel counter
    channel_counter = 0

    #log that you're looping through the channels
    add_to_log(log_name, main_dir, "Looping through the channels.", save_log_flag)

    #loop through the channels
    for channel in obj["data_frame"].columns:

        #add the channel to the results_dict
        results_dict[time_point]["points"][channel] = {}

        #get the channel name without _norm
        channel_name = channel.split("_")[0]

        #log the channel name
        add_to_log(log_name, main_dir, f"Channel name: {channel_name}", save_log_flag)

        #if the channel name is channel1
        if channel_name == "channel1":

            #get the average intensity before the co_start
            avg_intensity_before = obj["data_frame"][channel][0:co_start].mean()

            #replace the values between the co_start and co_end with the average intensity before
            obj["data_frame"][channel][co_start:co_end] = avg_intensity_before

            #log that the crossover values will be ignored and replaced with the average intensity before the co
            add_to_log(log_name, main_dir, f"Crossover values will be ignored and replaced with the average intensity before the co.", save_log_flag)

        #log that the point list is being initialized
        add_to_log(log_name, main_dir, "Initializing the point list.", save_log_flag)

        #initialize the point list
        plotting_points = []

        #log that you're looping through the new plot length
        add_to_log(log_name, main_dir, "Looping through the new plot length and calculating the average differences.", save_log_flag)
  
        #loop through the new plot length
        for i in range(0, new_plot_length):
            
            #get the average of the left

            #if the plot type is segment
            if plot_type == "segment":

                #get the average of the left
                left_avg = obj["data_frame"][channel][first_value_index:first_value_index+i].mean()

                #if the first value index and first value index + i are the same
                if first_value_index == first_value_index+i:

                    #set the left average to the value at the first value index
                    left_avg = obj["data_frame"][channel][first_value_index]

            #if the plot type is crawl
            if plot_type == "crawl":

                #get the start pixel of the crawl iteration
                current_crawl_start_first_pixel = (first_value_index + i) - crawl_left_length_pixels

                #if the current crawl start first pixel is less than the universal first value index
                if current_crawl_start_first_pixel < universal_start_index:

                    #set the current crawl start first pixel to the universal first value index
                    current_crawl_start_first_pixel = universal_start_index

                #get the average of the left
                left_avg = obj["data_frame"][channel][current_crawl_start_first_pixel:first_value_index+i].mean()

                #if the current crawl start first pixel and first value index + i are the same
                if current_crawl_start_first_pixel == first_value_index+i:

                    #set the left average to the value at the first value index
                    left_avg = obj["data_frame"][channel][current_crawl_start_first_pixel]    

            #get the average of the right
            
            #if the plot type is segment
            if plot_type == "segment":
                
                #get the average
                right_avg = obj["data_frame"][channel][first_value_index+i+1:last_value_index].mean()

                #if the first value index + i + 1 and last value index are the same
                if first_value_index+i+1 == last_value_index:

                    #set the right average to the value at the last value index
                    right_avg = obj["data_frame"][channel][last_value_index]
            
            #if the plot type is crawl
            if plot_type == "crawl":

                #get the end pixel of the crawl iteration
                current_crawl_end_last_pixel = (first_value_index + i + 1) + crawl_right_length_pixels

                #if the current crawl end last pixel is greater than the universal last value index
                if current_crawl_end_last_pixel > universal_end_index:

                    #set the current crawl end last pixel to the universal last value index
                    current_crawl_end_last_pixel = universal_end_index
                
                #get the average to the right
                right_avg = obj["data_frame"][channel][first_value_index+i+1:current_crawl_end_last_pixel].mean()

                #if the first value index + i + 1 and current crawl end last pixel are the same
                if first_value_index+i+1 == current_crawl_end_last_pixel:

                    #set the right average to the value at the first value index
                    right_avg = obj["data_frame"][channel][first_value_index+i+1]

            #get the differences

            #if the use absolute value flag is true
            if use_absolutes_flag == True:

                #set the adding value to the absolute value of the difference between the left and right averages
                adding_value = abs(left_avg - right_avg)
            
            #if it is false
            if use_absolutes_flag == False:

                #set the adding value to the difference between the left and right averages
                adding_value = left_avg - right_avg

            #add the difference to the point list
            plotting_points.append(adding_value)

        #if the zoom flag is true
        if zoom_flag == True:

            #log that you're zooming in
            add_to_log(log_name, main_dir, "Zooming the plot.", save_log_flag)

            #get the zoom start index
            plotting_points = plotting_points[zoom_difference_start:zoom_difference_end]           

        #if the normalize points flag is true
        if normalize_points_flag == True:

            #log that you're normalizing to 0
            add_to_log(log_name, main_dir, "Getting the min value.", save_log_flag)

            #get the minimum value of the plotting points that are not nan
            min_value = min(plotting_points)

            #log the mean value
            add_to_log(log_name, main_dir, f"Min value: {min_value}", save_log_flag)

            #if the min value is less than 0
            if min_value < 0:

                #log that you're normalizing to 0
                add_to_log(log_name, main_dir, "Normalizing points to 0 in the y axis.", save_log_flag)

                #add the min value to all the points
                plotting_points = [x + abs(min_value) for x in plotting_points]
        
        #add the plotting points to the results dict
        results_dict[time_point]["points"][channel]["plotting_points"] = plotting_points        

        #log that the resutls were added to the results dict
        add_to_log(log_name, main_dir, "Points were added to the results dict.", save_log_flag)

        #log that you're creating the flat data frame
        add_to_log(log_name, main_dir, "Creating the flattened dataframe.", save_log_flag)

        #get the average before the crossover end
        avg_before = obj["data_frame"][channel][0:co_end].mean()

        #log the average before
        add_to_log(log_name, main_dir, f"Average before crossover: {avg_before}", save_log_flag)

        #get the average after the crossover end
        avg_after = obj["data_frame"][channel][co_end+1:].mean()

        #log the average after
        add_to_log(log_name, main_dir, f"Average after crossover: {avg_after}", save_log_flag)

        #get a new perfect data frame with the same number of rows set to the valid rows
        flat_df = pd.DataFrame(np.nan, index=range(0,len(obj["data_frame"])), columns=[channel])

        #log that the data frame was created
        add_to_log(log_name, main_dir, "Data frame created.", save_log_flag)

        #set the values before the crossover end to the average before
        flat_df[channel][0:co_end] = avg_before

        #set the values after the crossover end to the average after
        flat_df[channel][co_end+1:] = avg_after

        #log that the values were populated
        add_to_log(log_name, main_dir, "Values populated.", save_log_flag)

        #log that you're calculating the points for the flattened data frame
        add_to_log(log_name, main_dir, "Calculating the points for the flattened plot.", save_log_flag)

        #initialize the point list
        flat_plotting_points = []

        #loop through the new plot length
        for i in range(0, new_plot_length):

            #if the type is segment
            if plot_type == "segment":

                #get the average of the left
                left_avg = flat_df[channel][first_value_index:first_value_index+i].mean()

                #if the first value index and first value index + i are the same
                if first_value_index == first_value_index+i:

                    #set the left average to the value at the first value index
                    left_avg = flat_df[channel][first_value_index]
            
            #if the type is crawl
            if plot_type == "crawl":

                #get the start pixel of the crawl iteration
                current_crawl_start_first_pixel = (first_value_index + i) - crawl_left_length_pixels

                #if the current crawl start first pixel is less than the universal first value index
                if current_crawl_start_first_pixel < universal_start_index:

                    #set the current crawl start first pixel to the universal first value index
                    current_crawl_start_first_pixel = universal_start_index

                #get the average of the left
                left_avg = flat_df[channel][current_crawl_start_first_pixel:first_value_index+i].mean()

                #if the current crawl start first pixel and first value index + i are the same
                if current_crawl_start_first_pixel == first_value_index+i:

                    #set the left average to the value at the first value index
                    left_avg = flat_df[channel][first_value_index]
            
            #get the average of the right

            #if the type is segment
            if plot_type == "segment":
                
                #get the average of the right
                right_avg = flat_df[channel][first_value_index+i+1:last_value_index].mean()

                #if the first value index + i + 1 and last value index are the same
                if first_value_index+i+1 == last_value_index:

                    #set the right average to the value at the last value index
                    right_avg = flat_df[channel][last_value_index]

            #if the type is crawl
            if plot_type == "crawl":

                #get the end pixel of the crawl iteration
                current_crawl_end_last_pixel = (first_value_index + i + 1) + crawl_right_length_pixels

                #if the current crawl end last pixel is greater than the universal last value index
                if current_crawl_end_last_pixel > universal_end_index:

                    #set the current crawl end last pixel to the universal last value index
                    current_crawl_end_last_pixel = universal_end_index
                
                #get the average to the right
                right_avg = flat_df[channel][first_value_index+i+1:current_crawl_end_last_pixel].mean()

                #if the first value index + i + 1 and current crawl end last pixel are the same
                if first_value_index+i+1 == current_crawl_end_last_pixel:

                    #set the right average to the value at the first value index
                    right_avg = flat_df[channel][first_value_index+i+1]

            #get the differences

            #if the use absolute value flag is true
            if use_absolutes_flag == True:

                #get the absolute value of the difference
                adding_value = abs(left_avg - right_avg)
            
            #if it is false
            if use_absolutes_flag == False:

                #get the difference
                adding_value = left_avg - right_avg

            #add the difference to the point list
            flat_plotting_points.append(adding_value)
        
        #if the zoom flag is true
        if zoom_flag == True:

            #log that you're zooming in
            add_to_log(log_name, main_dir, "Zooming the plot.", save_log_flag)

            #get the zoom start index
            flat_plotting_points = flat_plotting_points[zoom_difference_start:zoom_difference_end]           

        #if the normalize points flag is true
        if normalize_points_flag == True:

            #log that you're getting the min
            add_to_log(log_name, main_dir, "Getting the min value.", save_log_flag)

            #get the minimum value of the plotting points that are not nan
            min_value = min(flat_plotting_points)

            #log the min value
            add_to_log(log_name, main_dir, f"Min value: {min_value}", save_log_flag)

            #if the min value is less than 0
            if min_value < 0:

                #log that you're normalizing to 0
                add_to_log(log_name, main_dir, "Normalizing the points to 0.", save_log_flag)

                #add the min value to all the points
                plotting_points = [x + abs(min_value) for x in flat_plotting_points]

        #add the plotting points to the results dict
        results_dict[time_point]["points"][channel]["flat_plotting_points"] = flat_plotting_points

        #log that you're done calculating for the channel
        add_to_log(log_name, main_dir, "Done calculating for the channel: "+str(channel), save_log_flag)

        #add one to the channel counter
        channel_counter += 1
    
    #log that all the channels were plotted
    add_to_log(log_name, main_dir, "All the channels in time point were calculated.", save_log_flag)

    #add one to the time point counter
    time_point_counter += 1

#log that the plots will be created
add_to_log(log_name, main_dir, "Creating the plots.", save_log_flag)

#start a time point counter
time_point_counter = 0

#make a change of limits flag
change_of_limits_flag = False

#if the type is crawl and the auto x flag is enables, get the max x
if plot_type == "crawl" and auto_x_flag == True:

    #add to log that you're calculating the max xs
    add_to_log(log_name, main_dir, "Calculating the max x.", save_log_flag)

    #get a list for the max xs
    max_xs = []

    #get the crawl left length + the crawl right length
    crawl_length_in_pixels = crawl_left_length_pixels + crawl_right_length_pixels

    #get the total lengths for the x in the time points
    for time_point in results_dict:

        #get the current co start
        current_co_start = results_dict[time_point]["co_start"]

        #get the current co end
        current_co_end = results_dict[time_point]["co_end"]

        #get the total length
        total_co_length = current_co_end - current_co_start

        #get the total lenght in pixels
        total_co_length_in_pixels = total_co_length + crawl_length_in_pixels

        #add it to the max xs
        max_xs.append(total_co_length_in_pixels)

    #get the max x
    max_x = max(max_xs)

    #set the low x to 0 and x high to the max x
    x_limits = [0, max_x]   



#loop through the time points
for time_point in results_dict:

    #log that the plots will be created for the time point
    add_to_log(log_name, main_dir, "Creating the plots for the time point: "+str(time_point), save_log_flag)

    #start a channel counter
    channel_counter = 0

    #get the current co start
    current_co_start = results_dict[time_point]["co_start"]

    #get the current co end
    current_co_end = results_dict[time_point]["co_end"]

    #if the normalize y flag is true
    if normalize_y_axes_flag == True:

        #get the max value from all the channels
        max_value = max([max(results_dict[time_point]["points"][channel]["plotting_points"]) for channel in results_dict[time_point]["points"]])

        #get the min value from all the channels
        min_value = min([min(results_dict[time_point]["points"][channel]["plotting_points"]) for channel in results_dict[time_point]["points"]])

        #if the y_limis specified flag is false
        if y_lim_specified_flag == False:

            #set the y_limits[0] to the min value
            y_limits[0] = min_value - (min_value*0.1)

            #set the y_limits[1] to the max value
            y_limits[1] = max_value + (max_value*0.1)
        
    #if the normalize y axes prebleach is true
    if normalize_y_axes_prebleach_flag == True and time_point == "prebleach":

        #get the max value from all the channels of t0min
        max_value = max([max(results_dict["t0min"]["points"][channel]["plotting_points"]) for channel in results_dict["t0min"]["points"]])

        #get the min value from all the channels of t0min
        min_value = min([min(results_dict["t0min"]["points"][channel]["plotting_points"]) for channel in results_dict["t0min"]["points"]])

        #if the y_limis specified flag is false
        if y_lim_specified_flag == False:

            #set the y_limits[0] to the min value
            y_limits[0] = min_value - (min_value*0.1)

            #set the y_limits[1] to the max value
            y_limits[1] = max_value + (max_value*0.1)
    
    #get the custom ticks
    custom_ticks = get_custom_ticks(new_plot_length,0.5,pixel_size)

    #loop through the channels in the time point
    for channel in results_dict[time_point]["points"]:

        #log that the points will be plotted
        add_to_log(log_name, main_dir, "Plotting the points for the channel: "+str(channel), save_log_flag)

        #plot the points
        ax[time_point_counter, (channel_counter*2)].plot(results_dict[time_point]["points"][channel]["plotting_points"], plot_colors[channel_counter], alpha=0.75)

        #add the shade below the function
        ax[time_point_counter, (channel_counter*2)].fill_between(range(len(results_dict[time_point]["points"][channel]["plotting_points"])), results_dict[time_point]["points"][channel]["plotting_points"], color=plot_colors[channel_counter], alpha=0.2)

        #set up the crossover area
        ax[time_point_counter, (channel_counter*2)].axvspan(current_co_start, current_co_end, alpha=0.2, color='green')

        #set the x ticks
        ax[time_point_counter, (channel_counter*2)].set_xticks(custom_ticks[0])

        #set the tick labels 
        ax[time_point_counter, (channel_counter*2)].set_xticklabels(custom_ticks[1])

        #set the x label
        ax[time_point_counter, (channel_counter*2)].set_xlabel("Length (microns)")

        #if the x limit is specified
        if x_lim_specified_flag == True:

            #set the x limits to the x_lim
            ax[time_point_counter, (channel_counter*2)].set_xlim(x_limits[0], x_limits[1])

        #if the auto x limit is true
        if auto_x_flag == True:

            #set the x limits to the x_lim
            ax[time_point_counter, (channel_counter*2)].set_xlim(x_limits[0], x_limits[1])

        #set the y label
        ax[time_point_counter, (channel_counter*2)].set_ylabel("Average difference")

        #if the normalize y axes flag is true
        if normalize_y_axes_flag == True:

            #set the y limits to the y_lim
            ax[time_point_counter, (channel_counter*2)].set_ylim(y_limits[0], y_limits[1])

        #if the normalize y axes prebleach flag is true
        if normalize_y_axes_prebleach_flag == True and time_point == "prebleach":

            #set the y limits to the y_lim
            ax[time_point_counter, (channel_counter*2)].set_ylim(y_limits[0], y_limits[1])

        #if the y limit is specified
        if y_lim_specified_flag == True:

            #set the y limits to the y_lim
            ax[time_point_counter, (channel_counter*2)].set_ylim(y_limits[0], y_limits[1])

        #log that the points were plotted
        add_to_log(log_name, main_dir, "Points were plotted for the channel: "+str(channel), save_log_flag)

        #log that the flattened data will be plotted
        add_to_log(log_name, main_dir, "Plotting the flattened data for the channel: "+str(channel), save_log_flag)

        #plot the flattened data
        ax[time_point_counter, (channel_counter*2)+1].plot(results_dict[time_point]["points"][channel]["flat_plotting_points"], plot_colors[channel_counter], alpha=0.75)

        #add the shade below the function
        ax[time_point_counter, (channel_counter*2)+1].fill_between(range(len(results_dict[time_point]["points"][channel]["flat_plotting_points"])), results_dict[time_point]["points"][channel]["flat_plotting_points"], color=plot_colors[channel_counter], alpha=0.2)

        #set up the crossover area
        ax[time_point_counter, (channel_counter*2)+1].axvspan(current_co_start, current_co_end, alpha=0.2, color='green')

        #set the x ticks
        ax[time_point_counter, (channel_counter*2)+1].set_xticks(custom_ticks[0])

        #set the tick labels
        ax[time_point_counter, (channel_counter*2)+1].set_xticklabels(custom_ticks[1])

        #if the x limit is specified
        if x_lim_specified_flag == True:

            #set the x limits to the x_lim
            ax[time_point_counter, (channel_counter*2)+1].set_xlim(x_limits[0], x_limits[1])

        #if the auto x limit is true
        if auto_x_flag == True:

            #set the x limits to the x_lim
            ax[time_point_counter, (channel_counter*2)+1].set_xlim(x_limits[0], x_limits[1])

        #set the x label
        ax[time_point_counter, (channel_counter*2)+1].set_xlabel("Length (microns)")

        #set the y label
        ax[time_point_counter, (channel_counter*2)+1].set_ylabel("Average difference")

        #if the normalize y axes flag is true
        if normalize_y_axes_flag == True:

            #set the y limits to the y_lim
            ax[time_point_counter, (channel_counter*2)+1].set_ylim(y_limits[0], y_limits[1])

        #if the normalize y axes prebleach flag is true
        if normalize_y_axes_prebleach_flag == True and time_point == "prebleach":

            #set the y limits to the y_lim
            ax[time_point_counter, (channel_counter*2)+1].set_ylim(y_limits[0], y_limits[1])

        #if the y limit is specified
        if y_lim_specified_flag == True:

            #set the y limits to the y_lim
            ax[time_point_counter, (channel_counter*2)+1].set_ylim(y_limits[0], y_limits[1])

        #log that the flattened data was plotted
        add_to_log(log_name, main_dir, "Flattened data was plotted for the channel: "+str(channel), save_log_flag)

        #increment the channel counter
        channel_counter += 1
    
    #increment the time point counter
    time_point_counter += 1

#get the save file
save_file = main_dir+"c069_differences_plot_ls"+str(arguments.ls)+"_re"+str(arguments.re)+"_cll"+str(arguments.cll)+"_crl"+str(arguments.crl)+"_absolute"+str(use_absolutes_flag)+".pdf"

#save as pdf
plt.savefig(save_file, dpi=300)
   
#endregion ////////////////////// END MAIN  //////////////////////


