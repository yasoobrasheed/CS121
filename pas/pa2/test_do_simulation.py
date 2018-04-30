# CS121: Schelling Model of Housing Segregation
# 
# Test code for do_simulation
#

import os
import sys

timeout=60

# Handle the fact that the grading code may not
# be in the same directory as schelling.py
sys.path.append(os.getcwd())

# Get the test files from the same directory as
# this file.
BASE_DIR = os.path.dirname(__file__)


from schelling import do_simulation
import pytest
import utility

def count_homeowners(grid):
    '''
    Count the number of occupied homes:

    Inputs:
        grid: (list of lists of strings) the grid

    Returns: integer
    '''

    num_homeowners = 0
    for row in grid:
        for home in row:
            if home != "O":
                num_homeowners += 1
    return num_homeowners


def helper(input_filename, expected_filename, R, threshold, 
           max_num_steps, expected_num_relocations):
    '''
    Do one simulation with the specified parameters (R, threshold,
    max_num_steps) starting from the specified input file.  Match
    actual grid generated with the expected grid and match expected
    steps and actual steps.

    Inputs:
        input_filename: (string) name of the input grid file
        expected_filename: (string) name of the expected grid file.
        R: (int) radius for the neighborhood
        threshold: (float) satisfaction threshold
        max_steps: (int) maximum number of steps to do
        expected_num_relocations: (int) expected number of relocations
            performed during the simulation
    '''

    input_filename = os.path.join(BASE_DIR, input_filename)
    actual_grid = utility.read_grid(input_filename)
    expected_num_homeowners = count_homeowners(actual_grid)

    actual_num_steps = do_simulation(actual_grid, R, threshold, 
                                     max_num_steps)
    actual_num_homeowners = count_homeowners(actual_grid)

    expected_filename = os.path.join(BASE_DIR, expected_filename)
    expected_grid = utility.read_grid(expected_filename)

    if actual_num_steps != expected_num_relocations:
        s = ("actual and expected values number of steps do not match\n"
             "  got {:d}, expected {:d}")
        s = s.format(actual_num_steps, expected_num_relocations)
        pytest.fail(s)

    if actual_num_homeowners != expected_num_homeowners:
        if actual_num_homeowners <= expected_num_homeowners:
            s = "Homeowners are fleeing the city!\n"
        else:
            s = "City is gaining homeowners.\n"
        msg_num_owners = "number of homeowners: {:d}\n"
        s += ("  Actual " + msg_num_owners).format(actual_num_homeowners)
        s += ("  Expected " + msg_num_owners).format(expected_num_homeowners)
        pytest.fail(s)
        
    mismatch = utility.find_mismatch(actual_grid, expected_grid)
    if mismatch:
        (i, j) = mismatch
        s = ("actual and expected grid values do not"
              + " match at location ({:d}, {:d})\n")
        s = s.format(i, j)
        s = s + "  got {}, expected {}".format( actual_grid[i][j],
                                                expected_grid[i][j] )
        pytest.fail(s)

def test_0():
    # Check stopping condition #1
    input_fn = "tests/a17-sample-grid.txt"
    output_fn = "tests/a17-sample-grid-1-44-0-final.txt"
    helper(input_fn, output_fn, 1, 0.44, 0, 0)

def test_1():
    # Check stopping condition #2
    input_fn = "tests/a17-sample-grid.txt"
    output_fn = "tests/a17-sample-grid-1-20-2-final.txt"
    helper(input_fn, output_fn, 1, 0.2, 2, 0)

def test_2():
    # Check choosing among locations with acceptable similarity score.
    input_fn = "tests/grid-several-sat-first.txt"
    output_fn = "tests/grid-several-sat-first-1-20-2-final.txt"
    helper(input_fn, output_fn, 1, 0.2, 2, 1)

def test_3():
    # Check choosing among locations with acceptable similarity score.
    input_fn = "tests/grid-several-sat-middle.txt"
    output_fn = "tests/grid-several-sat-middle-1-20-2-final.txt"
    helper(input_fn, output_fn, 1, 0.2, 2, 1)

def test_4():
    # Check choosing among locations with same similarity score.
    input_fn = "tests/grid-ties.txt"
    output_fn = "tests/grid-ties-1-20-2-final.txt"
    helper(input_fn, output_fn, 1, 0.2, 2, 1)

def test_5():
    # Check case where there no suitable homes.
    input_fn = "tests/grid-sea-of-red.txt"
    output_fn = "tests/grid-sea-of-red-1-40-1-final.txt"
    helper(input_fn, output_fn, 1, 0.4, 1, 0)

def test_6():
    # Check case where possible new location is in the
    # homeowner's current neighborhood
    input_fn = "tests/grid-sea-of-red.txt"
    output_fn = "tests/grid-sea-of-red-1-20-1-final.txt"
    helper(input_fn, output_fn, 1, 0.2, 1, 1)

def test_7():
    # Check case where possible new location is in the homeowner's
    # current neighborhood
    input_fn = "tests/grid-sea-of-red.txt"
    output_fn = "tests/grid-sea-of-red-1-30-1-final.txt"
    helper(input_fn, output_fn, 1, 0.3, 1, 0)

def test_8():
    # Check sample grid after 1 simulation step
    input_fn = "tests/a17-sample-grid.txt"
    output_fn = "tests/a17-sample-grid-1-44-1-final.txt"
    helper(input_fn, output_fn, 1, 0.44, 1, 5)

def test_9():
    # Check sample grid after 2 simulation steps
    input_fn = "tests/a17-sample-grid.txt"
    output_fn = "tests/a17-sample-grid-1-44-2-final.txt"
    helper(input_fn, output_fn, 1, 0.44, 2, 7)

def test_10():
    # Check sample grid after 3 simulation steps
    input_fn = "tests/a17-sample-grid.txt"
    output_fn = "tests/a17-sample-grid-1-44-3-final.txt"
    helper(input_fn, output_fn, 1, 0.44, 3, 7)

def test_11():
    # Check stopping condition #2.
    input_fn = "tests/a17-sample-grid.txt"
    output_fn = "tests/a17-sample-grid-2-44-4-final.txt"
    helper(input_fn, output_fn, 2, 0.44, 4, 0)

def test_12():
    # Check sample grid with R of 2
    input_fn = "tests/a17-sample-grid.txt"
    output_fn = "tests/a17-sample-grid-2-44-7-final.txt"
    helper(input_fn, output_fn, 2, 0.44, 7, 0)

@pytest.mark.large
def test_13():
    # Large grid
    input_fn = "tests/large-grid.txt"
    output_fn = "tests/large-grid-2-33-20-final.txt"
    helper(input_fn, output_fn, 2, 0.33, 20, 149)

