# CS121 Lab 3: Functions

import math

# Your distance function goes here 
<<<<<<< HEAD
def dist(first_coor, second_coor):
    x_1 = first_coor[0]
    x_2 = first_coor[1]
    y_1 = second_coor[0]
    y_2 = second_coor[1]
    return math.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)


# Your perimeter function goes here 
def perimeter(first_coor, second_coor, third_coor):
    side_1 = dist(first_coor, second_coor)
    side_2 = dist(second_coor, third_coor)
    side_3 = dist(third_coor, first_coor)

    return side_1 + side_2 + side_3


def go():
    print("distance: " + str(dist((0, 1), (1, 0))))
    print("perimeter: " + str(perimeter((-1, 0), (0, 1), (1, 0))))
=======

# Your perimeter function goes here 

def go():
    '''
    Write a small amount of code to verify that your functions work

    Verify that the distance between the points (0, 1) and (1, 0) is
    close to math.sqrt(2)

    After that is done, verify that the triangle with vertices at 
    (0, 0), (0, 1), (1, 0) has a perimeter 2 + math.sqrt(2)
    '''

    # replace the pass with code that calls your functions
    # and prints the results
    pass

if __name__ == "__main__":
    go()
    
                

>>>>>>> 5948107c6aa4a0fae598e416d34f75c6afb0e3b7
