#region ###################################### DESCRIPTION ##########################################

"""

This script will look for the "_avg_proj.tif" files and create the normalized data frames, saving the combined
profiles as .csv files.

It will also create the plots of the profiles for each channel and save them as png and pdf files.

"""

#endregion ################################### END OF DESCRIPTION ###################################



import datetime
from math import ceil
import os
import pickle
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

#set the pixel size
pixel_size = 0.042598146

#set the x axis step size
step_size = 0.2

#set an array to hold the colors
plot_colors = ["royalblue", "blueviolet", "m", "y", "c", "m", "k"]

#get the colors for the chromsome lines
chromosome_line_colors = []

#get the name only without the parent directories
script_name = script_name.split("/")[-1]

#set the functions for the log
#the function to start the log
def start_log(script_name, main_dir):
    
    return
    
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

    return

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

    return

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

#the function to get the color list for the chromosomes
#get a functoon the generate the color gradients
def getColorList(number_of_objects):

    #get the color list
    returning_color_list = []

    #divide the number of colors by 3
    number_of_colors_per_section = int(number_of_objects / 3)

    #set the for the number of sections and the color of sections per list
    sections = [number_of_colors_per_section]*3

    #find out if there's a residual
    residual = number_of_objects % 3

    #if there's a residual, add it to the first section
    if residual > 0:

        #get the flag of no residual
        no_residual = False

        #residual counter
        residual_counter = 0

        #set up a while loop
        while no_residual == False:

            #add one to the sections list at the residual counter
            sections[residual_counter] += 1

            #sum all the sections
            sum_of_sections = sum(sections)

            #if the sum of the sections is equal to the number of objects
            if sum_of_sections == number_of_objects:

                #set the flag to true
                no_residual = True

            #add one to the residual counter
            residual_counter += 1

    #get the counter
    color_counter = 0
    
    #loop through the sections
    for a in range(3):

        #reset the current color
        current_color = [0, 0, 0]

        #get the number of times you have to generate a color
        number_of_times = sections[a]

        #get the step
        step = 1 / (number_of_times)

        #loop through the number of times
        for b in range(number_of_times):

            #if the counter is 0
            if color_counter == 0:

                #set all the other colors to 0
                for c in range(3):

                    #if the a is not c
                    if a != c:

                        #set the color to 0
                        current_color[c] = 0

                    #if the color counter is equal to b
                    else:

                        #set the color to 1
                        current_color[c] = 1

            #if the color counter is more than 0
            else:

                #subtract the step from the current color
                current_color[a] -= step

                #if the a is less than 2
                if a < 2:

                    #add the step to the next color
                    current_color[a+1] += step
                 
            #add the current color list to the returning color list as a tuple
            returning_color_list.append(tuple(current_color))

            #add one to the color counter
            color_counter += 1

        #reset the color counter
        color_counter = 0

    #return the list
    return returning_color_list

#function to get the time point
def get_time_point(file_name):

    #split the file name by _gonad
    after_gonad = file_name.split("_gonad")[1]

    #get the index of the first undersoce
    first_underscore_index = after_gonad.index("_")

    #get after the first underscore
    after_gonad = after_gonad[first_underscore_index+1:]

    #get the index of the second underscore
    second_underscore_index = after_gonad.index("_")

    #get the time point
    time_point = after_gonad[:second_underscore_index]

    return time_point

#the function to get the base name
def get_base_name_and_time_point(file_name):

    #get the index of _gonad
    gonad_split_string = file_name.split("_gonad")

    #add _gonad to the first part
    gonad_split_string[0] = gonad_split_string[0] + "_gonad"

    #get the before gonad string
    before_gonad_string = gonad_split_string[0]

    #get the after gonad string
    after_gonad_string = gonad_split_string[1]

    #get the index of _
    underscore_gonad_index = after_gonad_string.find("_")

    #get the gonad number
    gonad_number = after_gonad_string[:underscore_gonad_index]

    #get the string after underscore
    after_gonad_underscore_string = after_gonad_string[underscore_gonad_index+1:]

    #get the index of _
    time_underscore_index = after_gonad_underscore_string.find("_")

    #get the time poitn
    time_point = after_gonad_underscore_string[:time_underscore_index]

    #get after time underscore index string
    after_time_underscore_index_string = after_gonad_underscore_string[time_underscore_index+1:]

    #get the index of _sbs
    sbs_index = after_time_underscore_index_string.find("_sbs")

    #get after sbs index
    after_sbs_index_string = after_time_underscore_index_string[sbs_index+4:]
    
    #get the sbs underscore index
    sbs_underscore_index = after_sbs_index_string.find("_")

    #get the sbs number
    sbs_number = after_sbs_index_string[:sbs_underscore_index]

    #get the _chr index
    chr_index = after_sbs_index_string.find("_chr")

    #get the after chr index string
    after_chr_index_string = after_sbs_index_string[chr_index+4:]

    #get the chr underscore index
    chr_underscore_index = after_chr_index_string.find("_")

    #get the chr number
    chr_number = after_chr_index_string[:chr_underscore_index]  

    #get the base name
    base_name = before_gonad_string + gonad_number + "_sbs" + sbs_number + "_chr" + chr_number

    #make a new string[] for the base name and time point
    base_name_and_time_point = [base_name, time_point]

    return base_name_and_time_point

#the function to get the time point list order
def get_time_point_list_order(time_point_list):

    #get the time point list order
    time_point_list_order = []

    #make a list without letters
    no_letter_list = []

    #flag for time list
    list_of_flags = []

    #make a to take out list
    to_take_out_list = []

    #set a counter for the time point
    times_ordering_counter = 0

    #go through each time point
    for time_point in time_point_list:

        #get only the numeric characters from the time point string
        no_letter_time_point = ""

        #go through each character in the time point
        for character in time_point:

            #if the character is a number
            if character.isnumeric():

                #add the character to the no letter time point
                no_letter_time_point = no_letter_time_point + character

        #if the no letter time point is ""
        if no_letter_time_point == "":

            #set it to an "a"
            no_letter_time_point = time_point

            #add a 1 to the list of flags
            list_of_flags.append(times_ordering_counter)

            #add the time point to the to take out list
            to_take_out_list.append(times_ordering_counter)

            #add 1 to the times ordering counter
            times_ordering_counter = times_ordering_counter + 1
        
        #if the no letter time point is not ""
        else:

            #add a 0 to the list of flags
            list_of_flags.append(times_ordering_counter)

            #add 1 to the times ordering counter
            times_ordering_counter = times_ordering_counter + 1

        #add the no letter time point to the no letter list
        no_letter_list.append(no_letter_time_point)
        
    #get a list for the a's
    a_list = []

    #get a list for the b's
    b_list = []

    #get a c_list
    actual_time_list = []

    #loop through the list of flags
    for flag in list_of_flags:

        #if the flag is in the to take out list
        if flag in to_take_out_list:

            #add the corresponding time point to the a list
            a_list.append(time_point_list[list_of_flags.index(flag)])
        
        #if the flag is not in the to take out list
        else:

            #add the corresponding no letter list as an int to the b list
            b_list.append(int(no_letter_list[list_of_flags.index(flag)]))

            #add the corresponding time point to the actual time list
            actual_time_list.append(time_point_list[list_of_flags.index(flag)])
        
    #sort the a list
    a_list.sort()

    #sort the actual time list based on the b list
    actual_time_list_order = [x for _,x in sorted(zip(b_list, actual_time_list))]

    #join the actual time list order and the a list in the time point list order
    time_point_list_order = a_list + actual_time_list_order

    return time_point_list_order

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

np.set_printoptions(precision=4, suppress=True)

#get the path to the file
root = tk.Tk()
root.withdraw()

#get a directory using tkinter and set the starting directory
main_dir = filedialog.askdirectory() + "/"

#start the log
log_name = start_log(script_name, main_dir)

#log an empty space
add_to_log(log_name, main_dir, "")

#log the main directory
add_to_log(log_name, main_dir, "Main directory selected: " + main_dir)

#get the results directory
results_dir = main_dir + "results/"

#if the results directory does not exist, create it
if not os.path.exists(results_dir):

    #create the results directory
    os.mkdir(results_dir)

    #log the results directory creation
    add_to_log(log_name, main_dir, "Results directory created: " + results_dir)

#get all the pdf files in the directory
file_list = [f for f in os.listdir(main_dir) if f.endswith("profile.csv")]

#log that the file list is obtained
add_to_log(log_name, main_dir, "File list obtained")

#log an empty space
add_to_log(log_name, main_dir, "")

#make the time point list
time_point_list = []

#get the number of columns list
columns_list = []

#get the df dictionary {time_point:[file_name,df, co_parameter_list, side_length_list], [file_name2 ,df2 , co_parameter_list2 , side_length_list2], ...}
df_dict = {}

#get the max length
max_right_length = 0
max_left_length = 0

#loop through the file list
for file_name in file_list:

    #create a list to pass variables later
    pass_list = []

    #log which file is being processed
    add_to_log(log_name, main_dir, "Processing file: " + file_name)

    #get the time point
    time_point = get_time_point(file_name)

    #log the time point
    add_to_log(log_name, main_dir, "Time point: " + str(time_point)) 

    #log that the file will be read
    add_to_log(log_name, main_dir, "Reading file: " + file_name + " to pandas data frame.")

    #read the csv file
    df = pd.read_csv(main_dir + file_name)

    #log that the file is read
    add_to_log(log_name, main_dir, "File: " + file_name + " read to pandas data frame.")

    #get the number of rows in the data frame
    num_rows = len(df)

    #log the number of rows
    add_to_log(log_name, main_dir, "Dataframe number of rows: " + str(num_rows))

    #get the crossover parameters
    current_co_mid = df["co_mid"][0]

    current_co_start = df["co_start"][0]

    current_co_end = df["co_end"][0]

    #get the column list from the data frame
    current_columns = list(df.columns)

    #get rid of the co_mid in the list
    current_columns.remove("co_mid")

    #get rid of the co_start in the list
    current_columns.remove("co_start")

    #get rid of the co_end in the list
    current_columns.remove("co_end")

    #get the number of columns
    num_columns = len(current_columns)

    #if the time point is not on the list, add it
    if time_point not in time_point_list:

        #add the time point to the dictionary
        df_dict[time_point] = []

        #add the time point to the list
        time_point_list.append(time_point)

        #add the current columns to the columns list
        columns_list.append(current_columns)
    
    #log that you're getting the normalized channel
    add_to_log(log_name, main_dir, "Getting the normalized channels.")

    #get a flag to know if there's a prebleach string in the file name
    prebleach_flag = "prebleach" in file_name

    #loop through the current_columns
    for column in current_columns:

        #log the channel you're working on
        add_to_log(log_name, main_dir, "Working on channel: " + column)

        #get the mean of the channel
        channel_mean = df[column].mean()

        #log that you have obtained the channel mean and the value
        add_to_log(log_name, main_dir, "Channel mean obtained: " + str(channel_mean))

        #if the time point is prebleach
        if prebleach_flag:

            #log that it is a prebleach flag
            add_to_log(log_name, main_dir, "Prebleach file detected, obtaining the t0min file.")

            #get the base name
            prebleach_base_name = get_base_name_and_time_point(file_name)[0]

            #get the normalized to string
            normalized_to_string = file_name

            #loop through the files in the directory
            for file in os.listdir(main_dir):

                #if there's t0min in the file name
                if "t0min" in file and ".csv" in file:

                    #get the file base name
                    current_looping_file_base_name = get_base_name_and_time_point(file)[0]

                    #if the current looping file base name and the prebleach base name are the same
                    if current_looping_file_base_name == prebleach_base_name:

                        #log that you have found the t0min file
                        add_to_log(log_name, main_dir, "t0min file found: " + file)

                        #get the t0min df
                        t0min_df = pd.read_csv(main_dir + file)

                        #log that you have read the t0min file
                        add_to_log(log_name, main_dir, "t0min file read to pandas data frame.")

                        #get the t0min channel mean
                        channel_mean = t0min_df[column].mean()

                        #log the mean of the t0min channel
                        add_to_log(log_name, main_dir, "t0min channel mean obtained: " + str(channel_mean))

                        #get the normalized to string
                        normalized_to_string = file
        
        #log that you're normalizing the channel
        add_to_log(log_name, main_dir, "Normalizing channel: " + column + "from file: " + file_name + " with channel mean: " + str(channel_mean) + "of file: " + normalized_to_string)

        #get the normalized string
        norm_string = column + "_norm"

        #normalize the channel
        df[norm_string] = df[column] / channel_mean

        #log that you have normalized the channel
        add_to_log(log_name, main_dir, "Channel: " + column + " normalized and added to data frame column: " + norm_string)

    #log that the columns have been normalized
    add_to_log(log_name, main_dir, "All columns normalized.")     

    #log the crossover parameters
    add_to_log(log_name, main_dir, "Crossover mid: " + str(current_co_mid) + " Crossover start: " + str(current_co_start) + " Crossover end:" + str(current_co_end))

    #get a list for the crossover parameters
    co_parameter_list = {"co_parameters":[current_co_mid, current_co_start, current_co_end]}

    #get the left side length
    left_side_length = current_co_mid

    #log the left side of the chromosome value
    add_to_log(log_name, main_dir, "Left side of the chromosome length: " + str(left_side_length))

    #if the left side length is greater than the max left length, set the max left length to the left side length
    if left_side_length > max_left_length:

        #set the max left length to the left side length
        max_left_length = left_side_length

        #log that the new max is found
        add_to_log(log_name, main_dir, "New max left length found: " + str(max_left_length))

    #get the right side length
    right_side_length = num_rows - current_co_mid

    #log the right side of the chromosome value
    add_to_log(log_name, main_dir, "Right side of the chromosome length: " + str(right_side_length))

    #if the right side length is greater than the max right length, set the max right length to the right side length
    if right_side_length > max_right_length:

        #set the max right length to the right side length
        max_right_length = right_side_length

        #log that the new max is found
        add_to_log(log_name, main_dir, "New max right length found: " + str(max_right_length))

    #get the into a list
    side_length_list = {"side_lengths":[left_side_length, right_side_length]}

    #get the list of adding
    adding_list = [file_name,df, co_parameter_list, side_length_list]

    #log that you're adding the parameters to the dictionary
    add_to_log(log_name, main_dir, "Adding df, co parameters and length to the df dictionary dictionary.")

    #add all parameters into the dictionary
    df_dict[time_point].append(adding_list)

    #log that the parameters are added to the dictionary
    add_to_log(log_name, main_dir, "Parameters added to the df dictionary dictionary.")

    #log an empty space
    add_to_log(log_name, main_dir, "")

#log that you're getting the time point list order
add_to_log(log_name, main_dir, "Getting the time point list order for the time points: " + str(time_point_list))

#get a time point list order
time_point_list_order = get_time_point_list_order(time_point_list)

#log the obtained time point list order
add_to_log(log_name, main_dir, "Time point list order: " + str(time_point_list_order))

#log that the dictionary is created
add_to_log(log_name, main_dir, "Dictionary completed.")

#get the max length
max_length = max_right_length + max_left_length

#log the new max length
add_to_log(log_name, main_dir, "New max length: " + str(max_length))

#get the micon length
micron_length = max_length * pixel_size

#log the micron length
add_to_log(log_name, main_dir, "Micron length: " + str(micron_length))

#get the axes
custom_ticks = get_custom_ticks(max_length, step_size, pixel_size)

#log the custom ticks
add_to_log(log_name, main_dir, "Custom ticks for x axis of plots: " + str(custom_ticks))

#log that the extended dataframes will be created
add_to_log(log_name, main_dir, "Creating extended dataframes.")

#start a time point counter
time_point_counter = 0

#get the number of time points
num_time_points = len(time_point_list)

#log the number of time points
add_to_log(log_name, main_dir, "Number of time points: " + str(num_time_points))

#log the actual time points
add_to_log(log_name, main_dir, "Time points: " + str(time_point_list))

#log that you're looping though the dictionary time points
add_to_log(log_name, main_dir, "Looping through the time points.")

#create the dictionary with the final scaled data frames
final_df_dict = {}

#loop through the time points
for time_point in time_point_list:

    #add it to the final dictionary
    final_df_dict[time_point] = "final_scaled_dataframe"

#loop through the time points
for time_point in time_point_list:

    #make an entry on the final df dictionary
    final_df_dict[time_point] = [[],""]

    #get the index of the time point
    time_point_index = time_point_list.index(time_point)

    #get the current columns
    current_columns = columns_list[time_point_index]

    #get the number of columns
    column_number = len(current_columns)

    #create a list for the co_start_lists
    current_co_start_list = []

    #create a list for the co_end_lists
    current_co_end_list = []

    #log that you're processing the time point
    add_to_log(log_name, main_dir, "Processing time point: " + str(time_point))

    #add the columns at time point
    add_to_log(log_name, main_dir, "Dataframe columns at time point: " + str(current_columns))

    #log an empty space
    add_to_log(log_name, main_dir, "")

    #loop through the list of the dictionary at the time point
    for element in df_dict[time_point]:

        #Log the file you're working on
        add_to_log(log_name, main_dir, "Working on file: " + str(element[0]))

        #get the dataframe
        df = element[1]

        #get the co_mid
        co_mid = element[2]["co_parameters"][0]

        #get the co_start
        co_start = element[2]["co_parameters"][1]

        #get the co_end
        co_end = element[2]["co_parameters"][2]

        #get the left side length
        left_side_length = element[3]["side_lengths"][0]

        #get the right side length
        right_side_length = element[3]["side_lengths"][1]       

        #get the left side difference
        left_side_difference = max_left_length - left_side_length

        #get the right side difference
        right_side_difference = max_right_length - right_side_length

        #get the new_co_mid
        new_co_mid = co_mid + left_side_difference

        #get the new_co_start
        new_co_start = co_start + left_side_difference

        #add it to the current_co_start list
        current_co_start_list.append(new_co_start)

        #get the new_co_end
        new_co_end = co_end + left_side_difference

        #add it to the current_co_end list
        current_co_end_list.append(new_co_end)

        #log the new co parameters
        add_to_log(log_name, main_dir, "New co parameters: co_mid = " + str(new_co_mid) + ", co_start = " + str(new_co_start) + ", co_end = " + str(new_co_end))

        #log that you're creating the scaled dataframe
        add_to_log(log_name, main_dir, "Creating the scaled dataframe.")

        #create the scaled dataframe with the columns of the df and the max length as rows
        scaled_df = pd.DataFrame(index=range(max_length), columns=df.columns)

        #log that you're filling the scaled dataframe
        add_to_log(log_name, main_dir, "Filling the scaled dataframe.")

        #get the columns of the original data frame into a list
        df_columns = list(df.columns)

        #loop through the number of rows of the original dataframe
        for a in range(len(df)):
            
            #loop through the columns of the data frame
            for b in range(len(df_columns)):

                #set the value of the scaled dataframe
                scaled_df[df_columns[b]][a + left_side_difference] = df[df_columns[b]][a]

        #log that the scaling is done
        add_to_log(log_name, main_dir, "Scaling done.")

        #log that you're adding it to the final df dictionary
        add_to_log(log_name, main_dir, "Adding the scaled dataframe to the final df dictionary.")

        #add the scaled dataframe to the final df dictionary
        final_df_dict[time_point][0].append(scaled_df)

        #log an empty space
        add_to_log(log_name, main_dir, "")
    
    #log that you're creating the average dataframe for the time point
    add_to_log(log_name, main_dir, "Creating the average dataframe for the time point: " + str(time_point))

    #get a new list with the columns with the "_norm" added
    norm_columns_list = []

    #loop through the columns
    for column in current_columns:

        #add the column with the "_norm" added
        norm_columns_list.append(column + "_norm")

    #initialize the average dataframe
    average_df = pd.DataFrame(index=range(max_length), columns=norm_columns_list)

    #get a file name for the average dataframe
    average_df_file_name = "average_df_" + str(time_point) + ".csv"

    #log that the data frame is initialized
    add_to_log(log_name, main_dir, "Data frame: "+ average_df_file_name + " initialized.")

    #log that you're filling the average dataframe
    add_to_log(log_name, main_dir, "Filling the average dataframe.")

    #loop through the columns of the average dataframe
    for column in norm_columns_list:

        #log that you're filling the column
        add_to_log(log_name, main_dir, "Getting averages for column: " + str(column))

        #loop through the number of rows of the scaled dataframe
        for a in range(0,max_length):

            #get a new counter for the number of values that actually had a value
            dfs_with_values = 0

            #get a variable for the sum of the values
            sum_of_values = 0

            #loop through the scaled dataframes
            for scaled_df in final_df_dict[time_point][0]:

                #check if the value is not nan
                if not np.isnan(scaled_df[column][a]):

                    #add one to the counter
                    dfs_with_values += 1

                    #add the value to the sum
                    sum_of_values += scaled_df[column][a]
            
            #check if the counter is not 0
            if dfs_with_values != 0:

                #get the average
                average = sum_of_values / dfs_with_values

                #set the value of the average dataframe
                average_df[column][a] = average
            
            #if the counter is 0
            else:
                    
                    #set the value to nan
                    average_df[column][a] = np.nan
            
            #log that you've added the row
            add_to_log(log_name, main_dir, "Added row: " + str(a) + " from column: " + str(column) + " with the average value: " + str(average_df[column][a]))

        #log that you're done with the column
        add_to_log(log_name, main_dir, "Done with column: " + str(column))

        #log an empty space
        add_to_log(log_name, main_dir, "")
    
    #log that you're done with the average dataframe
    add_to_log(log_name, main_dir, "Done with the average dataframe.")

    #log and empty space
    add_to_log(log_name, main_dir, "")

    #add the data frame to the final df dictionary
    final_df_dict[time_point][1] = average_df

    #log that you added the data frame to the final df dictionary
    add_to_log(log_name, main_dir, "Added the average dataframe to the final df dictionary.")

    #log that you're saving the average dataframe
    add_to_log(log_name, main_dir, "Saving the average dataframe at: " + results_dir + average_df_file_name + ".")

    #save the average dataframe
    average_df.to_csv(results_dir + average_df_file_name, index=False)

    #log that you're done saving the average dataframe
    add_to_log(log_name, main_dir, "Done saving the average dataframe.")

    #get the average co_start from the current_co_start_list
    average_co_start = int(round(sum(current_co_start_list) / len(current_co_start_list), 0))

    #get the average co_end from the current_co_end_list
    average_co_end = int(round(sum(current_co_end_list) / len(current_co_end_list),0))

    #log that you're adding the co_start and co_end to the final df dictionary
    add_to_log(log_name, main_dir, "Adding the average co_start with value "+ str(average_co_start) +" and the average co_end with value "+ str(average_co_end) +" to the final df dictionary at time point: " + str(time_point))

    #append the average co_start and co_end to the final df dictionary
    final_df_dict[time_point].append([average_co_start, average_co_end])

    #log that you're done with the time point
    add_to_log(log_name, main_dir, "Done with time point: " + str(time_point))

    #log an empty space
    add_to_log(log_name, main_dir, "")

#log that you're saving the final df dictionary
add_to_log(log_name, main_dir, "Saving the final df dictionary at: " + str(results_dir) + "final_df_dict.pickle")

#save the final df dictionary
pickle.dump(final_df_dict, open(results_dir + "final_df_dict.pickle", "wb"))

#log that the final dictionary is saved
add_to_log(log_name, main_dir, "Done saving the final df dictionary.")

#log that you're creating the plots
add_to_log(log_name, main_dir, "Creating the plots.")

#get all the unique columns from inside the columns_list[]
unique_columns_list = []

#loop through the columns_list[]
for a in range(len(columns_list)):

    #loop through the columns_list[a]
    for b in range(len(columns_list[a])):

        #check if the column is not in the unique_columns_list
        if columns_list[a][b] not in unique_columns_list:

            #add the column to the unique_columns_list
            unique_columns_list.append(columns_list[a][b])

#get the max number of columns
max_number_of_columns = len(unique_columns_list)

#log that you're creating the plots for the columns
add_to_log(log_name, main_dir, "Creating the plots for the columns: " + str(unique_columns_list))

#log an empty space
add_to_log(log_name, main_dir, "")

#loop through the max_number_of_columns
for a in range(max_number_of_columns):

    #get the first column name
    current_column_name = unique_columns_list[a]

    #get the norm column name
    norm_column_name = current_column_name + "_norm"

    #log that the working column is the first column name
    add_to_log(log_name, main_dir, "Working with column: " + str(norm_column_name))

    #get the number of time points that have this column
    number_of_time_points = 0

    #get a list with the number of time points that have the column
    time_point_with_column_list = []

    #loop through the time points length
    for b in range(len(time_point_list)):

        #check if the column is in the time point
        if current_column_name in columns_list[b]:

            #add one to the number of time points
            number_of_time_points += 1

            #add the time point to the list
            time_point_with_column_list.append(time_point_list[b])

    #log that the number of time points with the column is
    add_to_log(log_name, main_dir, "Number of time points with column: " + str(number_of_time_points))

    #log that the time points with the column are
    add_to_log(log_name, main_dir, "Time points with column: " + str(time_point_with_column_list))
    
    #get the number of plots based on the number of time points with the column
    number_of_plots = len(time_point_with_column_list)

    #log that you're setting up the figure
    add_to_log(log_name, main_dir, "Setting up the figure with the number of sub-plots: " + str(number_of_plots))

    #make a figure with the number of subplots set to the number of time points with the column
    fig, ax = plt.subplots(nrows=number_of_plots, ncols=1, figsize=(20,30))

    #set the font to times new roman
    plt.rcParams["font.family"] = "Times New Roman"

    #set up the plot hspaceing
    plt.subplots_adjust(hspace=0.6)

    #set the figure title
    fig.suptitle("Average intensity for channel " + str(a+1), fontsize=16)

    #log that the figure was set
    add_to_log(log_name, main_dir, "Done setting up the figure.")

    #start a counter for the time point
    time_point_plot_counter = 0

    #loop through the time point list order
    for time_point_order in time_point_list_order:

        #check if the time point is in the time_point_with_column_list
        if time_point_order in time_point_with_column_list:

            #log that the time point youre working with
            add_to_log(log_name, main_dir, "Creating the plot for time point: " + str(time_point_order))

            #get the averaged dataframe
            current_averaged_df = final_df_dict[time_point_order][1]

            #log that the data frame was loaded
            add_to_log(log_name, main_dir, "Done loading the data frame.")

            #get the co_start and co_end
            co_start = final_df_dict[time_point_order][2][0]
            co_end = final_df_dict[time_point_order][2][1]

            #log that the average co start and co end were loaded with ther values
            add_to_log(log_name, main_dir, "Done loading the average co_start with value: " + str(co_start) + " and the average co_end with value: " + str(co_end))

            #get tthe start and end of the values
            #get a list to hold the values of the channel
            channel_values_list = current_averaged_df

            #get the length of the averaged_df
            length_of_averaged_df = len(current_averaged_df)

            #log that the length of the averaged_df is
            add_to_log(log_name, main_dir, "Length of the averaged_df: " + str(length_of_averaged_df))

            #get the average value before co start
            average_value_before_co_start = current_averaged_df[norm_column_name][0:co_start].mean()

            #log that the average value before co start is
            add_to_log(log_name, main_dir, "Average value before co start: " + str(average_value_before_co_start))

            #get the average value after co end
            average_value_after_co_end = current_averaged_df[norm_column_name][co_end:length_of_averaged_df].mean()

            #log that the average value after co end is
            add_to_log(log_name, main_dir, "Average value after co end: " + str(average_value_after_co_end))

            #set the subplot title
            ax[time_point_plot_counter].set_title("Time point: " + str(time_point_order))

            #plot the square from 0 to the end of the plot with height of the mean before co
            ax[time_point_plot_counter].fill_between(current_averaged_df.index, average_value_before_co_start, color="dimgray", alpha=0.1)

            #set the y limits
            ax[time_point_plot_counter].set_ylim([0, 3])

            #set the y label
            ax[time_point_plot_counter].set_ylabel("Normalized and Averaged Intensity")

            #set the x label
            ax[time_point_plot_counter].set_xlabel("Length (microns)")

            #set the x limits
            ax[time_point_plot_counter].set_xlim(0, length_of_averaged_df)

            #set the x ticks
            ax[time_point_plot_counter].set_xticks(custom_ticks[0])

            #set the x tick labels
            ax[time_point_plot_counter].set_xticklabels(custom_ticks[1])

            #plot the averaged_df
            ax[time_point_plot_counter].plot(current_averaged_df[norm_column_name], plot_colors[time_point_plot_counter], alpha=0.75)
            
            #get the index_list
            index_list = list(current_averaged_df[0:length_of_averaged_df].index)

            #get the function
            #get the index of the plot
            plot_function = list(current_averaged_df[0:length_of_averaged_df][norm_column_name])

            #fill the area under the plot from the left side difference until the length of the df plus the left side difference
            ax[time_point_plot_counter].fill_between(index_list, plot_function, color=plot_colors[time_point_plot_counter], alpha=0.1)

            #plot the horizontal line for the co_start mean
            ax[time_point_plot_counter].plot([0, co_start], [average_value_before_co_start, average_value_before_co_start], color="slateblue", linestyle='--', linewidth=2)

            #plot the horizontal line for the co_end mean
            ax[time_point_plot_counter].plot([co_end, length_of_averaged_df], [average_value_after_co_end, average_value_after_co_end], color="salmon", linestyle='--', linewidth=2)

            #set up the crossover area
            ax[time_point_plot_counter].axvspan(co_start, co_end, alpha=0.2, color='green')

            #log that the plot was created
            add_to_log(log_name, main_dir, "Done creating the plot for time point: " + str(time_point_order) + " in the channel: "+ str(a+1))

            #log an emtpy space
            add_to_log(log_name, main_dir, "")

            #add one to the time point plot counter
            time_point_plot_counter += 1
    
    #log that the entire figure was finished
    add_to_log(log_name, main_dir, "Done creating the figure for channel: " + str(a+1))

    #get the file name to save the figure
    figure_filename_pdf = "c069_time_points_combined_channel" + str(a+1) + ".pdf"
    figure_filename_png = "c069_time_points_combined_channel" + str(a+1) + ".png"

    #log that you're preparing to save both, pdf and png
    add_to_log(log_name, main_dir, "Preparing to save the figure for channel: " + str(a+1) + " as both, pdf and png.")

    #save the figure as pdf
    plt.savefig(results_dir + figure_filename_pdf, format='pdf')

    #log that the figure was saved as pdf and where it was saved
    add_to_log(log_name, main_dir, "Done saving the figure for channel: " + str(a+1) + " as pdf in: " + results_dir + figure_filename_pdf)

    #save the figure as png
    plt.savefig(results_dir + figure_filename_png, format='png')

    #log that the figure was saved as png and where it was saved
    add_to_log(log_name, main_dir, "Done saving the figure for channel: " + str(a+1) + " as png in: " + results_dir + figure_filename_png)

    #loop through the time points
    for time_point_order in time_point_list_order:

        #get the index of the time point order
        index_of_time_point_order = time_point_list_order.index(time_point_order)

        #get the figure extent filename
        figure_extent_filename_pdf = "c069_time_points_combined_channel" + str(a+1) + "_" + str(time_point_order) + ".pdf"
        figure_extent_filename_png = "c069_time_points_combined_channel" + str(a+1) + "_" + str(time_point_order) + ".png"

        #get the figure extents
        extent = ax[index_of_time_point_order].get_window_extent().transformed(fig.dpi_scale_trans.inverted())

        #save the figure
        fig.savefig(results_dir + figure_extent_filename_pdf, format = 'pdf', bbox_inches=extent.expanded(1.2, 1.3))

        #log that the figure was saved as pdf and where it was saved
        add_to_log(log_name, main_dir, "Done saving the figure for channel: " + str(a+1) + " and time point: " + str(time_point_order) + " as pdf in: " + results_dir + figure_extent_filename_pdf)

        #save the figure
        fig.savefig(results_dir + figure_extent_filename_png, format = 'png', bbox_inches=extent.expanded(1.2, 1.3))

        #log that the figure was saved as png and where it was saved
        add_to_log(log_name, main_dir, "Done saving the figure for channel: " + str(a+1) + " and time point: " + str(time_point_order) + " as png in: " + results_dir + figure_extent_filename_png)

    #log that the channel was finished
    add_to_log(log_name, main_dir, "Done creating the figure for channel: " + str(a+1))

    #log an empty space
    add_to_log(log_name, main_dir, "")

#log that the script is done
add_to_log(log_name, main_dir, "Done creating the figures for all channels.")

#log that the script is finished
add_to_log(log_name, main_dir, "Done with the script....")

            









    
    


            

            


    


        





        




















