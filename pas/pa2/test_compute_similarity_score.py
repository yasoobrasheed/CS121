# CS121: Schelling Model of Housing Segregation
# 

# Automatically added to test code for compute_similarity_score

# Handle the fact that the test code may not be in the same directory
# as schelling.py

import os
import sys

sys.path.append(os.getcwd())

import schelling
import pytest
import utility
import math

EPS = 0.000001

def helper_test_compute_similarity_score(filename, R, location, expected):
    '''
    Check result of calling compute_similarity_score on the specified
    location with in an R-neighborhood with the specified threshold.

    Inputs:
        filename: (string) name of the input grid file
        R: (integer) neighborhood parameter
        location: (pair of integers) location in the grid to be tested
        expected: (float) expected result.
    '''
    grid = utility.read_grid(filename)

    actual = schelling.compute_similarity_score(grid, R, location)
    if abs(actual - expected) > EPS or \
       (math.isnan(actual) and not math.isnan(expected)) or \
       (not math.isnan(actual) and math.isnan(expected)):

        s = "Actual value ({}) is not equal to the expected value ({}).\n"
        s = s + "    @ location {} with R-{:d} neighborhoods.\n"
        pytest.fail(s.format(actual, expected, location, R))

# Generated code



def test_0():
    # Check boundary neighborhood:top left corner.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 0, (0, 0), 1.0)

def test_1():
    # Check boundary neighborhood:top left corner.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 1, (0, 0),
                                                      0.6666666666666666)

def test_2():
    # Check boundary neighborhood: top left corner.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 2, (0, 0),
                                                      0.7142857142857143)

def test_3():
    # Check boundary neighborhood: top right corner.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 0, (0, 4), 1.0)

def test_4():
    # Check boundary neighborhood: top right corner.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 1, (0, 4),
                                                      0.6666666666666666)

def test_5():
    # Check boundary neighborhood: top right corner.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 2, (0, 4),
                                                      0.5714285714285714)

def test_6():
    # Check boundary neighborhood: lower left corner.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 0, (4, 0), 1.0)

def test_7():
    # Check boundary neighborhood: lower left corner.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 1, (4, 0), 0.75)

def test_8():
    # Check boundary neighborhood: lower left corner.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 2, (4, 0),
                                                      0.4444444444444444)

def test_9():
    # Check interior R-0 neighborhood.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 0, (1, 1), 1.0)

def test_10():
    # Check neighborhood that is complete when R is 1.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 1, (1, 1),
                                                      0.2857142857142857)

def test_11():
    # Check neighborhood that is not complete when R is 2.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 2, (1, 1),
                                                      0.46153846153846156)

def test_12():
    # Check neighborhood that corresponds to the whole city.
    filename = "tests/a17-sample-grid.txt"
    helper_test_compute_similarity_score(filename, 2, (2, 2), 0.55)

def test_13():
    # Check interior neighborhood with location that has no other neighbors.
    filename = "tests/grid-no-neighbors.txt"
    helper_test_compute_similarity_score(filename, 1, (2, 2), 1.0)

def test_14():
    # Check boundary neighborhood (lower right corner) with location that
    # has no other neighbors.
    filename = "tests/grid-no-neighbors.txt"
    helper_test_compute_similarity_score(filename, 1, (4, 4), 1.0)

def test_15():
    # Check boundary neighborhood (lower right corner) with location that
    # has a few neighbors.
    filename = "tests/grid-no-neighbors.txt"
    helper_test_compute_similarity_score(filename, 2, (4, 4), 0.25)

