
#region ################################### DESCRIPTION ##########################################

"""

This script will read the results from the c018 megasome with two crossovers and plot them
on the designed triangle plot that we often use. 

For it to work, you need the crossover coordinates file and the crossover category file. 

Run the script in the directory with those files and use the arguments to specify the plot.

Run the -h argument to see the help.

"""

#endregion ################################ END OF DESCRIPTION ###################################


#region ################################### IMPORTS ##############################################

import os
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import math
import tifffile
import datetime
import argparse

#endregion ################################ END OF IMPORTS #######################################


#region ################################### GLOBALS ##############################################


#region ///////// vector specs

#set up the vector magnitude
vector_magnitude = 1

#set up the vector angle
vector_angle = 0

#set up the crossover_axes_angle
crossover_axes_angle = 90

#set up the origin point
origin_point = [0,0]

out_name = None

#endregion ////// end vector specs


#region ///////// point specs

#set up the points specs
points_specs =  {
                1:{"shape":"o", "color":"black", "edgecolor":"black", "alpha":1, "plotting":True, "size":200, "edge_width":2},
                2:{"shape":"o", "color":"gold", "edgecolor":"black", "alpha":1, "plotting":True, "size":200, "edge_width":2},
                3:{"shape":"s", "color":"green", "edgecolor":"black", "alpha":1, "plotting":True, "size":200, "edge_width":2},
                4:{"shape":"*", "color":"slateblue", "edgecolor":"black", "alpha":1, "plotting":True, "size":400, "edge_width":2},
                }

#endregion ////// end point specs


#region ///////// patches specs

#set up the plotting patches
plotting_patches =  {
                    1:{"name":"outer", "color":"yellow", "alpha":0.2, "plotting":True},
                    2:{"name":"mixed_left", "color":"blue", "alpha":0.2, "plotting":True},
                    3:{"name":"mixed_right", "color":"blue", "alpha":0.2, "plotting":True},
                    4:{"name":"inner", "color":"green", "alpha":0.2, "plotting":True},
                    5:{"name":"interference", "color":"gray", "alpha":0.3, "plotting":True}
                    }

#endregion ////// end patches specs


#region ///////// plt figure specs

#set up the x limit ratios for the lowest and highest compared to the vector magnitude
x_limit_ratio_lowest_highest_to_vector_magnitude = [0.05, 0.05]

#set up the y limit ratios for lowest and highest compared to the vector magnitude
y_limit_ratio_loest_highest_to_vector_magniture = [0.05, 0.05]

#set up custom x limits
custom_x_limits = []

#set up custom y limits
custom_y_limits = []

#endregion ////// end plt figure specs


#region ///////// plotting data specs

#set file termination that is expected of the crossover coordinates file
crossover_coordinates_file_termination_list = ["_co_coords.csv"]

#set up the file termination that is expected of the crossover category file
crossover_category_file_termination_list = ["_sum_proj_category.csv"]

#set up a list of the string that identify the files to include. In theory, this should be the chromosome tiff image. 
#In carlos's experiments c018, they terminate with _str.tif so that will be added to the list next by default. Take it out if you don't want it. 
#The script will later take out the extension of the file name and add the crossover coordinates file termination to it to get the crossover coordinates from that file. 
#The script will also take out the extension of the file name and add the crossover category file termination to it to get the crossover category from that file.
#if multiple files with different terminations are found for the crossover coordinates file and the category file, it will take the first one of each and ignore the rest 
#of the files.
inclusion_string_list = ["_str.tif"]

#set up a list of the strings that identify the files to exclude.
exclude_file_terminations_list = []

#set up the plotting chromosomes from directory
plotting_chromosomes_directory_list = []

#set up the plotting points from file
plotting_chromosomes_file_list = []

#set up the plotting chromosomes full dictionary 
plotting_chromosomes_final_dictionary = {}

#set up the adding dictionary list
# plotting_chromosomes_dictionary_list = []

#for the syp1_paper figure 4:
#for outer
#1: c016_slide1_20190531_004_SIR_chrALN_sbs4_str_chromosome2_megasome_no_dapi_str.tif
#2: c018_2022_10_20_strain_gfpcosa1_met7_stain_pansyp1_syp1phos_gfp_slide7_gonad10_sbs2_chr3_zero_clamped_str.tif
# plotting_chromosomes_dictionary_list =  [
#                                         {"name":"1","crossover_list":[162, 500], "category":2, "length":560},
#                                         {"name":"2", "crossover_list":[61, 301], "category":2, "length":389}
#                                         ]       

#for inner
#1: c016_slide1_20190531_004_SIR_chrALN_sbs12_str_chromosome1_megasome_no_dapi_str.tif
#2: c016_slide1_20190531_006_SIR_chrALN_sbs4_str_chromosome4_megasome_no_dapi_str.tif
# plotting_chromosomes_dictionary_list =  [
#                                         {"name":"1","crossover_list":[153, 365], "category":3, "length":488},
#                                         {"name":"2","crossover_list":[224, 322], "category":3, "length":540}
#                                         ]

#for mixed
#1: c018_2022_10_20_stain_gfpcosa1_met7_stain_pansyp1_syp1phos_gfp_slide7_gonad8_sbs13_chr1_zero_clamped_str.tif
#2: c018_2022_10_20_stain_gfpcosa1_met7_stain_pansyp1_syp1phos_gfp_slide8_gonad4_sbs6_chr1_zero_clamped_str.tif
# plotting_chromosomes_dictionary_list =  [
#                                         {"name":"1","crossover_list":[43, 173], "category":4, "length":289},
#                                         {"name":"2", "crossover_list":[91, 257], "category":4, "length":276}
#                                         ]

#all of them combined
plotting_chromosomes_dictionary_list =  [
                                        {"name":"1","crossover_list":[162, 500], "category":2, "length":560},
                                        {"name":"2", "crossover_list":[61, 301], "category":2, "length":389},
                                        {"name":"1","crossover_list":[153, 365], "category":3, "length":488},
                                        {"name":"2","crossover_list":[224, 322], "category":3, "length":540},
                                        {"name":"1","crossover_list":[43, 173], "category":4, "length":289},
                                        {"name":"2", "crossover_list":[91, 257], "category":4, "length":276}
                                        ]



#endregion ////// end plotting data specs

#get the current directory
current_directory = os.getcwd()

#if the current directory does not end with a slash
if not current_directory.endswith("/"):

    #add the slash
    current_directory += "/"

#endregion ################################ END OF GLOBALS #######################################


#region ################################### FUNCTIONS ############################################

#funtion to get the date and time string
def get_date_time_string():

    #get the date and time string
    return str(datetime.datetime.now()).replace(" ", "_").replace(":", "-").split(".")[0]

#function to plot a point
def plot_chromosome_point(crossover_coords, chromosome_length, point_type, origin_point, vector_angle, secondar_vector_angle, name):

    #if the type is plot
    if points_specs[point_type]["plotting"]:

        #get the normalized points
        normalized_points = [x / chromosome_length for x in crossover_coords]

        #get the first point from left
        first_point_from_left = normalized_points[0]

        #get the second poitn from right
        second_point_from_right = 1 - normalized_points[1]

        #get the final point 
        final_point = [origin_point[0] + (second_point_from_right * math.cos(math.radians(vector_angle))) + (first_point_from_left * math.cos(math.radians(secondar_vector_angle))), (origin_point[1] + (second_point_from_right * math.sin(math.radians(vector_angle))) + (first_point_from_left * math.sin(math.radians(secondar_vector_angle))))]

        #plot the final point
        plt.scatter(final_point[0], final_point[1], color=points_specs[point_type]["color"], marker=points_specs[point_type]["shape"], edgecolors=points_specs[point_type]["edgecolor"], s=points_specs[point_type]["size"], linewidths=points_specs[point_type]["edge_width"], alpha=points_specs[point_type]["alpha"])

        #make a label with the name 
        plt.text(final_point[0], final_point[1], name, fontsize=5)

        #return the final point
        return final_point

#endregion ################################ END OF FUNCTIONS #####################################


#region ################################### MAIN #################################################

#if name is main, print the script name
if __name__ == "__main__":

    #region //////////// arguments parser

    #set up the arguments parser
    parser = argparse.ArgumentParser(description="Make the triangle plot for the meT7 chromosomes with two crossovers")

    #add the arguments
    parser.add_argument("-vm", "--vector-magnitude", help="The magnitude of the vector", type=float, default=None)
    parser.add_argument("-an", "--vector-angle", help="The angle of the vector", type=float, default=None)
    parser.add_argument("-caa", "--crossover-axes-angle", help="The angle of the crossover axes", type=float, default=None)
    parser.add_argument("-xr", "--x-limits-ratio", help="The x limit ratio for the lowest and highest compared to the vector magnitude", type=float, nargs=2, default=None)
    parser.add_argument("-yr", "--y-limits-ratio", help="The y limit ratio for the lowest and highest compared to the vector magnitude", type=float, nargs=2, default=None)
    parser.add_argument("-or", "--origin-point", help="The origin point of the triangle plot", type=float, nargs=2, default=None)
    parser.add_argument("-xl", "--x-limits", help="The x limits of the plot", type=float, nargs=2, default=None)
    parser.add_argument("-yl", "--y-limits", help="The y limits of the plot", type=float, nargs=2, default=None)
    parser.add_argument("-d", "--directory", help="The directory of the chromosomes to plot", type=str, nargs='+',default=None)
    parser.add_argument("-f", "--file", help="The file of the chromosome to plot", type=str, nargs='+',default=None)
    parser.add_argument("-in", "--inclusion-string", help="The string that identifies the files to include", type=str, nargs='+',default=None)
    parser.add_argument("-ex", "--exclusion-string", help="The string that identifies the files to exclude", type=str, nargs='+',default=None)
    parser.add_argument("-cofn", "--crossover-terminations", help="Crossovers Termination File Name. The termination that identifies the crossover files", type=str, nargs='+' ,default=None)
    parser.add_argument("-catfn", "--category-terminations", help="Category Termination File Name. The termination that identifies the crossover category file", type=str, nargs='+' ,default=None)
    parser.add_argument("-o", "--output", help="The output file name", type=str, default=None)

    #parse the arguments
    args = parser.parse_args()

    #if the vector magnitude is not none
    if args.vector_magnitude is not None:

        #set the vector magnitude
        vector_magnitude = args.vector_magnitude
    
    #if the vector angle is not none
    if args.vector_angle is not None:

        #set the vector angle
        vector_angle = args.vector_angle

    #if the crossover axes angle is not none
    if args.crossover_axes_angle is not None:

        #set the crossover axes angle
        crossover_axes_angle = args.crossover_axes_angle
    
    #if the origin point is not none
    if args.origin_point is not None:

        #set the origin point
        origin_point = args.origin_point

    #if the x limits ratio is not none
    if args.x_limits_ratio is not None:

        #set the x limit ratio
        x_limit_ratio_lowest_highest_to_vector_magnitude = args.x_limits_ratio

    #if the y limits ratio is not none
    if args.y_limits_ratio is not None:

        #set the y limit ratio
        y_limit_ratio_loest_highest_to_vector_magniture = args.y_limits_ratio

    #if the x limits is not none
    if args.x_limits is not None:

        #set the x limits
        custom_x_limits = args.x_limits

    #if the y limits is not none
    if args.y_limits is not None:

        #set the y limits
        custom_y_limits = args.y_limits

    #if the directory is not none
    if args.directory is not None:

        #loop through the directories and add them to the plotting chromosomes directory list
        for directory in args.directory:

            #add the directory to the plotting chromosomes directory list
            plotting_chromosomes_directory_list.append(directory)

    #if the file is not none
    if args.file is not None:

        #loop through the files and add them to the plotting chromosomes file list
        for file in args.file:

            #add the file to the plotting chromosomes file list
            plotting_chromosomes_file_list.append(file)

    #if the inclusion string is not none
    if args.inclusion_string is not None:

        #loop through the inclusion strings and add them to the inclusion string list
        for inclusion_string in args.inclusion_string:

            #add the inclusion string to the inclusion string list
            inclusion_string_list.append(inclusion_string)

        #make a set of the inclusion string list
        inclusion_string_list = list(set(inclusion_string_list))

    #if the exclusion string is not none
    if args.exclusion_string is not None:

        #loop through the exclusion strings and add them to the exclusion string list
        for exclusion_string in args.exclusion_string:

            #add the exclusion string to the exclusion string list
            exclude_file_terminations_list.append(exclusion_string)

        #make a set of the exclusion string list
        exclude_file_terminations_list = list(set(exclude_file_terminations_list))

    #if the crossover terminations is not none
    if args.crossover_terminations is not None:

        #loop through the crossover terminations and add them to the crossover coordinates file termination list
        for crossover_termination in args.crossover_terminations:

            #add the crossover termination to the crossover coordinates file termination list
            crossover_coordinates_file_termination_list.append(crossover_termination)

        #make a set of the crossover coordinates file termination list
        crossover_coordinates_file_termination_list = list(set(crossover_coordinates_file_termination_list))

    #if the category terminations is not none
    if args.category_terminations is not None:

        #loop through the category terminations and add them to the crossover category file termination list
        for category_termination in args.category_terminations:

            #add the category termination to the crossover category file termination list
            crossover_category_file_termination_list.append(category_termination)

        #make a set of the crossover category file termination list
        crossover_category_file_termination_list = list(set(crossover_category_file_termination_list))

    #if the output is not none
    if args.output is not None:

        #if it desn't end with .png
        if not args.output.endswith(".png"):

            #print a message 
            print("The output file name does not end with .png. I don't have time to implement name handling.... please use a .png termination.")

            #exit
            exit()

        #set the output name
        out_name = args.output

    #endregion ///////// end arguments parser

    #region //////////// making the plot body

    #set up the total second_vector_angle
    second_vector_angle = vector_angle + crossover_axes_angle

    #set up the vector in axis
    vector_in_x = False

    #set up the vector in y axis
    vector_in_y = False

    #set up the second vector in x axis
    second_vector_in_x = False

    #set up the second vector in y axis
    second_vector_in_y = False

    #if the cosine of the vector angle is 1 or -1
    if math.cos(math.radians(vector_angle)) == 1 or math.cos(math.radians(vector_angle)) == -1:

        #set the vector in x axis
        vector_in_x = True

    #if the sine of the vector angle is 1 or -1
    if math.sin(math.radians(vector_angle)) == 1 or math.sin(math.radians(vector_angle)) == -1:

        #set the vector in y axis
        vector_in_y = True

    #if the cosine of the second vector angle is 1 or -1
    if math.cos(math.radians(second_vector_angle)) == 1 or math.cos(math.radians(second_vector_angle)) == -1:

        #set the second vector in x axis
        second_vector_in_x = True

    #if the sine of the second vector angle is 1 or -1
    if math.sin(math.radians(second_vector_angle)) == 1 or math.sin(math.radians(second_vector_angle)) == -1:

        #set the second vector in y axis
        second_vector_in_y = True

    #set up vector_end_point
    vector_end_point = [(origin_point[0] + (vector_magnitude * math.cos(math.radians(vector_angle)))), (origin_point[1] + (vector_magnitude * math.sin(math.radians(vector_angle))))]

    #start the vector_slope
    vector_slope = None

    #start the vector b
    vector_b = None

    #if the vector is not in x or y axis
    if not vector_in_x and not vector_in_y:

        #get the slope of the vector_end_point to the origin point
        vector_slope = (origin_point[1] - vector_end_point[1]) / (origin_point[0] - vector_end_point[0])

    #if the vector is not in x or y axis
    if not vector_in_x and not vector_in_y:

        #get the vector b
        vector_b = vector_end_point[1] - (vector_end_point[0] * vector_slope)

    #set up the second_vector_end_point
    second_vector_end_point = [(origin_point[0] + (vector_magnitude * math.cos(math.radians(second_vector_angle)))), (origin_point[1] + (vector_magnitude * math.sin(math.radians(second_vector_angle))))]

    #start the second vector slope
    second_vector_slope = None

    #start the second vector b
    second_vector_b = None

    #if the second vector is not in x or y axis
    if not second_vector_in_x and not second_vector_in_y:
            
        #get the slope of the second_vector_end_point to the origin point
        second_vector_slope = (origin_point[1] - second_vector_end_point[1]) / (origin_point[0] - second_vector_end_point[0])

    #if the second vector is not in x or y axis
    if not second_vector_in_x and not second_vector_in_y:

        #get the second_vector b
        second_vector_b = second_vector_end_point[1] - (second_vector_end_point[0] * second_vector_slope)

    #get the min x
    min_x = min([origin_point[0], vector_end_point[0], second_vector_end_point[0]])

    #get the max x
    max_x = max([origin_point[0], vector_end_point[0], second_vector_end_point[0]])

    #get the min y
    min_y = min([origin_point[1], vector_end_point[1], second_vector_end_point[1]])

    #get the max y
    max_y = max([origin_point[1], vector_end_point[1], second_vector_end_point[1]])

    #get the x limits
    x_limits = [min_x - (vector_magnitude * x_limit_ratio_lowest_highest_to_vector_magnitude[0]), max_x + (vector_magnitude * x_limit_ratio_lowest_highest_to_vector_magnitude[1])]

    #get the y limits
    y_limits = [min_y - (vector_magnitude * y_limit_ratio_loest_highest_to_vector_magniture[0]), max_y + (vector_magnitude * y_limit_ratio_loest_highest_to_vector_magniture[1])]

    #get the triangle center point
    triangle_center_point = [(origin_point[0] + (0.25 * vector_magnitude * math.cos(math.radians(vector_angle))) + (0.25 * vector_magnitude * math.cos(math.radians(second_vector_angle)))), (origin_point[1] + (0.25 * vector_magnitude * math.sin(math.radians(second_vector_angle))) + (0.25 * vector_magnitude * math.sin(math.radians(vector_angle))))]

    #get the slope from the vector_end_point to the triangle_center_point
    vector_end_point_triangle_center_point_slope = (triangle_center_point[1] - vector_end_point[1]) / (triangle_center_point[0] - vector_end_point[0])
    
    #get the slope from the second_vector_end_point to the triangle center point
    second_vector_end_point_triangle_center_point_slope = (triangle_center_point[1] - second_vector_end_point[1]) / (triangle_center_point[0] - second_vector_end_point[0])

    #start the crossover_2_crossing_point
    vector_cutting_point = [None, None]

    #start the vector_cutting_b
    vector_cutting_b = vector_end_point[1] - (vector_end_point[0] * vector_end_point_triangle_center_point_slope)

    #start the second_vector_cutting_b
    second_vector_cutting_b = second_vector_end_point[1] - (second_vector_end_point[0] * second_vector_end_point_triangle_center_point_slope)

    #if the second vector is not in x or y axis
    if not second_vector_in_x and not second_vector_in_y:

        #get the intersection of the crossover_2_end point and the second vector 
        #the equation is x(vm - svm) = svb - vb
        vector_cutting_point[0] = (second_vector_b - vector_cutting_b)/(vector_end_point_triangle_center_point_slope - second_vector_slope)

        #get the y of the intersection of the vector cutting point
        vector_cutting_point[1] = (vector_end_point_triangle_center_point_slope * vector_cutting_point[0]) + vector_cutting_b

    #if the second vector is in the y axis
    if second_vector_in_y:

        #set the x to zero
        vector_cutting_point[0] = 0

        #set the y to the solution of y = mx + b
        vector_cutting_point[1] = (vector_end_point_triangle_center_point_slope * vector_cutting_point[0]) + vector_cutting_b

    #if the second vector is in the x axis
    if second_vector_in_x:

        #set the x to the solution of x = y-b/m
        vector_cutting_point[0] = (0 - vector_cutting_b) / vector_end_point_triangle_center_point_slope

        #set the y to zero
        vector_cutting_point[1] = 0

    #start the second_vector_cutting_point
    second_vector_cutting_point = [None, None]

    #if the vector is not in x or y axis
    if not vector_in_x and not vector_in_y:

        #get the intersection of the crossover_2_end point and the second vector 
        #the equation is x(vm - svm) = svb - vb
        second_vector_cutting_point[0] = (vector_b - second_vector_cutting_b)/(second_vector_end_point_triangle_center_point_slope - vector_slope)

        #get the y of the intersection of the vector cutting point
        second_vector_cutting_point[1] = (second_vector_end_point_triangle_center_point_slope * second_vector_cutting_point[0]) + second_vector_cutting_b

    #if the vector is in the y axis
    if vector_in_y:

        #set the x to zero
        second_vector_cutting_point[0] = 0

        #set the y to the solution of y = mx + b
        second_vector_cutting_point[1] = (second_vector_end_point_triangle_center_point_slope * second_vector_cutting_point[0]) + second_vector_cutting_b

    #if the vector is in the x axis
    if vector_in_x:

        #set the x to the solution of x = y-b/m
        second_vector_cutting_point[0] = (0 - second_vector_cutting_b) / second_vector_end_point_triangle_center_point_slope

        #set the y to zero
        second_vector_cutting_point[1] = 0

    #make the 2/3 point vector
    vector_two_thirds_point = [(origin_point[0] + (((2/3)*vector_magnitude) * math.cos(math.radians(vector_angle)))), (origin_point[1] + (((2/3)*vector_magnitude) * math.sin(math.radians(vector_angle))))]

    #make the 2/3 point second vector
    second_vector_two_thirds_point = [(origin_point[0] + (((2/3)*vector_magnitude) * math.cos(math.radians(second_vector_angle)))), (origin_point[1] + (((2/3)*vector_magnitude) * math.sin(math.radians(second_vector_angle))))]

    # #if the vector is in x axis
    # if vector_in_x:

    #     #set the crossover_2_b
    #     crossover_2_b = 0 - (vector_end_point[0] * vector_end_point_triangle_center_point_slope)

    # #if the vector is in the y axis
    # if vector_in_y:

    #     #set the crossover_2_b
    #     crossover_2_b = vector_end_point[1] - (vector_end_point[0] * vector_end_point_triangle_center_point_slope)

    # #if the vector is not in the x or y axis
    # if not vector_in_x and not vector_in_y:

    #     #set the crossover_2_b
    #     crossover_2_b = vector_end_point[1] - (vector_end_point[0] * vector_end_point_triangle_center_point_slope)

    # #if the secondary vector is in the x axis
    # if second_vector_in_x:

    #     #set the crossover_1_b
    #     crossover_1_b = 0 - (second_vector_end_point[0] * second_vector_end_point_triangle_center_point_slope)

    # #if the secondary vector is in the y axis
    # if second_vector_in_y:
            
    #         #set the crossover_1_b
    #         crossover_1_b = second_vector_end_point[1] - (second_vector_end_point[0] * second_vector_end_point_triangle_center_point_slope)

    #set up the figure
    fig, ax = plt.subplots(figsize=(15,15))

    #keep the axes aspect ratio equal
    ax.set_aspect('equal', adjustable='box')

    #if there's no custom x limits
    if len(custom_x_limits) == 0:

        #set up the x limit
        plt.xlim(x_limits)

    #if there's custom x limits
    if len(custom_x_limits) == 2:

        #set up the x limit
        plt.xlim(custom_x_limits)

    #if it is different than 0 or 2
    if len(custom_x_limits) != 0 and len(custom_x_limits) != 2:

        #print that the custom x limits are not 0 or 2
        print("The custom x limits are not 0 or 2")

        #exit
        exit()

    #if there's no custom y limits
    if len(custom_y_limits) == 0:

        #set up the y limit
        plt.ylim(y_limits)

    #if there's custom y limits
    if len(custom_y_limits) == 2:

        #set up the y limit
        plt.ylim(custom_y_limits)

    #if it is different than 0 or 2
    if len(custom_y_limits) != 0 and len(custom_y_limits) != 2:

        #print that the custom y limits are not 0 or 2
        print("The custom y limits are not 0 or 2")

        #exit
        exit()

    #plot the origin and the vector_end_point
    plt.plot([origin_point[0], vector_end_point[0]], [origin_point[1], vector_end_point[1]], color="black")
    
    #plot the origin and the second_vector_end_point
    plt.plot([origin_point[0], second_vector_end_point[0]], [origin_point[1], second_vector_end_point[1]], color="black")

    #plot the second_vector_end_point and the vector_end_point
    plt.plot([second_vector_end_point[0], vector_end_point[0]], [second_vector_end_point[1], vector_end_point[1]], color="black")

    #plot the line between the vector end point and the vector cutting point
    plt.plot([vector_end_point[0], vector_cutting_point[0]], [vector_end_point[1], vector_cutting_point[1]], color="black", linestyle="dashed", linewidth=1)

    #plot the line between the second vector end point and the second vector cutting point
    plt.plot([second_vector_end_point[0], second_vector_cutting_point[0]], [second_vector_end_point[1], second_vector_cutting_point[1]], color="black", linestyle="dashed", linewidth=1)

    #make the outer_polygon
    plotting_patches[1]["polygon"] = plt.Polygon([origin_point, second_vector_cutting_point, triangle_center_point, vector_cutting_point], color = plotting_patches[1]["color"], fill=True, alpha=plotting_patches[1]["alpha"])

    #make the left mixed polygon to the plot
    plotting_patches[2]["polygon"] = plt.Polygon([second_vector_cutting_point, vector_end_point, triangle_center_point], color=plotting_patches[2]["color"], fill=True, alpha=plotting_patches[2]["alpha"])

    #make the right mixed polygon to the plot
    plotting_patches[3]["polygon"] = plt.Polygon([vector_cutting_point, second_vector_end_point, triangle_center_point], color=plotting_patches[3]["color"], fill=True, alpha=plotting_patches[3]["alpha"])

    #make the innter polygon
    plotting_patches[4]["polygon"] = plt.Polygon([vector_end_point, second_vector_end_point, triangle_center_point], color=plotting_patches[4]["color"], fill=True, alpha=plotting_patches[4]["alpha"])

    #make the interference polygon
    plotting_patches[5]["polygon"] = plt.Polygon([vector_two_thirds_point, vector_end_point, second_vector_end_point, second_vector_two_thirds_point], color=plotting_patches[5]["color"], fill=True, alpha=plotting_patches[5]["alpha"])

    #loop through the plotting patches
    for patch_index in plotting_patches:

        #if the plotting is true
        if plotting_patches[patch_index]["plotting"]:

            #add the polygon to the plot
            ax.add_patch(plotting_patches[patch_index]["polygon"])

    #endregion ///////// end making the plot body

    #region //////////// gather points

    #make a list with no repeats of the directory list
    plotting_chromosomes_directory_list = list(set(plotting_chromosomes_directory_list))

    #if "." or "./" is in the plotting chromosomes directory list
    if "." in plotting_chromosomes_directory_list or "./" in plotting_chromosomes_directory_list:

        #replace it with the current directory
        plotting_chromosomes_directory_list = [current_directory if x == "." or x == "./" else x for x in plotting_chromosomes_directory_list]

    #make a set of the list again
    plotting_chromosomes_directory_list = list(set(plotting_chromosomes_directory_list))

    #make a list with the ignored directory list
    ignored_directories = []

    #make a list with no repeats of the file list
    plotting_chromosomes_file_list = list(set(plotting_chromosomes_file_list))

    #make a list with the ignored file list
    ignored_files = []

    #loop through the directory list and make sure all of them end with a slash
    for directory_index, directory in enumerate(plotting_chromosomes_directory_list):

        #if the directory does not end with a slash
        if not directory.endswith("/"):

            #add the slash
            plotting_chromosomes_directory_list[directory_index] += "/"

    #loop through the directory list and verify if they exist. if they don't, print the error and add them to the ignored directories
    for directory_index, directory in enumerate(plotting_chromosomes_directory_list):

        #if the directory does not exist
        if not os.path.exists(directory):

            #print the error
            print(f'The directory {directory} does not exist. ignoring it for the plotting.')

            #add the directory to the ignored directories
            ignored_directories.append(directory)

    #loop through the file list and verify if they exist. if they don't, print the error and add them to the ignored files
    for file_index, file in enumerate(plotting_chromosomes_file_list):

        #if the file does not exist
        if not os.path.exists(file):

            #print the error
            print(f'The file {file} does not exist. ignoring it for the plotting.')

            #add the file to the ignored files
            ignored_files.append(file)

    #remove the ignored directories from the plotting chromosomes directory list
    plotting_chromosomes_directory_list = [directory for directory in plotting_chromosomes_directory_list if directory not in ignored_directories]

    #remove the ignored files from the plotting chromosomes file list
    plotting_chromosomes_file_list = [file for file in plotting_chromosomes_file_list if file not in ignored_files]

    #loop through the directory list and get the files to add to the plotting chromosomes file list
    for directory in plotting_chromosomes_directory_list:

        #print the directory you're working on
        print(f'Working on directory: {directory}')

        #get the file list
        temprary_all_file_list = os.listdir(directory)

        #get a filtered file list 
        temporary_filtered_inclusion_file_list = []

        #loop through the file list
        for file in temprary_all_file_list:

            #loop through the inclusion string list
            for inclusion_string in inclusion_string_list:

                #if the inclusion string is in the file
                if inclusion_string in file:

                    #add the file to the filtered file list
                    temporary_filtered_inclusion_file_list.append(file)

        #get a filtered file list
        temprary_filtered_exclusion_file_list = temporary_filtered_inclusion_file_list.copy()

        #loop through the exclusion string list
        for exclusion_string in exclude_file_terminations_list:

            #get the filtered file list
            temprary_filtered_exclusion_file_list = [file for file in temprary_filtered_exclusion_file_list if exclusion_string not in file]

        #make a set of the filtered file list
        temprary_filtered_exclusion_file_list = list(set(temprary_filtered_exclusion_file_list))

        #loop through the filtered file list
        for file in temprary_filtered_exclusion_file_list:

            #add the file to the plotting chromosomes file list
            plotting_chromosomes_file_list.append(directory + file)

    #make a set of the plotting chromosomes file list
    plotting_chromosomes_file_list = list(set(plotting_chromosomes_file_list))

    #loop through the plotting chromosomes file list
    for file_index, file in enumerate(plotting_chromosomes_file_list):

        #start a new object 
        current_chromosome_object = {}

        #set the name
        current_chromosome_object["name"] = file

        #get the file without extension. Make sure that there might be more than one . in the file name
        file_without_extension = ".".join(file.split(".")[:-1])

        #get the crossover file list
        temproary_crossover_file_list = []

        #loop through the crossover coordinates file termination list
        for crossover_coordinates_file_termination in crossover_coordinates_file_termination_list:

            #if the file exists
            if os.path.exists(file_without_extension + crossover_coordinates_file_termination):
    
                #add the file to the crossover file list
                temproary_crossover_file_list.append(file_without_extension + crossover_coordinates_file_termination)

        #set the crossover list
        temporary_crossover_list = []

        #if there's at least one file in the crossover file list
        if len(temproary_crossover_file_list) > 0:

            #get the first file in the crossover file list
            first_file = temproary_crossover_file_list[0]

            #use pandas to read the first file
            crossover_data_frame = pd.read_csv(first_file)

            #get the crossover list
            temporary_crossover_list = crossover_data_frame["x"].tolist()

            #if the first crossover is bigger than the last crossover
            if temporary_crossover_list[0] > temporary_crossover_list[-1]:

                #reverse the crossover list
                temporary_crossover_list = temporary_crossover_list[::-1]
            
            #set the crossover list
            current_chromosome_object["crossover_list"] = temporary_crossover_list

        #if there's no file in the crossover file list
        if len(temproary_crossover_file_list) == 0:
            
            #print that the file doesn't have the crossover file
            print(f'The file {file} does not have the crossover file. Ignoring it.')

            #add the file to the ignored files
            ignored_files.append(file)

            #contine to the next file
            continue

        #get the category file list
        temproary_category_file_list = []

        #loop through the crossover category file termination list
        for crossover_category_file_termination in crossover_category_file_termination_list:

            #if the file exists
            if os.path.exists(file_without_extension + crossover_category_file_termination):

                #add the file to the category file list
                temproary_category_file_list.append(file_without_extension + crossover_category_file_termination)

        #start the temprary category
        temporary_category = None

        #if there's at least one file in the category file list
        if len(temproary_category_file_list) > 0:

            #get the first file in the category file list
            first_file = temproary_category_file_list[0]

            #use pandas to read the first file
            category_data_frame = pd.read_csv(first_file)

            #get the category
            temporary_category = category_data_frame["category"][0]

            #set the category
            current_chromosome_object["category"] = int(temporary_category)

        #if there's no file in the category file list
        if len(temproary_category_file_list) == 0:

            #print that the file doesn't have the category file
            print(f'The file {file} does not have the category file. Ignoring it.')

            #add the file to the ignored files
            ignored_files.append(file)

            #contine to the next file
            continue

        #use tifffile to read the file\
        chromsome_data = tifffile.imread(file)

        #get the shape
        chromosome_data_shape = chromsome_data.shape

        #get the length
        length = chromosome_data_shape[-1]

        #set the length
        current_chromosome_object["length"] = length

        #get the length of the plotting chromosomes dictionary
        current_chromsome_index = len(plotting_chromosomes_final_dictionary)

        #add the chromosome object to the plotting chromosomes dictionary
        plotting_chromosomes_final_dictionary[current_chromsome_index] = current_chromosome_object

    #loop through the plotting_chromosomes_dicionary_list
    for chromosome_object in plotting_chromosomes_dictionary_list:

        #get the plotting_chromosomes_final_dictionary length
        current_chromsome_index = len(plotting_chromosomes_final_dictionary)

        #add the chromosome object to the plotting chromosomes dictionary
        plotting_chromosomes_final_dictionary[current_chromsome_index] = chromosome_object

    #endregion ///////// end gather points
        
    #region //////////// plot points

    #loop through the plotting chromosomes dictionary
    for chromosome_index in plotting_chromosomes_final_dictionary:

        #get the chromosome object
        chromosome_object = plotting_chromosomes_final_dictionary[chromosome_index]

        #get the name
        chromosome_name = chromosome_object["name"]

        #get the chromosome length
        chromosome_length = chromosome_object["length"]

        #get the crossover list
        crossover_list = chromosome_object["crossover_list"]

        #get the category
        chromosome_category = chromosome_object["category"]

        #plot the point
        plotting_chromosomes_final_dictionary[chromosome_index]["plot_coord"] = plot_chromosome_point(crossover_list,chromosome_length,chromosome_category,origin_point, vector_angle, second_vector_angle, chromosome_name)

    #endregion ///////// end plot points



    #region //////////// saving plot

    #if the out name does not start with /
    if not out_name.startswith("/"):

        #add the current directory
        out_name = current_directory + out_name

    #if the out name exists in png, ask if you want to overwrite
    if os.path.exists(out_name.replace(".png", ".svg")) or os.path.exists(out_name.replace(".png", ".pdf")) or os.path.exists(out_name):

        #ask if you want to overwrite
        overwrite = input(f'The file {out_name} exists. Do you want to overwrite it? (y/n) ')

        #if the answer is not y
        if overwrite != "y":

            #exit
            exit()

    #print the out name
    print(f'Plotting the figure in {out_name}')

    #save the figure as png
    plt.savefig(out_name, dpi=300)

    #save the figure as svb
    plt.savefig(out_name.replace(".png", ".svg"), dpi=300)

    #save the figure as pdf
    plt.savefig(out_name.replace(".png", ".pdf"), dpi=300)

    #endregion ///////// end saving plot

    exit()

#endregion ################################ END OF MAIN ##########################################


