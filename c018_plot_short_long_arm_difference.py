

#region ################################### DESCRIPTION ##########################################

"""

This script will read the results from the c018 megasome short and long arm measurements and 
plot the results as a matplotlib figure.

"""

#endregion ################################ END OF DESCRIPTION ###################################


#region ################################### IMPORTS ##############################################

import os
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

#endregion ################################ END OF IMPORTS #######################################


#region ################################### GLOBALS ##############################################

#variable for the normalize to chromosome mean
normalize_to_chromosome_mean = True

#endregion ################################ END OF GLOBALS #######################################


#region ################################### FUNCTIONS ############################################



#endregion ################################ END OF FUNCTIONS #####################################

#region ################################### MAIN #################################################

#if name is main, print the script name
if __name__ == "__main__":

    #get the working directory
    working_directory = os.getcwd()

    #if the working directory doesn't end with a /, add opne
    if not working_directory.endswith("/"):
        working_directory += "/"

    #get the file list
    file_list = os.listdir(working_directory)

    #get the file list for the measurements files
    working_file_list = [file for file in file_list if "short_long_arm_measurements" in file]

    #create a figure
    fig = plt.figure()

    #create the axis
    ax = fig.add_subplot(111)

    #set the ax limit from -4.5 to 4.5
    ax.set_xlim(-4.5, 4.5)

    #make a dictionary with the data
    dictionary_data = {}

    #loop through the working file list
    for file in enumerate(working_file_list):

        #add the file to the dictionary
        dictionary_data[file[0]] = {"file_name": file[1]}

        #get the pandas data frame
        pandas_df = pd.read_csv(working_directory + file[1])

        #get the short arm mean values
        short_arm_mean_list = list(pandas_df["short_arm_mean"])

        #get the long arm mean values
        long_arm_mean_list = list(pandas_df["long_arm_mean"])

        #add them to the dictionary
        dictionary_data[file[0]]["short_arm_mean"] = {"pansyp1":short_arm_mean_list[0], "syp1phos":short_arm_mean_list[1]}

        #add them to the dictionary
        dictionary_data[file[0]]["long_arm_mean"] = {"pansyp1":long_arm_mean_list[0], "syp1phos":long_arm_mean_list[1]}

        #get the short arm lenth
        short_arm_length_list = list(pandas_df["short_arm_length"])

        #get the long arm length
        long_arm_length_list = list(pandas_df["long_arm_length"])

        #add them to the dictionary
        dictionary_data[file[0]]["short_arm_length"] = short_arm_length_list[0]

        #add them to the dictionary
        dictionary_data[file[0]]["long_arm_length"] = long_arm_length_list[0]

        #get the short arm to long arm ratio
        short_arm_long_arm_length_ratio = short_arm_length_list[0]/long_arm_length_list[0]

        #add them to the dictionary
        dictionary_data[file[0]]["short_arm_long_arm_length_ratio"] = short_arm_long_arm_length_ratio

        #get the long arm intensity list
        long_arm_intensity_list = list(pandas_df["long_arm_int"])

        #get the short arm intensity list
        short_arm_intensity_list = list(pandas_df["short_arm_int"])

        #add them to the dictionary
        dictionary_data[file[0]]["short_arm_intensity"] = {"pansyp1":short_arm_intensity_list[0], "syp1phos":short_arm_intensity_list[1]}

        #add them to the dictionary
        dictionary_data[file[0]]["long_arm_intensity"] = {"pansyp1":long_arm_intensity_list[0], "syp1phos":long_arm_intensity_list[1]}

        #get the combined length
        combined_length = short_arm_length_list[0] + long_arm_length_list[0]

        #get the combined pansyp1 intensity
        combined_pansyp1_intensity = short_arm_intensity_list[0] + long_arm_intensity_list[0]

        #get the combined syp1phos intensity
        combined_syp1phos_intensity = short_arm_intensity_list[1] + long_arm_intensity_list[1]

        #get the chr height
        chr_height = pandas_df["chr_height"][0]

        #add them to the dictionary
        dictionary_data[file[0]]["chr_length"] = combined_length

        #add them to the dictionary
        dictionary_data[file[0]]["chr_height"] = chr_height

        #add them to the dictionary
        dictionary_data[file[0]]["chr_intensity"] = {"pansyp1":combined_pansyp1_intensity, "syp1phos":combined_syp1phos_intensity}

        #add the chr_mean
        dictionary_data[file[0]]["chr_mean"] = {"pansyp1":combined_pansyp1_intensity/(combined_length*chr_height), "syp1phos":combined_syp1phos_intensity/(combined_length*chr_height)}

        #get the long arm short arm mean difference
        pansyp1_long_arm_short_arm_mean_difference = long_arm_mean_list[0] - short_arm_mean_list[0]

        #get the syp1phos long arm short arm mean difference
        syp1phos_long_arm_short_arm_mean_difference = long_arm_mean_list[1] - short_arm_mean_list[1]

        #add them to the dictionary
        dictionary_data[file[0]]["long_arm_short_arm_mean_difference"] = {"pansyp1":pansyp1_long_arm_short_arm_mean_difference, "syp1phos":syp1phos_long_arm_short_arm_mean_difference}

        #add the normalized to chr_mean
        dictionary_data[file[0]]["long_arm_short_arm_mean_difference_normalized_to_chr_mean"] = {"pansyp1":pansyp1_long_arm_short_arm_mean_difference/dictionary_data[file[0]]["chr_mean"]["pansyp1"], "syp1phos":syp1phos_long_arm_short_arm_mean_difference/dictionary_data[file[0]]["chr_mean"]["syp1phos"]}

    #get the number of files
    number_of_files = len(dictionary_data.keys())

    #create a list from the dictionary keys
    dictionary_keys_list = list(dictionary_data.keys())

    #get the list of the short arm ratios
    short_arm_long_arm_length_ratio_list = [dictionary_data[key]["short_arm_long_arm_length_ratio"] for key in dictionary_keys_list]

    #get the name list
    name_list = [dictionary_data[key]["file_name"] for key in dictionary_keys_list]

    #create a list of the short arm mean differences for syp1phos
    syp1phos_long_arm_short_arm_mean_difference_list = [dictionary_data[key]["long_arm_short_arm_mean_difference"]["syp1phos"] for key in dictionary_keys_list]

    #if the normalize to chromosome mean is true, replace that list with the normalized list
    if normalize_to_chromosome_mean:

        #create a list of the short arm mean differences for syp1phos
        syp1phos_long_arm_short_arm_mean_difference_list = [dictionary_data[key]["long_arm_short_arm_mean_difference_normalized_to_chr_mean"]["syp1phos"] for key in dictionary_keys_list]

    #sort the syp1phos_long_arm_short_arm_mean_difference_list using the short_arm_long_arm_length_ratio_list and get both lists sorted by the short_arm_long_arm_length_ratio_list
    short_arm_long_arm_length_ratio_list, syp1phos_long_arm_short_arm_mean_difference_list, name_list = zip(*sorted(zip(short_arm_long_arm_length_ratio_list, syp1phos_long_arm_short_arm_mean_difference_list, name_list)))

    #loop through the short_arm_long_arm_length_ratio_list and scatter
    for index, value in enumerate(short_arm_long_arm_length_ratio_list):

        #get the corresponding syp1phos_long_arm_short_arm_mean_difference_list value
        x_value = syp1phos_long_arm_short_arm_mean_difference_list[index]

        #if the x_value is greater than 0, scatter in blue
        if x_value >= 0:
            ax.scatter(x_value, value, color="blue", edgecolors="black")

            #print the name
            print(f"Name: {name_list[index]}, value: {x_value}, ratio: {value}" )


        #if the x_value is less than 0, scatter in magenta
        elif x_value < 0:
            ax.scatter(x_value, value, color="magenta", edgecolors="black")

        #if the value is less than 0.5 and the x_value is greater than 0, print the file name 
        if value < 0.5 and x_value > 0:

            #print
            print("")

            #print the file name
            print(f"Under 0.5 ratio and positive difference: {name_list[index]}, value: {x_value}, ratio: {value}" )
            
            #print
            print("")
    
    #set the title
    ax.set_title("Chromosome segments phosphorylated SYP-1 average intensity difference")

    #set the y label
    ax.set_ylabel("Short arm length / long arm length")

    ax.set_xlabel("Phosphorylated SYP-1 long arm mean - short arm mean")

    #if the normalize to chromosome mean is true, change the x label
    if normalize_to_chromosome_mean:

        #set the x label
        ax.set_xlabel("Phosphorylated SYP-1 (long arm mean - short arm mean) / chromosome mean")

    #plot the points as scatter
    # ax.scatter(syp1phos_long_arm_short_arm_mean_difference_list, dictionary_keys_list, color="red", label="syp1phos")

    # #set the color of the negative poitns to magenta
    # ax.scatter([value for value in syp1phos_long_arm_short_arm_mean_difference_list if value < 0], [key for key in dictionary_keys_list if dictionary_data[key]["long_arm_short_arm_mean_difference"]["syp1phos"] < 0], color="magenta", edgecolors="black")

    # #set the color of the positive points to blue
    # ax.scatter([value for value in syp1phos_long_arm_short_arm_mean_difference_list if value > 0], [key for key in dictionary_keys_list if dictionary_data[key]["long_arm_short_arm_mean_difference"]["syp1phos"] > 0], color="blue", edgecolors="black")

    #create a dictionary of the file name with the corresponding value if the value is greater than 0
    syp1phos_long_arm_short_arm_mean_difference_greater_than_zero = {dictionary_data[key]["file_name"]:dictionary_data[key]["long_arm_short_arm_mean_difference"]["syp1phos"] for key in dictionary_keys_list if dictionary_data[key]["long_arm_short_arm_mean_difference"]["syp1phos"] > 0}

    #loop through the dictionary and print the file name and the value
    # for key in syp1phos_long_arm_short_arm_mean_difference_greater_than_zero.keys():
    #     print(key, syp1phos_long_arm_short_arm_mean_difference_greater_than_zero[key])

    #add a vertical line to the zero in green color
    ax.axvline(x=0, color="green")

    #get the plot filename
    plot_filename = "c018_megasome_segments_short_long_arm_difference_plot.pdf"

    #save the plot as a pdf
    plt.savefig(working_directory + plot_filename, bbox_inches="tight", format="pdf", dpi=300)    

    #show the plot
    plt.show()




#endregion ################################ END OF MAIN ##########################################




