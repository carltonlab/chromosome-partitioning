#region description



#endregion description

#region imports

import os
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tifffile
import pandas as pd

#endregion imports


#region functions

#get the voxel size
def get_voxel_size(tags, dimension):

    #make sure the dimension is either XResolution or YResolution
    if dimension not in ['XResolution', 'YResolution']:
        return 0
    
    #get the number of pixels and the units
    if dimension in tags:

        number_of_pixels, units = tags[dimension].value

        #print the number of pixels
        print(f'{dimension} number of pixels: {number_of_pixels}')

        #print the units
        print(f'{dimension} units: {units}')

        #return the division
        return units/number_of_pixels

    #print that it is not in the dimensions
    print(f'{dimension} is not in the tags')

    #return 0
    return 0    
    

#endregion functions


#if name is main
if __name__ == "__main__":
    
    #get the current directory
    current_directory = os.getcwd()

    #get the list of file in the current directory
    file_list = os.listdir(current_directory)
    tif_files = [tiff_file for tiff_file in file_list if tiff_file.endswith('_str.tif')]

    #loop through the file list
    for tif_file_ing in tif_files:
        
        #get the tif file
        tif_file = tif_file_ing

        #print a space
        print('')

        #print the file name
        print(f'File Name: {tif_file}')

        #get the file path
        file_path = os.path.join(current_directory, tif_file)

        #get the file name without extensions by replacing .tif with ''
        file_name_without_extension = tif_file.replace('.tif', '')

        #find out if the _reversed.tif file exists
        if file_name_without_extension + '_reversed.tif' in file_list:

            #set the new file path
            file_path = os.path.join(current_directory, file_name_without_extension + '_reversed.tif')

            #set the tif file
            tif_file = file_name_without_extension + '_reversed.tif'

            #set the new file name without extension
            file_name_without_extension = file_name_without_extension + '_reversed'

        #load the tiff file with the tifffile library
        loaded_tiff_file = tifffile.imread(file_path)

        #get the imagej metadata from the tiff file
        imagej_metadata = tifffile.TiffFile(file_path).imagej_metadata

        #start the variables of the image
        image_unit = None
        image_spacing = None
        image_slices = None
        image_x_pixel_size = None
        image_y_pixel_size = None
        image_channel_number = None
        image_width = None
        image_height = None

        #get the unit
        if "unit" in imagej_metadata:
            image_unit = imagej_metadata['unit']
        else: 
            image_unit = 'micron'
        
        #get the spacing
        if "spacing" in imagej_metadata:
            image_spacing = imagej_metadata['spacing']
        else:
            image_spacing = None

        #get the slices
        if "slices" in imagej_metadata:
            image_slices = imagej_metadata['slices']
        else:
            image_slices = None

        #get the number of channels
        if "channels" in imagej_metadata:
            image_channel_number = imagej_metadata['channels']
        else:
            image_channel_number = None

        #get the tiff tags
        tiff_tags = tifffile.TiffFile(file_path).pages[0].tags

        #get the image x resolution
        image_x_pixel_size = get_voxel_size(tiff_tags, 'XResolution')

        #get the image y resolution
        image_y_pixel_size = get_voxel_size(tiff_tags, 'YResolution')

        #set the iamge width
        image_width = loaded_tiff_file.shape[-1]

        #set the image height
        image_height = loaded_tiff_file.shape[-2]

        #create the numpy array that will hold the values
        average_image_numpy = np.zeros((image_channel_number, image_height, image_width))

        #start the dictionary that will hold the average values
        pixel_values_dictionary = {}

        #loop through the channels and add an entry to the dictionary
        for channel in range(image_channel_number):

            pixel_values_dictionary["channel"+str(channel+1)] = {"sum":0, "above_0_count":0, "average_value":0}

        #loop through the channels
        for channel in range(image_channel_number):
    
            #loop through the image width
            for x_coord in range(image_width):

                #loop through the image height
                for y_coord in range(image_height):

                    #restart the pixel value
                    pixel_values_dictionary["channel"+str(channel+1)]["sum"] = 0
                    pixel_values_dictionary["channel"+str(channel+1)]["above_0_count"] = 0
                    pixel_values_dictionary["channel"+str(channel+1)]["average_value"] = 0

                    #loop through the slices
                    for z_coord in range(image_slices):
                        
                        #get the pixel value
                        pixel_value = loaded_tiff_file[z_coord, channel, y_coord, x_coord]

                        #if the pixel value is above 0
                        if pixel_value > 0:

                            #add it to the sum
                            pixel_values_dictionary["channel"+str(channel+1)]["sum"] += pixel_value

                            #add 1 to the above 0 count
                            pixel_values_dictionary["channel"+str(channel+1)]["above_0_count"] += 1

                    #if the above 0 count is above 0
                    if pixel_values_dictionary["channel"+str(channel+1)]["above_0_count"] > 0:

                        #get the average value
                        pixel_values_dictionary["channel"+str(channel+1)]["average_value"] = pixel_values_dictionary["channel"+str(channel+1)]["sum"]/pixel_values_dictionary["channel"+str(channel+1)]["above_0_count"]

                    #add the average value to the numpy array
                    average_image_numpy[channel, y_coord, x_coord] = pixel_values_dictionary["channel"+str(channel+1)]["average_value"]

        #get a name in the meantime
        save_name = file_name_without_extension + '_avg_proj.tif'

        #get the save path
        save_path = os.path.join(current_directory, save_name)

        #make the average image numpy array a float32
        average_image_numpy = average_image_numpy.astype(np.float32)

        #print the image_y_pixel_size
        print(f'image_y_pixel_size: {image_y_pixel_size}')

        #print the image_x_pixel_size
        print(f'image_x_pixel_size: {image_x_pixel_size}')

        #if the image_y_pixel_size is 0 or the image_x_pixel_size is 0
        if image_y_pixel_size == 0 or image_x_pixel_size == 0:
    
            #save without resolution
            tifffile.imwrite(save_path, average_image_numpy, imagej=True, metadata={'axes': 'CYX', 'unit': image_unit, 'spacing': image_spacing, 'slices': image_slices, 'channels': image_channel_number})

        #else
        else:

            #save the average image numpy array
            tifffile.imwrite(save_path, average_image_numpy, resolution=(1./image_x_pixel_size, 1./image_y_pixel_size), imagej=True, metadata={'axes': 'CYX', 'unit': image_unit, 'spacing': image_spacing, 'slices': image_slices, 'channels': image_channel_number})

    #print that the program is done
    print('Done')