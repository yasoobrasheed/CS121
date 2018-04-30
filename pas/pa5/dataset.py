# CS121 Linear regression
# Data representation.

import csv
import json
import os.path
import numpy as np
import sys

from sklearn.model_selection import train_test_split

def load_json_file(dir_path, filename):
    '''
    Load a JSON file and return its contents.

    Inputs:
        dir_path: (string) path to the directory that contains the
          file
        filename: (string) name of the file

    Returns: depends on the contents of the JSON file.
    '''
    data = None

    try:
        path = os.path.join(dir_path, filename)
        with open(path) as f:
            data = json.load(f)
    except IOError as ioe:                 
        print("Could not open file:", filename, file=sys.stderr)
        sys.exit(0)
    except json.JSONDecodeError as je:
        print("JSON load failed:", filename, file=sys.stderr)
        print(je)
        sys.exit(0)

    return data


def load_numpy_array(dir_path, filename):
    '''
    Load a CSV file into a Numpy array and return it.

    Inputs:
        dir_path: (string) path to the directory that contains the
          file
        filename: (string) name of the file

    Returns: list of strings, 2D Numpy array of floats
    '''
    labels, data = None, None

    try:
        path = os.path.join(dir_path,  filename)
        with open(path) as f:
            # first row must contain the column labels
            labels = f.readline().strip().split(',')
            data = np.loadtxt(f, delimiter=',', dtype=np.float64)
    except IOError as ioe:                 
        print("Could not open file:", filename, file=sys.stderr)
        sys.exit(0)
    except ValueError as ve:
        print("Numpy load failed:", filename, file=sys.stderr)
        print(ve)
        sys.exit(0)

    return labels, data


class DataSet(object):
    '''
    Class for representing a data set.
    '''

    '''
    Constructor

    Inputs: 
        dir_path: (string) path to the directory that contains the
        file
		json: numpy array of the json data
		csv: numpy array of the csv data
		split_numpy: calling train_test_split on csv numpy array
		training_data: numpy array of the first split
		testing_data: numpy array of the next split
    '''
    def __init__(self, dir_path):
        json = load_json_file(dir_path, "parameters.json")
        csv = load_numpy_array(dir_path, "data.csv")

        self.dataset_name = json['name']
        self.pred_vars = json['predictor_vars']
        self.dep_var_index = json['dependent_var']
        self.column_labels = csv[0]

        train_size = json['training_fraction']
        split_numpy = train_test_split(csv[1], train_size=train_size, random_state=json['seed'])
        self.training_data = np.array(split_numpy[0])
        self.testing_data = np.array(split_numpy[1])
