#region ########################################################## DESCRIPTION ####################################################################

"""
This script plots the short and long arm average intensities for each channel in the csv files. 
It gets a directory (the directory where the script is executed from) and looks for files with the name ending with 'with_short_arm.csv'.

For this to work, you need to have run the script c012_get_arm_differences.py first, which will create the csv files with the short arm values.
It will take many csv files and plot them individually so you can combine all the .csv files in one directory from different genotypes, experiments, etc. 

The script will plot the short arm values in magenta and the long arm values in blue. Please modify as needed. 

"""


#endregion ####################################################### END OF DESCRIPTION #############################################################

#import pandas
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#get the directory string
main_directory = os.getcwd()

#if name is main
if __name__ == '__main__':

    #print an empty space
    print('')    

    #print that the script is running
    print('running c012_plot_short_and_long_arm_average_intensityes.py')

    #if the main directory does not exist, print an error message
    if not os.path.exists(main_directory):
        print(f'the main directory does not exist: {main_directory}')

        #exit the script
        exit()

    #if the directory does not end with a /
    if not main_directory.endswith('/'):
        
        #add a /
        main_directory += '/'

    #get the file list
    file_list = os.listdir(main_directory)

    #get the csv files
    csv_files = [file for file in file_list if file.endswith('with_short_arm.csv')]

    #print the csv files
    print(f'the csv files are: {csv_files}')  

    #initialize the data frame list, where the csv files will be loaded to. 
    data_frame_list = []

    #loop through the csv files and load them to the data frame list
    #by opening them with pandas
    for csv_file in csv_files:

        #get the file string
        file_string = f'{main_directory}{csv_file}'

        #open the csv file to pandas
        data_frame = pd.read_csv(file_string)

        #append the data frame to the data frame list
        data_frame_list.append(data_frame)

    #start the number of plots
    number_of_plots = 0

    #loop through the data frame list
    for data_frame in data_frame_list:

        #get the number of columns
        number_of_columns = len(data_frame.columns)

        #get the number of plots by subtracting 1 from the number of columns,
        #since the first column is the file name and then divide by 2
        number_of_plots += (number_of_columns - 2) / 2

    #get the number of plots, round it up and cast it as an integer
    number_of_plots = int(round(number_of_plots))

    #print the number of plots
    print(f'the number of plots is: {number_of_plots}')

    #make the figure 
    fig, ax = plt.subplots(nrows=number_of_plots, ncols=1, figsize=(10, (number_of_plots*10)))

    #make a counter for the plot index
    plot_index = 0

    #get the counter for the file
    file_counter = 0    

    #loop through the data frame list
    for current_data_frame in data_frame_list:

        #get the file name by getting the file at the csv files list
        current_file_name = csv_files[file_counter]

        #get the number of plots for this data frame
        number_of_plots = (len(current_data_frame.columns) - 2) / 2

        #make it an int
        number_of_plots = int(round(number_of_plots))

        #get the column name list
        current_column_name_list = list(current_data_frame.columns)

        #get it from 1 to the end
        current_column_name_list = current_column_name_list[2:]

        #loop through the number of plots
        for channel in range(number_of_plots):

            #get the column names
            plotting_column_names = current_column_name_list[channel*2:channel*2+2]

            #print the plotting column names
            print(f'the plotting column names are: {plotting_column_names}')

            #get the short arm values
            short_arm_values = list(current_data_frame[plotting_column_names[0]])

            #get the short arm mean
            short_arm_mean = sum(short_arm_values) / len(short_arm_values)

            #get the short arm np array
            short_arm_np_array = np.array(short_arm_values)

            #get the std of the short arm
            short_arm_std = np.std(short_arm_np_array)

            #get the long arm values
            long_arm_values = list(current_data_frame[plotting_column_names[1]])

            #get the long arm mean
            long_arm_mean = sum(long_arm_values) / len(long_arm_values)

            #get the long arm np array
            long_arm_np_array = np.array(long_arm_values)

            #get the std of the long arm
            long_arm_std = np.std(long_arm_np_array)

            #get the short arm length list
            short_arm_length_list = list(current_data_frame['short_arm_lenth'])

            #sort the short arm length list, the short arm values and the long arm values by the short arm length list descending
            short_arm_length_list, short_arm_values, long_arm_values = zip(*sorted(zip(short_arm_length_list, short_arm_values, long_arm_values), reverse=True))

            #get the index list
            index_list = list(range(1, len(short_arm_values)+1))

            #get the mid of plot
            mid_of_plot = len(short_arm_values) / 2

            #get an eigth of the plot
            tenth_of_plot = len(short_arm_values) / 20

            #make the scatter plot for the short arm
            ax[plot_index].scatter(short_arm_values, index_list, color='m', label='short arm', alpha=0.2, edgecolor='black', s=100)

            # #make the box plot for the short arm
            # ax[plot_index].boxplot(short_arm_values, 
            #                         positions=[mid_of_plot],
            #                         widths=20, 
            #                         patch_artist=True,
            #                         boxprops=dict(facecolor='m', color='m', alpha=0.8),
            #                         meanprops=dict(color='m'),
            #                         medianprops=dict(color='m'), 
            #                         whiskerprops=dict(color='m'), 
            #                         capprops=dict(color='m'), 
            #                         vert=False)
            
            #make the error bar
            ax[plot_index].errorbar(short_arm_mean, 
                                    mid_of_plot-tenth_of_plot, 
                                    xerr=short_arm_std, 
                                    fmt='^', 
                                    color='m', 
                                    label='short arm', 
                                    alpha=1, 
                                    markersize=5)

            #make the scatter plot for the long arm
            ax[plot_index].scatter(long_arm_values, index_list, color='b', label='long arm', alpha=0.2, edgecolor='black', s=100)

            # #make the box plot for the long arm
            # ax[plot_index].boxplot(long_arm_values,
            #                         positions=[mid_of_plot],
            #                         widths=20,
            #                         patch_artist=True,
            #                         boxprops=dict(facecolor='b', color='b', alpha=0.8),
            #                         meanprops=dict(color='b'),
            #                         medianprops=dict(color='b'),
            #                         whiskerprops=dict(color='b'),
            #                         capprops=dict(color='b'), 
            #                         vert=False)
            
            #make the error bar
            ax[plot_index].errorbar(long_arm_mean, 
                                    mid_of_plot+tenth_of_plot, 
                                    xerr=long_arm_std, 
                                    fmt='v', 
                                    color='b', 
                                    label='long arm', 
                                    alpha=1, 
                                    markersize=5)

            #set the title
            ax[plot_index].set_title(f'{current_file_name} - {plotting_column_names[0]} and {plotting_column_names[1]}')

            #set the x limits from -3.5 to 4.5
            ax[plot_index].set_xlim(0, 4.5)

            #add one to the plot index
            plot_index += 1

        #add one to the file counter
        file_counter += 1            

    #save the plot as a pdf and png
    plt.savefig(f'{main_directory}short_and_long_arm_average_intensityes.pdf')
    plt.savefig(f'{main_directory}short_and_long_arm_average_intensityes.png')



