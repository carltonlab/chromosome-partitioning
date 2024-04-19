#region ######################################## DESCRIPTION ##################################################

"""
This script will get the corresponding roi file from a straightened chromosome or nuclei and make the 3D model from it
using pyplot, roifile.
"""

#endregion ##################################### END DESCRIPTION ##############################################


#region ######################################## IMPORTS ######################################################

import json
import roifile
import matplotlib.pyplot as plt
import argparse
import os
import sys
import pickle as pkl
from scipy.interpolate import splprep, splev

#endregion ###################################### END IMPORTS ##################################################


#region ######################################## GLOBALS ######################################################

#variable for the z step
z_step = 0.125

#variable for the pixel size in microns
pixel_size_in_microns = 0.04

#the plot to limit distance ratio
plot_to_limit_distance_ratio = 0.1

#set the colors 
colors = ["purple", "forestgreen", "silver", "royalblue", "orange", "red", "pink", "black", "white"]

axes_pane_color = (0.05, 0.05, 0.05, 1)

show_grid_flag = True

#set the grid color
grid_color = (0.15, 0.15, 0.15, 1)

#set the grid color
plt.rcParams['grid.color'] = grid_color

#set the ticks color
ticks_clolor = (1,1,1,1)

#set the tick step in microns
tick_step_in_microns = 0.5

#endregion ##################################### END GLOBALS ##################################################


#region ######################################## CLASSES ######################################################



#endregion ##################################### END CLASSES ##################################################


#region ######################################### METHODS ######################################################

#method to load the roi file
def load_roi_files(main_dir, file):

    #read the roi and make them a list of the rois with
    rois = [file, roifile.roiread(main_dir + file)]

    #return the rois
    return rois

#method to get the chromosomes object
def get_chromosomes_object(sbs_rois):

    #get the z steo to pixel size ratio
    z_step_to_pixel_size_ratio = z_step/pixel_size_in_microns

    #make a dictionary
    chromosomes_object = {}

    #get the rois file names
    rois_file_names = [roi.name for roi in sbs_rois[1]]

    #get the last item
    last_item = rois_file_names[-1]

    #get the chromosome number by getting the string between "chr" and the first "-"
    chromosome_number = int(last_item[last_item.find("chr") + 3:last_item.find("-")])

    #loop through the number of chromosomes
    for chromosome in range(1, chromosome_number + 1):

        #start the object entry
        chromosomes_object["chr" + str(chromosome)] = {"coords": {} }

    #loop through the number of chromosomes
    for chromosome in range(1, chromosome_number + 1):

        #start a cooridnate counter
        coordinate_counter = 0

        #get the chr string
        chr_string = "chr"  + str(chromosome) + "-"

        #get the chromosome roi list
        chromosome_roi_list = []

        #loop through the sbs_rois[1]
        for roi in sbs_rois[1]:

            #if the chr string is in the roi name
            if chr_string in roi.name:

                #append the roi to the list
                chromosome_roi_list.append(roi)

        #if the chromosome roi list length is greater than 0
        if len(chromosome_roi_list) > 0:

            #loop through the chromosome roi list
            for chromosome_roi in chromosome_roi_list:

                #get the subpixel_coordinates
                subpixel_coordinates = chromosome_roi.subpixel_coordinates

                #loop through the subpixel_coordinates
                for subpixel_coordinate in subpixel_coordinates:
                    
                    #get the z relative coordinate by multiplying the z position by the z step to pixel size ratio
                    z_relative_coordinate = chromosome_roi.z_position * z_step_to_pixel_size_ratio

                    #get the cooridnates
                    x_coord = subpixel_coordinate[0]

                    #get the y coordinate
                    y_coord = subpixel_coordinate[1]

                    #get the z position
                    z_position = chromosome_roi.z_position

                    #get the relative z coordinate
                    z_relative_coordinate = z_position * z_step_to_pixel_size_ratio

                    #add them to the corresponding chromosomes object
                    chromosomes_object["chr" + str(chromosome)]["coords"][str(coordinate_counter)] = {}
                    chromosomes_object["chr" + str(chromosome)]["coords"][str(coordinate_counter)]["x"] = x_coord
                    chromosomes_object["chr" + str(chromosome)]["coords"][str(coordinate_counter)]["y"] = y_coord
                    chromosomes_object["chr" + str(chromosome)]["coords"][str(coordinate_counter)]["z"] = z_relative_coordinate
                    chromosomes_object["chr" + str(chromosome)]["coords"][str(coordinate_counter)]["z_position"] = z_position
                    chromosomes_object["chr" + str(chromosome)]["coords"][str(coordinate_counter)]["pixel_size"] = pixel_size_in_microns
                    chromosomes_object["chr" + str(chromosome)]["coords"][str(coordinate_counter)]["z_step"] = z_step
                    chromosomes_object["chr" + str(chromosome)]["coords"][str(coordinate_counter)]["z_step_to_pixel_size_ratio"] = z_step_to_pixel_size_ratio

                    #increment the coordinate counter
                    coordinate_counter += 1

    #return the chromosomes object
    return chromosomes_object

#method to get the custom ticks
def get_custom_ticks(x_range, y_range, z_range):

    #get the custom ticks object
    custom_ticks_object = {}

    #get the x range in microns
    x_range_in_microns = x_range * pixel_size_in_microns

    #get the y range in microns
    y_range_in_microns = y_range * pixel_size_in_microns

    #get the z range in microns
    z_range_in_microns = z_range * pixel_size_in_microns

    #get the x tick
    x_ticks = []

    xticks_done = False

    #start xtick
    current_x_tick = 0

    #while loop for the x ticks
    while xticks_done is False:

        #current_xmicron_xpixel_pair
        current_xmicron_xpixel_pair = [current_x_tick, int(current_x_tick / pixel_size_in_microns)]

        #add the current x tick to the x ticks
        x_ticks.append(current_xmicron_xpixel_pair)

        #increment the current x tick
        current_x_tick += tick_step_in_microns

        #round to the first decimal
        current_x_tick = round(current_x_tick, 1)

        #if the current x tick is greater than the x range in microns
        if current_x_tick > x_range_in_microns:
            
            #get the current xmicron_xpixel_pair
            current_xmicron_xpixel_pair = [current_x_tick, int(current_x_tick / pixel_size_in_microns)]

            #add the current x tick to the x ticks
            x_ticks.append(current_xmicron_xpixel_pair)

            #set the xticks done to true
            xticks_done = True

    #get the y tick
    y_ticks = []

    yticks_done = False

    #start ytick
    current_y_tick = 0

    #while loop for the y ticks
    while yticks_done is False:

        #make the list of micron_pickel tick
        micron_pixel_ticks = [current_y_tick , int(current_y_tick / pixel_size_in_microns)]

        #add the current y tick to the y ticks
        y_ticks.append(micron_pixel_ticks)

        #increment the current y tick
        current_y_tick += tick_step_in_microns

        #round to the first decimal
        current_y_tick = round(current_y_tick, 1)

        #if the current y tick is greater than the y range in microns
        if current_y_tick > y_range_in_microns:

            #get the current ymicron_ypixel_pair
            current_ymicron_ypixel_pair = [current_y_tick, int(current_y_tick / pixel_size_in_microns)]

            #add the current y tick to the y ticks
            y_ticks.append(current_ymicron_ypixel_pair)

            #set the yticks done to true
            yticks_done = True

    #get the z tick
    z_ticks = []

    zticks_done = False

    #start ztick
    current_z_tick = 0

    #while loop for the z ticks
    while zticks_done is False:

        #get the ccurrent pair
        current_zmicron_zpixel_pair = [current_z_tick, int(current_z_tick / pixel_size_in_microns)]

        #add the current z tick to the z ticks
        z_ticks.append(current_zmicron_zpixel_pair)

        #increment the current z tick
        current_z_tick += tick_step_in_microns

        #round to the first decimal
        current_z_tick = round(current_z_tick, 1)

        #if the current z tick is greater than the z range in microns
        if current_z_tick > z_range_in_microns:

            #get the current zmicron_zpixel_pair
            current_zmicron_zpixel_pair = [current_z_tick, int(current_z_tick / pixel_size_in_microns)]

            #add the current z tick to the z ticks
            z_ticks.append(current_zmicron_zpixel_pair)

            #set the zticks done to true
            zticks_done = True

    #put them into the custom ticks object
    custom_ticks_object["x"] = x_ticks

    #put them into the custom ticks object
    custom_ticks_object["y"] = y_ticks

    #put them into the custom ticks object
    custom_ticks_object["z"] = z_ticks

    #return the custom ticks object
    return custom_ticks_object

#method to make the model plots
def make_model_plots(saving_object):

    #loop through the saving object
    for file_index in saving_object:

        #get the file name
        file_name = saving_object[file_index]["file_name"]

        #print a space
        print("")

        #print the file name
        print("Making the 3D model for: " + file_name)

        #get the chromosomes object
        chromosomes_object = saving_object[file_index]["chromosomes_object"]

        #make the figure
        fig = plt.figure()

        #set the size
        fig.set_size_inches(10, 10)

        #make the axis
        ax = fig.add_subplot(111, projection='3d')

        #set the figure's patch
        fig.set_facecolor('black')

        #set the axis face color
        ax.set_facecolor('black')

        #take out the grid
        ax.grid(show_grid_flag)

        #set the w_axis color
        ax.xaxis.set_pane_color(axes_pane_color)

        #set the w_axis color
        ax.yaxis.set_pane_color(axes_pane_color)

        #set the w_axis color
        ax.zaxis.set_pane_color(axes_pane_color)

        #set the tick params
        ax.tick_params(axis='x', colors=ticks_clolor, pad=0)

        #set the tick params
        ax.tick_params(axis='y', colors=ticks_clolor, pad=0)

        #set the tick params
        ax.tick_params(axis='z', colors=ticks_clolor, pad=0)

        #get the max x
        max_x = 0

        #get the max y
        max_y = 0

        #get the max z
        max_z = 0

        #get the min x 
        min_x = 100000

        #get the min y
        min_y = 100000

        #get the min z
        min_z = 100000

        #make a chromosome points object
        chromosome_points_object = {}

        #loop through the chrommosomes in the chromosomes object
        for chromosome in chromosomes_object:

            #get the cooridnates object
            coordinates_object = chromosomes_object[chromosome]["coords"]

            #add to the chromosome points object
            chromosome_points_object[chromosome] = {"x": None, "y": None, "z": None}

            #get the x coordinates
            x_coordinates = [coordinates_object[point]["x"] for point in coordinates_object]

            #set the chromosome points object
            chromosome_points_object[chromosome]["x"] = x_coordinates

            #get the y coordinates
            y_coordinates = [coordinates_object[point]["y"] for point in coordinates_object]

            #set the chromosome points object
            chromosome_points_object[chromosome]["y"] = y_coordinates

            #get the z coordinates
            z_coordinates = [coordinates_object[point]["z"] for point in coordinates_object]

            #set the chromosome points object
            chromosome_points_object[chromosome]["z"] = z_coordinates

            #get the max x
            current_max_x = max(x_coordinates)

            #if the current max x is greater than the max x
            if current_max_x > max_x:

                #set the max x
                max_x = current_max_x

            #get the min x
            current_min_x = min(x_coordinates)

            #if the current min x is less than the min x
            if current_min_x < min_x:

                #set the min x
                min_x = current_min_x

            #get the max y
            current_max_y = max(y_coordinates)

            #if the current max y is greater than the max y
            if current_max_y > max_y:

                #set the max y
                max_y = current_max_y

            #get the min y
            current_min_y = min(y_coordinates)

            #if the current min y is less than the min y
            if current_min_y < min_y:

                #set the min y
                min_y = current_min_y


            #get the max z
            current_max_z = max(z_coordinates)

            #if the current max z is greater than the max z
            if current_max_z > max_z:

                #set the max z
                max_z = current_max_z

            #get the min z
            current_min_z = min(z_coordinates)

            #if the current min z is less than the min z
            if current_min_z < min_z:

                #set the min z
                min_z = current_min_z

        #get the x range
        x_range = max_x - min_x

        #get the 0.1 x range
        x_range_01 = x_range * plot_to_limit_distance_ratio

        #get the stated min x
        stated_min_x = min_x - x_range_01

        #if the stated min x is less than 0
        if stated_min_x < 0:

            #set the stated min x to 0
            stated_min_x = 0

        #get the stated max x
        stated_max_x = max_x + x_range_01

        #get the y range
        y_range = max_y - min_y

        #get the 0.1 y range
        y_range_01 = y_range * plot_to_limit_distance_ratio

        #get the stated min y
        stated_min_y = min_y - y_range_01

        #if the stated min y is less than 0
        if stated_min_y < 0:

            #set the stated min y to 0
            stated_min_y = 0

        #get the stated max y
        stated_max_y = max_y + y_range_01

        #get the z range
        z_range = max_z - min_z

        #get the 0.1 z range
        z_range_01 = z_range * plot_to_limit_distance_ratio

        #get the stated min z
        stated_min_z = min_z - z_range_01

        #if the stated min z is less than 0
        if stated_min_z < 0:

            #set the stated min z to 0
            stated_min_z = 0

        #get the stated max z
        stated_max_z = max_z + z_range_01

        #start the chromosome counter
        chromosome_counter = 0

        #loop through the chromosome points object
        for chromosome in chromosome_points_object:

            #subtract the statex min x from the x coordinates
            x_coordinates = [x - stated_min_x for x in chromosome_points_object[chromosome]["x"]]

            #subtract the stated min y from the y coordinates
            y_coordinates = [y - stated_min_y for y in chromosome_points_object[chromosome]["y"]]

            #subtract the stated min z from the z coordinates
            z_coordinates = [z - stated_min_z for z in chromosome_points_object[chromosome]["z"]]

            #get the interpolation points
            tck, u  = splprep([x_coordinates, y_coordinates, z_coordinates], s=26)

            #get the new points
            new_points = splev(u, tck)

            #get the x coordinates
            new_x_coordinates = new_points[0]

            #get the y coordinates
            new_y_coordinates = new_points[1]

            #get the z coordinates
            new_z_coordinates = new_points[2]

            #if the chromosome counter is 0
            if chromosome_counter == 0:

                #plot the points
                ax.plot(new_x_coordinates, new_y_coordinates, new_z_coordinates, color=colors[chromosome_counter], linewidth=3)

            #else if the chromosome counter more than 0
            elif chromosome_counter > 0:

                #plot the points
                ax.plot(new_x_coordinates, new_y_coordinates, new_z_coordinates, color=colors[chromosome_counter], linewidth=0.7)

            #increment the chromosome counter
            chromosome_counter += 1

        #set the title
        ax.set_title(file_name)

        #set the title color
        ax.title.set_color(ticks_clolor)

        #set the title font size
        ax.title.set_fontsize(8)

        #set the x label
        ax.set_xlabel("Microns")

        #set the color
        ax.xaxis.label.set_color(ticks_clolor)

        #set the y label
        ax.set_ylabel("Microns")

        #set the color
        ax.yaxis.label.set_color(ticks_clolor)

        #set the z label
        ax.set_zlabel("Microns")

        #set the color
        ax.zaxis.label.set_color(ticks_clolor)

        #get the custom ticks for the axes
        custom_ticks_object = get_custom_ticks(stated_max_x - stated_min_x, stated_max_y - stated_min_y, stated_max_z - stated_min_z)

        #get the x ticks
        x_ticks_merged_list = custom_ticks_object["x"]

        #get the actual m ticks
        x_ticks_actual_list = [x_tick[1] for x_tick in x_ticks_merged_list]

        #get the x tick labels
        x_tick_labels = [str(x_tick[0]) for x_tick in x_ticks_merged_list]

        #get the last x_ticks_actual_list
        last_x_ticks_actual_list = x_ticks_actual_list[-1]

        #set the x limit
        ax.set_xlim3d(0, last_x_ticks_actual_list)

        #get the y ticks
        y_ticks_merged_list = custom_ticks_object["y"]

        #get the actual m ticks
        y_ticks_actual_list = [y_tick[1] for y_tick in y_ticks_merged_list]

        #get the y tick labels
        y_tick_labels = [str(y_tick[0]) for y_tick in y_ticks_merged_list]

        #get the last y_ticks_actual_list
        last_y_ticks_actual_list = y_ticks_actual_list[-1]

        #set the y limit
        ax.set_ylim3d(0, last_y_ticks_actual_list)

        #get the z ticks
        z_ticks_merged_list = custom_ticks_object["z"]

        #get the actual m ticks
        z_ticks_actual_list = [z_tick[1] for z_tick in z_ticks_merged_list]

        #get the z tick labels
        z_tick_labels = [str(z_tick[0]) for z_tick in z_ticks_merged_list]

        #get the last z_ticks_actual_list
        last_z_ticks_actual_list = z_ticks_actual_list[-1]

        #set the z limit
        ax.set_zlim3d(0, last_z_ticks_actual_list)

        #set the x ticks
        ax.set_xticks(x_ticks_actual_list)

        #set the x tick labels
        ax.set_xticklabels(x_tick_labels)

        #set the y ticks
        ax.set_yticks(y_ticks_actual_list)

        #set the y tick labels
        ax.set_yticklabels(y_tick_labels)

        #set the z ticks
        ax.set_zticks(z_ticks_actual_list)

        #set the z tick labels
        ax.set_zticklabels(z_tick_labels)

        #set the label font size
        ax.tick_params(labelsize=7)

        #make the rendering proportional
        ax.set_aspect('auto')

        #get the file name without extension
        file_name_without_extension = file_name[:file_name.find(".")]

        #get the save name
        save_name = file_name_without_extension + "_3dmodel.pdf"

        #set the view point
        ax.view_init(azim=-45, elev=25)

        #save the figure as a pdf
        plt.savefig(main_dir + save_name, format="pdf", dpi=300)

        #set the other view point
        ax.view_init(azim=-90, elev=-90)

        #get the new save name
        second_save_name = save_name.replace("_3dmodel.pdf", "_same_as_projection.pdf")

        #save the figure as a pdf
        plt.savefig(main_dir + second_save_name, format="pdf", dpi=300)

        #Set everything but the plot to invisible
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.zaxis.set_visible(False)

        #set the background to transparent
        ax.patch.set_alpha(0)

        #set the figure's patch
        fig.set_facecolor('none')

        #set the axis face color
        ax.set_facecolor('none')

        #set the w_axis color
        ax.xaxis.set_pane_color((0,0,0,0))

        #set the w_axis color
        ax.yaxis.set_pane_color((0,0,0,0))

        #set the w_axis color
        ax.zaxis.set_pane_color((0,0,0,0))

        #set the axes color
        ax.xaxis.label.set_color((0,0,0,0))

        #set the axes color
        ax.yaxis.label.set_color((0,0,0,0))

        #set the axes color
        ax.zaxis.label.set_color((0,0,0,0))

        #set the title color
        ax.title.set_color((0,0,0,0))

        #hide the ticks
        ax.set_xticks([])

        #hide the ticks
        ax.set_yticks([])

        #hide the ticks
        ax.set_zticks([])

        #hide the actual axis
        ax._axis3don = False

        #hide the grid
        ax.grid(False)

        #set the transparent title
        transparent_file_name = save_name.replace("_3dmodel.pdf", "_same_as_projection_transparent.png")

        #save the figure as transparent background png
        plt.savefig(main_dir + transparent_file_name, format="png", dpi=300, transparent=True)
    
        #print the the file was saved
        print("The file was saved as: " + save_name)

        #the projection model was saved as
        print("The projection model was saved as: " + second_save_name)

        #the transparent projection model was saved as
        print("The transparent projection model was saved as: " + transparent_file_name)

        #close the figure
        plt.close(fig)

#endregion ###################################### END METHODS ##################################################


#region ######################################### MAIN #########################################################

#if name is main
if __name__ == "__main__":

    #start the main dir
    main_dir = None

    #set the files
    files = None
    
    #get the parser
    parser = argparse.ArgumentParser(description="Plot the STR roi files into a 3D model from the fiji carltonlab straightener.")

    #add the argument for the main directory
    parser.add_argument('-d', type=str, help='The main directory to use.')

    #add the argument for the files
    parser.add_argument('-f', nargs="+", type=argparse.FileType('r'), help='The files to use.')

    #add an exclude option to the parser
    parser.add_argument('-e', nargs="+", type=str, help='The strings to exclude from the files.')

    #get the parser args
    args = parser.parse_args()

    #get the main dir
    main_dir = args.d

    #if the user did not add any directory
    if main_dir is None:

        #set the main dir to the current dir
        main_dir = os.getcwd() + "/"

    #if the main dir does not end with a slash
    if main_dir is not None and not main_dir.endswith("/"):
        
        #add a slash
        main_dir += "/"

    #get the files
    files_types = args.f

    #if the files_types length is greater than 0
    if files_types is not None and len(files_types) > 0:

        #set the files
        files = [file.name for file in files_types]

    #if the user added any files
    if files is None:

        #set the files to the current dir
        files = os.listdir(main_dir)

        #filter them
        files = [file for file in files if file.endswith(".roi") or file.endswith(".zip")]

    #if the files length is greater than 0 and the exclude is not none
    if files is not None and len(files) > 0 and args.e is not None:

        #loop through the exclude
        for exclude in args.e:

            #filter the files
            files = [file for file in files if exclude not in file]


    #print the files
    print("The files to use are: " + str(files))

    #verify the existance of the main_dir
    if not os.path.exists(main_dir):

        #print the error
        print("The main directory does not exist.")
        print("main_dir: " + main_dir)

        #exit the program
        exit()

    #verify the existance of the files
    if files is None or len(files) == 0:

        #print the error
        print("There are no files to use.")

        #exit the program
        exit()

    #loop thorugh the files and verify they exist
    for file in files:

        #if the file does not exist
        if not os.path.exists(file):

            #print the error
            print("The file does not exist.")
            print("file: " + file)

            #exit the program
            exit()

    #get the rois lists
    rois_list = [load_roi_files(main_dir, file) for file in files]

    #start the saving object
    saving_object = {}

    #loop through the roi object
    for rois in enumerate(rois_list):

        #print a space
        print("")

        #print the file name
        print("Getting the chromosomes object for: " + rois[1][0])

        #get the index and the roi
        index, sbs_rois = rois

        #make index a str
        index = str(index)

        #add the index to the saving object
        saving_object[index] = {}

        #add the file name to the saving object
        saving_object[index]["file_name"] = sbs_rois[0]

        #get the chromosomes object
        chromosomes_object = get_chromosomes_object(sbs_rois)

        #add the chromosomes object to the saving object
        saving_object[index]["chromosomes_object"] = chromosomes_object

    #get the pickle of the saving object
    pickle = pkl.dumps(saving_object)

    #save the pickle
    with open(main_dir + "straight_models.pickle", "wb") as f:

        #write the pickle
        f.write(pickle)
    
    #make the plots
    make_model_plots(saving_object)

    





#endregion ###################################### END MAIN ######################################################