import math
import pylab
import numpy


def sinc(x):
    if x != 0:
        return math.sin(x) / x
    else:
        return 1


def plot_sinc():
    # Compute Xs using range or numpy.arange
    # Compute Ys using a loop
    # Call plot
    # Call show
    # remove the next line
    
    X = range(-10, 10)
    Y = []
    for each in X:
        Y.append(sinc(X))

plot_sinc()
