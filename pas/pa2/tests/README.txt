CS 121: Schelling's Model of Housing Segregation

The grid file format is simple. The first line contains the grid
size. Each subsequent line contains information for a single row,
starting with row 0. A "B" means that the corresponding location has a
blue homeowner, an "R" means that the corresponding location has a red
homeowner, and an "O" means that the location is open.  See the file
``a17-sample-grid.txt``, which contains the initial grid from
the example discussed in the programming assignment.

a17-sample-grid.txt: example from the writeup.

grid-sea-of-red.txt: A grid in which all the homes are
occupied by red homeowners, except two open homes and two home
occupied by blue homeowners.

Examples that use the sample grid from the assignment description:

  a17-sample-grid.txt: original state

  a17-sample-grid-1-44-0-final.txt: result of running simulation with threshold of 44
    and zero steps.

  a17-sample-grid-1-20-2-final.txt: result of running simulation with
    a threshold of 20 for up to two steps.

  Files for step 1 in sample simulation in assignment description: (R-1 neighborhood with 0.44 threshold)
    a17-sample-grid-1-44-1-final.txt: state at the end of step 1 

  Files for step 2 in sample simulation in assignment description:
    (start from a17-sample-grid-1-44-1-final.txt, if you wish to start your
     simulation at the beginning of step 2.)
    a17-sample-grid-1-44-2-final.txt: state at the end of step 2 

  Files for step 3 in sample simulation in assignment description:
    (start from a17-sample-grid-1-44-2-final.txt, if you wish to start your
     simulation at the beginning of step 3.)
    a17-sample-grid-1-44-3-final.txt: state at the end of step 3

  a17-sample-grid-1-44-4-final.txt: result for sample simulation with
    an R-1 neighborhood, a threshold of 0.44, and up to 4 steps.

  a17-sample-grid-2-44-7-final.txt: result for sample simulation with
    an R-2 neighborhood, a threshold of 0.44, and up to 7 steps.


Files for testing possible new location in homeowner's neighborhood:

  grid-sea-of-red.txt: A grid in which most the homes are occupied by
    red homeowners, except two open homes and two homes occupied by
    blue homeowners.

  grid-sea-of-red-1-20-1-final.txt: result of simulation
    with R of 1 and threshold of 0.20.  Homeowner @ (3,3) moves to (2,3)

  grid-sea-of-red-1-30-1-final.txt: result of simulation
    with R of 1 and threshold of 0.30.  No relocations occur

  grid-sea-of-red-1-40-1-final.txt: result of simulation
    with R of 1 and threshold of 0.40.  No relocations occur.

  grid-no-neighbors.txt: A sparsely populated grid used in
    compute_similarity score tests.

  grid-several-sat-first.txt: grid used to test a relocation where the
    homeowner would be satisfied in more than one of the open homes and
    the first one has the best score.
  grid-several-sat-first-1-20-2-final.txt: result of simulating
    2 step on grid-several-sat-first.txt w/ R-1 neighborhood
    and .20 threshold.

  grid-several-sat-middle.txt: grid used to test a relocation where the
    homeowner would be satisfied in more than one of the open homes and
    the middle one has the best score.
  grid-several-sat-middle-1-20-2-final.txt: result of simulating 2
    step on grid-several-sat-middle.txt w/ R-1 neighborhood and .20
    threshold.

  grid-ties.txt: grid used to test a relocation where the homeowner
    would be satisfied in more than one of the open homes and there is a
    tie for the best score.
  grid-ties-1-20-2-final.txt: result of simulating 2
    step on grid-ties.txt w/ R-1 neighborhood and .20
    threshold.


Large grid example:

  large-grid.txt: grid used in large example

  large-grid-2-33-20-final.txt: Result of simulation of R-2
    neighborhood w/ threshold of 0.33 and up to 20 steps.

