# CS121 Linear regression assignment
# Print text answers.
#
import sys
from model import *
from dataset import DataSet

import matplotlib.pyplot as plt
import numpy as np


'''
Prints out the calls to the model instance with the dataset specified
Runs tasks 1a, 1b, 2, 3, 4, and 5

Inputs:
    dataset: DataSet instance

Variables:
    model: instance of the Model class with the dataset specified

Returns: prints out the tasks
'''
def go(dataset):
    model = Model(dataset, dataset.pred_vars)
    
    print(" ")
    print(dataset.dataset_name + " Task 1a:")
    print(" ")
    model.task_one_a()
    print(" ")
    print(dataset.dataset_name + " Task 1b:")
    print(" ")
    model.task_one_b()
    print(" ")
    print(dataset.dataset_name + " Task 2:")
    print(" ")
    model.task_two()
    print(" ")
    print(dataset.dataset_name + " Task 3:")
    print(" ")
    model.task_three()
    print(dataset.dataset_name + " Task 4:")
    print(" ")
    model.task_four()
    print(" ")
    print(dataset.dataset_name + " Task 5:")
    print(" ")
    model.task_five()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 output <dataset directory name>", file=sys.stderr)
        sys.exit(0)

    dataset = DataSet(sys.argv[1])
    go(dataset)

