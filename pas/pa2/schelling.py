#  CS121: Schelling Model of Housing Segregation
#
#   Program for simulating of a variant of Schelling's model of
#   housing segregation.  This program takes four parameters:
#
#    filename -- name of a file containing a sample city grid
#
#    R - The radius of the neighborhood: home at Location (k, l) is in
#        the neighborhood of the home at Location (i, j)
#        if i-R <= k <= i+R and j-R <= l <= j+R
#
#    threshold - minimum acceptable threshold for ratio of the number
#                of similar neighbors to the number of occupied homes
#                in a neighborhood.
#
#    max_steps - the maximum number of passes to make over the city
#                during a simulation.
#
#  
#    By: Yasoob Rasheed
#

import os
import sys
import utility
import click


# AUXILIARY METHODS FOR COMPUTE_SIMILARITY_SCORE

def generate_neighborhood(grid, R, location):
    # Generate a list with the order of the houses in a given neighborhood "R"
    i = location[0]
    j = location[1]
    neighborhood = []
    
    # Using the eqution given, grab the house at the indices of the neighborhood
    for k in range(0, len(grid)):
        if i - R <= k <= i + R:
            for l in range(0, len(grid[k])):
                if j - R <= l <= j + R:
                    neighborhood.append(grid[k][l])

    return neighborhood


def compute_similarity_score(grid, R, location):
    ''' 
    Compute the similarity score for the homeowner at the specified
    location using a neighborhood of radius R.

    Inputs: 
        grid (list of lists of strings): the grid
        R (int): radius for the neighborhood
        location (pair of ints): a grid location
      
    Returns: float
    '''   
    # I have bypassed writing an assertion that a spot is open
    assert utility.is_grid(grid), "Grid argument is the wrong type"

    # First figure out what color this home is
    home_color = grid[location[0]][location[1]]

    # Next get the neighborhood around this home
    neighborhood = generate_neighborhood(grid, R, location)

    # Next build a counter for each type of home
    same_color_homes = 0.0
    different_color_homes = 0.0

    # Next use an equation to return the similarity score
    for other_home_color in neighborhood:
        if other_home_color == home_color:
            same_color_homes += 1.0
        elif other_home_color != "O":
            different_color_homes += 1.0

    return (same_color_homes) / (different_color_homes + same_color_homes)


# AUXILIARY METHODS FOR DO_SIMULATION

def one_step(grid, R, threshold, open_locations):
    # Run through one entire step and keep track of the number of swaps
    # Variable relocation holds the amount of relocations
    relocations = 0

    for x in range(0, len(grid)):
        for y in range(0, len(grid[x])):
            # 2. Compute homeowner's similarity score
            similarity_score = compute_similarity_score(grid, R, (x, y))
            if grid[x][y] != "O" and similarity_score < threshold:
                # 3. Swap the values at the two locations
                if swap(grid, R, threshold, open_locations, (x, y)) != -1:
                    relocations += 1

    return relocations
    

def swap(grid, R, threshold, open_locations, home_location):
    # 3. Swap the values at the two locations
    # best_similatiry and best_location hold the values of the open location to swap with the house
    # flag is used to make sure that there is a place to swap the house and the open location
    # flag equals False means no and equals True means yes
    best_similarity = 1.0
    best_location = (0, 0)
    x = home_location[0]
    y = home_location[1]
    flag = False
    
    # Loop through the open locations to find the best swap
    for open_location in open_locations:
        i = open_location[0]
        j = open_location[1]
        
        grid[i][j] = grid[x][y]
        grid[x][y] = "O"
        similarity = compute_similarity_score(grid, R, open_location)
        
        # If a potential swap location exists record it
        if threshold <= similarity < best_similarity:
            best_similarity = similarity
            best_location = open_location
            flag = True

        grid[x][y] = grid[i][j]
        grid[i][j] = "O"
    
    # If a swap exists do the swap
    # Delete existing spot from open locations
    # Add old location to open location list
    # Else if no swap exists return that one doesn't exist with a -1
    if flag:
        grid[best_location[0]][best_location[1]] = grid[x][y]
        grid[x][y] = "O"

        index_of_best_location = open_locations.index(best_location)
        del open_locations[index_of_best_location]
        open_locations.append(home_location)
    else:
        return -1


def do_simulation(grid, R, threshold, max_steps):
    '''
    Do a full simulation.

    Inputs:
        grid: (list of lists of strings) the grid
        R: (int) radius for the neighborhood
        threshold: (float) satisfaction threshold
        max_steps: (int) maximum number of steps to do

    Returns:
        (int) The number of relocations completed.
    '''
    assert utility.is_grid(grid), "Grid argument is the wrong type"

    # Steps 1-5 outline the logic of the do_simulation method    
    # 1. Create and initialize the list of open locations
    open_locations = []
    
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            if grid[i][j] == "O":
                open_locations.append((i, j))
    
    # 4. Simulate one step of the simulation
    relocations = 0
    steps = 0
	
    # Keep track of the relocations of one step
    while(steps != max_steps):
        relocations += one_step(grid, R, threshold, open_locations)
        # 5. Run steps until one of the stopping conditions is met: No relocations in a step
        if relocations == 0:
            return relocations
        else:
            steps += 1
    
    # 5. Run steps until one of the stopping conditions is met: Maximum steps reached
    if steps == max_steps:
        return relocations 


@click.command(name="schelling")
@click.option('--grid_file', type=click.Path(exists=True))
@click.option('--r', type=int, default=1, help="neighborhood radius")
@click.option('--threshold', type=float, default=0.44,
                                         help="satisfaction threshold")
@click.option('--max_steps', type=int, default=1)
def go(grid_file, r, threshold, max_steps):
    '''
    Put it all together: do the simulation and process the results.
    '''

    if grid_file is None:
        print("No parameters specified: just loading the code.")
        return

    grid = utility.read_grid(grid_file)

    if len(grid) < 20:
        print("Initial state of city:")
        for row in grid:
            print(row)
        print()

    num_relocations = do_simulation(grid, r, threshold, max_steps)
    print("Number of relocations done: " + str(num_relocations))

    if len(grid) < 20:
        print()
        print("Final state of the city:")
        for row in grid:
            print(row)

if __name__ == "__main__":
    go()
