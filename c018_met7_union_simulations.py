"""

This sill run a simulation to test the frequency of the union and short arm designation to that site. 

"""

#region ################################ IMPORTS ################################

#import the random module
import pickle
import random
import argparse
import matplotlib.pyplot as plt

#endregion ############################# IMPORTS ################################

#region ################################ METHODS ################################

#function to generate the crossover positions
def generateCrossoverPositions(current_main_border_indexes, megasome_length, co_minimum_distance):

    #start the co_positions list
    co_positions = [None, None]

    #start the co_counter
    co_counter = 0

    #start the while loop for the crossover counter less than 2
    while co_counter < 2:

        #get the random crossover position by getting a random int between 1 and the megasome length -2
        random_crossover_position = random.randint(1, megasome_length-2)

        #if the random crossover position is not in the current main border indexes
        if random_crossover_position not in current_main_border_indexes:
            
            #set the valid flag to true
            valid_flag = True

            #if the co counter is 1
            if co_counter == 1:

                #get the first crossover position
                first_crossover_position = co_positions[0]

                #get the absolute difference between the random crossover position and the first crossover position
                absolute_difference = abs(random_crossover_position - first_crossover_position)

                #if the absolute difference is less than the co minimum distance
                if absolute_difference < co_minimum_distance:

                    #set the valid flag to false
                    valid_flag = False

            #if the valid flag is true
            if valid_flag == True:
            
                #set the co position to the random crossover position
                co_positions[co_counter] = random_crossover_position

                #increment the co counter
                co_counter += 1

    #sort the co positions
    co_positions.sort()

    #return the co positions
    return co_positions.copy()


def run_union_simulation(number_of_cycles, interference_factor):

    #get the category dictionary
    category_dictinary = {
        1: [1,1],
        2: [1,2],
        3: [1,3],
        4: [1,4],
        5: [1,5],
        6: [2,1],
        7: [2,2],
        8: [2,3],
        #the key value pairs is as follows:
        #left_end = 1
        #union_1 = 2
        #union_2 = 3
        #right_end = 4
        #other_co = 5
        9: [2,4],
        10: [2,5],
        11: [3,1],
        12: [3,2],
        13: [3,3],
        14: [3,4],
        15: [3,5],
        16: [4,1],
        17: [4,2],
        18: [4,3],
        19: [4,4],
        20: [4,5],
        21: [5,1],
        22: [5,2],
        23: [5,3],
        24: [5,4],
        25: [5,5]
    }

    #union coords list
    union_coords = [1, 138, 315, 490]

    #set the single chromosome length
    avg_single_chromosome_length = 138 * interference_factor

    #set the megasome length
    megasome_length = 490

    #create a list of the results
    results = []

    #loop through the number of cycles
    for cycle in range(number_of_cycles):

        #get the first crossover position by getting a random int between 1 and the megasome length
        first_crossover_position = random.randint(2, megasome_length-1)

        #set the second crossover position to 0
        second_crossover_position = 0

        #set the crossover difference bool
        crossover_difference = False

        #get the second crossover position from a while loop
        while crossover_difference == False:

            #get the second crossover position
            second_crossover_position = random.randint(2, megasome_length-1)

            #get the absolute difference to the first crossover position
            absolute_difference = abs(first_crossover_position - second_crossover_position)

            #if the absolute difference is greater than the single chromosome length
            if absolute_difference > avg_single_chromosome_length:

                #set the crossover difference to true
                crossover_difference = True
        
        #if the first crossover position is greater than the second crossover position
        if first_crossover_position > second_crossover_position:

            #flip them
            first_crossover_position, second_crossover_position = second_crossover_position, first_crossover_position

        #the key value pairs is as follows:
        #left_end = 1
        #union_1 = 2
        #union_2 = 3
        #right_end = 4
        #other_co = 5

        #get the difference dictionary for co_1
        co1_difference_list = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }

        #get the difference dictionary for co_2
        co2_difference_list = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }

        #calculate the difference for left end
        co1_difference_list[1] = abs(first_crossover_position - union_coords[0])

        #calculate the difference for union 1
        co1_difference_list[2] = abs(first_crossover_position - union_coords[1])

        #calculate the difference for union 2
        co1_difference_list[3] = abs(first_crossover_position - union_coords[2])

        #calculate the difference for right end
        co1_difference_list[4] = abs(first_crossover_position - union_coords[3])

        #calculate the difference for other co
        co1_difference_list[5] = abs(first_crossover_position - second_crossover_position)/2

        #calculate the difference for left end
        co2_difference_list[1] = abs(second_crossover_position - union_coords[0])

        #calculate the difference for union 1
        co2_difference_list[2] = abs(second_crossover_position - union_coords[1])

        #calculate the difference for union 2
        co2_difference_list[3] = abs(second_crossover_position - union_coords[2])

        #calculate the difference for right end
        co2_difference_list[4] = abs(second_crossover_position - union_coords[3])

        #calculate the difference for other co
        co2_difference_list[5] = co1_difference_list[5]



        #get the col1 min key
        co1_min_key = 0

        #get the co1 min value
        co1_min_value = 490

        #loop throumegasomegh the co1 difference list
        for key, value in co1_difference_list.items():

            #if the value is less than the min value
            if value < co1_min_value:

                #set the min value to the value
                co1_min_value = value

                #set the min key to the key
                co1_min_key = key

        #get the col2 min key
        co2_min_key = 0

        #get the co2 min value
        co2_min_value = 490

        #loop through the co2 difference list
        for key, value in co2_difference_list.items():

            #if the value is less than the min value
            if value < co2_min_value:

                #set the min value to the value
                co2_min_value = value

                #set the min key to the key
                co2_min_key = key
        
        #loop through the category dictionary
        for key, value in category_dictinary.items():

            #get the value 0
            value_0 = value[0]

            #get the value 1
            value_1 = value[1]

            #if the co1 min key is equal to the value 0 and the co2 min key is equal to the value 1
            if co1_min_key == value_0 and co2_min_key == value_1:

                #append the key to the results
                results.append(key)      

    #get the list without duplicates values with the count for each one
    results_list = [[x, results.count(x)] for x in set(results)] 

    #loop through the results list
    for list_unit in results_list:

        #get the second value
        ratio_of_total = list_unit[1]/number_of_cycles

        #append the ratio of total to the list
        list_unit.append(ratio_of_total)

    #print the results list
    print(results_list)


#run the union as border prediction
def run_union_as_border_prediction(number_of_cycles, megasome_length, interference_distance, main_border_indexes):
    
    #print that it is being run
    print("Running the union as border prediction")

    #make the returning results dictionary
    returning_results_dictionary = {}

    #get the category dictionary
    category_dictionary = {

        #set the category 1
        1:[["Undecided","Undecided"], ["Right","Undecided"], ["Left","Undecided"], ["Undecided","Left"], ["Undecided","Right"]],
        #set the category 2
        2:[["Left","Right"]],
        #set the category 3
        3:[["Right","Left"]],
        #set the category 4
        4:[["Right","Right"], ["Left","Left"]]
    
    }

    #get the minimum distance between the crossover positions
    co_minimum_distance = interference_distance

    #make the loop for the number of cycles
    for cycle in range(number_of_cycles):

        #print a space
        print("")

        #print the cycle
        print(f"Cycle: {cycle}")
        
        #generate the crossover positions
        crossover_positions = generateCrossoverPositions(main_border_indexes.copy(), megasome_length, co_minimum_distance)

        #start a new list to hold the restriction directions
        restriction_directions = []

        #loop through the enumeration of the crossover positions
        for index_co, crossover_position in enumerate(crossover_positions):

            #make a new list to hold the current crossover border indexes
            current_crossover_border_indexes = main_border_indexes.copy()

            #append the other crossover position to the current crossover border indexes
            if index_co == 0:
                current_crossover_border_indexes.append(crossover_positions[1])

            #if the index is 1
            if index_co == 1:
                current_crossover_border_indexes.append(crossover_positions[0])

            #start the relative distances list
            relative_distances_list = []

            #loop through the current crossover border indexes
            for border_index in current_crossover_border_indexes:

                #get the relative distance by getting the absolute difference between the crossover position and the border index
                relative_distance = abs(crossover_position - border_index)

                #if it is the last border index
                if border_index == current_crossover_border_indexes[-1]:

                    #append the relative distance to the relative distances list
                    #modify this to /2 if simulating not union as border
                    relative_distances_list.append(relative_distance)
                    #relative_distances_list.append(relative_distance/2)

                else:

                    #append the relative distance to the relative distances list
                    relative_distances_list.append(relative_distance)

            #get the index of the minimum relative distance
            min_relative_distance = megasome_length

            min_relative_distance_index = -1

            #loop through the enumeration of the relative distances list
            for index, relative_distance in enumerate(relative_distances_list):

                #if the relative distance is less than the min relative distance
                if relative_distance < min_relative_distance:

                    #set the min relative distance to the relative distance
                    min_relative_distance = relative_distance

                    #set the min relative distance index to the index
                    min_relative_distance_index = index

            #if the min relative distance is more than once in the relative distances list
            if relative_distances_list.count(min_relative_distance) > 1:

                #append undecided to the restriction directions
                restriction_directions.append("Undecided")

                #continue to the next iteration
                continue

            #if the min relative distance index is 0
            if min_relative_distance_index == 0:

                #append left to the restriction directions
                restriction_directions.append("Left")

            #if the min relative distance index is 3
            if min_relative_distance_index == 3:

                #append right to the restriction directions
                restriction_directions.append("Right")

            #print the index
            print(f"Index: {index}")
            
            #if the min relative distance is 4
            if min_relative_distance_index == 4:

                #if the index is 0, append right to the restriction directions
                if index_co == 0:
                    
                    #append right to the restriction directions
                    restriction_directions.append("Right")

                #if the index is 1, append left to the restriction directions
                if index_co == 1:

                    #append left to the restriction directions
                    restriction_directions.append("Left")

            #if the min relative distance is 1 or 2
            if min_relative_distance_index == 1 or min_relative_distance_index == 2:

                #get the comparing border
                comparing_border = current_crossover_border_indexes[min_relative_distance_index]

                #if the crossover position is less than the comparing border
                if crossover_position < comparing_border:

                    #append left to the restriction directions
                    restriction_directions.append("Right")

                #if the crossover position is greater than the comparing border
                if crossover_position > comparing_border:

                    #append right to the restriction directions
                    restriction_directions.append("Left")

        #get the type of category
        category_type = None

        #if there's at least one "Undecided" in the restriction directions
        if "Undecided" in restriction_directions:

            #set the category type to 1
            category_type = 1

        #loop through the category dictionary
        for key, value in category_dictionary.items():

            #if the restriction directions is equal to the value
            if restriction_directions in value:

                #set the category type to the key
                category_type = key

        #if the category type is None
        if category_type == None:

            #print the crossover positions
            print(f"Crossover positions: {crossover_positions}")

            #print the direction
            print(f"Direction: {restriction_directions}")

            #print the main_border_indexes
            print(f"Main border indexes: {main_border_indexes}")

            exit()

        #add the cycle to the returning results dictionary
        returning_results_dictionary[cycle] = {"crossover_positions": crossover_positions, "restriction_directions": restriction_directions, "category": category_type}

    #return the returning results dictionary
    return returning_results_dictionary

#run the union as border prediction
def run_union_as_border_prediction_no_other_co(number_of_cycles, megasome_length, interference_distance, main_border_indexes):
    
    #print that it is being run
    print("Running the union as border prediction")

    #make the returning results dictionary
    returning_results_dictionary = {}

    #get the category dictionary
    category_dictionary = {

        #set the category 1
        1:[["Undecided","Undecided"], ["Right","Undecided"], ["Left","Undecided"], ["Undecided","Left"], ["Undecided","Right"]],
        #set the category 2
        2:[["Left","Right"]],
        #set the category 3
        3:[["Right","Left"]],
        #set the category 4
        4:[["Right","Right"], ["Left","Left"]]
    
    }

    #get the minimum distance between the crossover positions
    co_minimum_distance = interference_distance

    #make the loop for the number of cycles
    for cycle in range(number_of_cycles):

        #print a space
        print("")

        #print the cycle
        print(f"Cycle: {cycle}")
        
        #generate the crossover positions
        crossover_positions = generateCrossoverPositions(main_border_indexes.copy(), megasome_length, co_minimum_distance)

        #start a new list to hold the restriction directions
        restriction_directions = []

        #loop through the enumeration of the crossover positions
        for index_co, crossover_position in enumerate(crossover_positions):

            #make a new list to hold the current crossover border indexes
            current_crossover_border_indexes = main_border_indexes.copy()

            #start the relative distances list
            relative_distances_list = []

            #loop through the current crossover border indexes
            for border_index in current_crossover_border_indexes:

                #get the relative distance by getting the absolute difference between the crossover position and the border index
                relative_distance = abs(crossover_position - border_index)

                #append the relative distance to the relative distances list
                relative_distances_list.append(relative_distance)

            #get the index of the minimum relative distance
            min_relative_distance = megasome_length

            min_relative_distance_index = -1

            #loop through the enumeration of the relative distances list
            for index, relative_distance in enumerate(relative_distances_list):

                #if the relative distance is less than the min relative distance
                if relative_distance < min_relative_distance:

                    #set the min relative distance to the relative distance
                    min_relative_distance = relative_distance

                    #set the min relative distance index to the index
                    min_relative_distance_index = index

            #if the min relative distance is more than once in the relative distances list
            if relative_distances_list.count(min_relative_distance) > 1:

                #append undecided to the restriction directions
                restriction_directions.append("Undecided")

                #continue to the next iteration
                continue

            #if the min relative distance index is 0
            if min_relative_distance_index == 0:

                #append left to the restriction directions
                restriction_directions.append("Left")

            #if the min relative distance index is 3
            if min_relative_distance_index == 3:

                #append right to the restriction directions
                restriction_directions.append("Right")

            #if the min relative distance is 1 or 2
            if min_relative_distance_index == 1 or min_relative_distance_index == 2:

                #get the comparing border
                comparing_border = current_crossover_border_indexes[min_relative_distance_index]

                #if the crossover position is less than the comparing border
                if crossover_position < comparing_border:

                    #append left to the restriction directions
                    restriction_directions.append("Right")

                #if the crossover position is greater than the comparing border
                if crossover_position > comparing_border:

                    #append right to the restriction directions
                    restriction_directions.append("Left")

        #get the type of category
        category_type = None

        #if there's at least one "Undecided" in the restriction directions
        if "Undecided" in restriction_directions:

            #set the category type to 1
            category_type = 1

        #loop through the category dictionary
        for key, value in category_dictionary.items():

            #if the restriction directions is equal to the value
            if restriction_directions in value:

                #set the category type to the key
                category_type = key

        #add the cycle to the returning results dictionary
        returning_results_dictionary[cycle] = {"crossover_positions": crossover_positions, "restriction_directions": restriction_directions, "category": category_type}

    #return the returning results dictionary
    return returning_results_dictionary


#endregion ############################# METHODS ################################

#region ################################# MAIN ##################################

#if name is main
if __name__ == "__main__":

    #set the number of cycles
    number_of_cycles = None

    #set the interference factor
    interference_distance = None

    #set the chromosome lengths
    chr_III = 138
    chr_X = 177
    chr_IV = 175

    #set the megasome length
    megasome_length = chr_III + chr_X + chr_IV

    #set the border indexes
    main_border_indexes = [0, chr_III-1, chr_III+chr_X-1, megasome_length-1]

    #create an argument parser
    parser = argparse.ArgumentParser(description="Run a simulation to test the frequency of the union and short arm designation to that site.")

    #add the arguments 
    parser.add_argument("-c", "--cycles", help="The number of cycles to run the simulation", type=int, default=100)

    #add the arguments for the interference distance
    parser.add_argument("-id", "--interferencedistance", help="The interference distance", type=int, default=chr_III)

    #parse the arguments
    args = parser.parse_args()

    #set the number of cycles
    number_of_cycles = args.cycles

    #set the interference factor
    interference_distance = args.interferencedistance

    #print the number of cycles
    print(f"Number of cycles: {number_of_cycles}")

    #print the megasome length
    print(f"Megasome length: {megasome_length}")

    #print the border indexes
    print(f"Border indexes: {main_border_indexes}")

    #print the interference distance
    print(f"Interference distance: {interference_distance}")

    #print a ""
    print("")

    #get the results dictionary
    results_dictionary = run_union_as_border_prediction(number_of_cycles, megasome_length, interference_distance, main_border_indexes)

    #make the figure
    fig, ax = plt.subplots()

    #make the plot symmetric
    ax.set_aspect('equal')

    #get the origin coordinate
    origin_coordinate = [0, 0]

    #get the co_2_end_coordinate
    co_2_end_coordinate = [1, 0]

    #get the co_1_end_coordinate
    co_1_end_coordinate = [0, 1]

    #get the center coordinate
    center_coordinate = [0.25,0.25]

    #get the co_2_end to center coordinate slope
    co_2_end_to_center_slope = (center_coordinate[1] - co_2_end_coordinate[1])/(center_coordinate[0] - co_2_end_coordinate[0])

    #get the co_1_end to center coordinate slope
    co_1_end_to_center_slope = (center_coordinate[1] - co_1_end_coordinate[1])/(center_coordinate[0] - co_1_end_coordinate[0])

    #get the co_2_to_center_b
    co_2_to_center_b = co_2_end_coordinate[1] - (co_2_end_to_center_slope*co_2_end_coordinate[0])

    #get the co_1_to_center_b
    co_1_to_center_b = co_1_end_coordinate[1] - (co_1_end_to_center_slope*co_1_end_coordinate[0])

    #get the co_1_cutting_point 
    co_1_cutting_point = [0,co_2_to_center_b]

    #get the co_2_cutting_point
    co_2_cutting_point = [((-1*co_1_to_center_b)/co_1_end_to_center_slope),0]

    #make the lines
    plt.plot([origin_coordinate[0], co_2_end_coordinate[0]], [origin_coordinate[1], co_2_end_coordinate[1]], color="black")

    plt.plot([origin_coordinate[0], co_1_end_coordinate[0]], [origin_coordinate[1], co_1_end_coordinate[1]], color="black")

    plt.plot([co_1_end_coordinate[0], co_2_end_coordinate[0]], [co_1_end_coordinate[1], co_2_end_coordinate[1]], color="black")

    #plot the co_1_cutting_line
    plt.plot(co_2_end_coordinate, co_1_cutting_point, color="black")

    #plot the co_2_cutting_line
    plt.plot(co_2_cutting_point, co_1_end_coordinate, color="black")

    #get the yellow polygon points
    yellow_polygon_points = [origin_coordinate, co_2_cutting_point, center_coordinate, co_1_cutting_point]

    #get the blue polygon left points
    blue_polygon_left_points = [co_2_cutting_point, co_2_end_coordinate, center_coordinate]

    #get the blue polygon right points
    blue_polygon_right_points = [center_coordinate, co_1_end_coordinate, co_1_cutting_point]

    #get the green polygon points
    green_polygon_points = [center_coordinate, co_2_end_coordinate, co_1_end_coordinate]

    #make the gray polygon points
    gray_polygon_points = [[1-(chr_III/megasome_length),0],co_2_end_coordinate, co_1_end_coordinate, [0,1-(chr_III/megasome_length)]]

    #plot the yellow polygon
    yellow_polygon = plt.Polygon(yellow_polygon_points, color="yellow", alpha=0.2)

    #plot the blue polygon left
    blue_polygon_left = plt.Polygon(blue_polygon_left_points, color="blue", alpha=0.2)

    #plot the blue polygon right
    blue_polygon_right = plt.Polygon(blue_polygon_right_points, color="blue", alpha=0.2)

    #plot the green polygon
    green_polygon = plt.Polygon(green_polygon_points, color="green", alpha=0.2)

    #plot the gray polygon
    gray_polygon = plt.Polygon(gray_polygon_points, color="gray", alpha=0.2)

    #add the polygons to the plot
    ax.add_patch(yellow_polygon)

    ax.add_patch(blue_polygon_left)

    ax.add_patch(blue_polygon_right)

    ax.add_patch(green_polygon)

    ax.add_patch(gray_polygon)

    #make the points specs
    point_specs = {
        1:{"shape":"o", "color":"black", "edgecolor":"black", "alpha":1, "plotting":False, "size":200, "edge_width":2},
        2:{"shape":"o", "color":"gold", "edgecolor":"black", "alpha":1, "plotting":True, "size":200, "edge_width":2},
        3:{"shape":"s", "color":"green", "edgecolor":"black", "alpha":1, "plotting":True, "size":200, "edge_width":2},
        4:{"shape":"*", "color":"slateblue", "edgecolor":"black", "alpha":1, "plotting":True, "size":400, "edge_width":2}
    }

    #get the n counter
    n_counter = 0

    #get the category 1 counter
    category_1_counter = 0

    #loop through the results dictionary
    for result in results_dictionary:

        #get the result coordinates
        result_coordinates = results_dictionary[result]["crossover_positions"]

        #get the category
        category = results_dictionary[result]["category"]

        #get the normalized coordinates
        normalized_coordinates = [(result_coordinates[0]+1)/megasome_length, (result_coordinates[1]+1)/megasome_length]

        #if the category is None
        if category == None:

            #print the crossover positions
            print(f"Crossover positions: {result_coordinates}")

            #print the direction
            print(f"Direction: {results_dictionary[result]['restriction_directions']}")

            exit()

        #print the category
        print(f"Category: {category}")
        
        #get the point shape based on the category
        point_shape = point_specs[category]["shape"]

        #get the point color based on the category
        point_color = point_specs[category]["color"]

        #get the point edge color based on the category
        point_edgecolor = point_specs[category]["edgecolor"]

        #get the point alpha based on the category
        point_alpha = point_specs[category]["alpha"]

        #get the point plotting based on the category
        point_plotting = point_specs[category]["plotting"]

        #get the point size based on the category
        point_size = point_specs[category]["size"]

        #get the point edge width based on the category
        point_edge_width = point_specs[category]["edge_width"]

        #get the x coordinate 
        x_coordinate = 1 - normalized_coordinates[1]

        #get the y coordinate
        y_coordinate = normalized_coordinates[0]

        #if the point is plotting
        if point_plotting == True:

            #plot the point
            plt.scatter(x_coordinate, y_coordinate, marker=point_shape, color=point_color, edgecolor=point_edgecolor, alpha=point_alpha, s=point_size, linewidth=point_edge_width)

            #increment the n counter
            n_counter += 1

    #save the plot as a png and pdf
    plt.savefig("c018_megasome_unions_co_counts_100xs_unions_138_177_175_interference_138_n_"+str(n_counter)+"_co_border_half.png", dpi=300)
    plt.savefig("c018_megasome_unions_co_counts_100xs_unions_138_177_175_interference_138_n_"+str(n_counter)+"_co_border_half.pdf", dpi=300)

    #save the returning dictionary as a pickle
    pickle.dump(results_dictionary, open("c018_megasome_unions_co_counts_100xs_unions_138_177_175_interference_138_n_"+str(n_counter)+"_co_border_half.pkl", "wb"))

    #show the plot
    plt.show()

    exit()

    #run the method
    run_union_simulation(number_of_cycles, interference_factor)

#endregion ############################## MAIN #################################