# CS121: PA 7 - Diversity Treemap
#
# Code for reading Silicon Valley diversity data, summarizing
# it, and building a tree from it.
#
# YOUR NAME: Yasoob Rasheed

import argparse
import csv
import json
import pandas as pd
import sys

import treenode
import treemap

###############
#             #
#  Your code  #
#             #
###############

def print_data(data, keyword):
    '''
    Helper method for load_diversity_data. Prints the counts of each
    unique value given data

    Inputs:
        data: (pandas dataframe) holds the data in the .csv file given
        keyword: (string) a given column in data

    Variables:
        df: (pandas datafram) turns keyword and count column into a pandas DataFrame
        group: (pandas group object) groups the counts by the keyword

    Returns:
        No return value, just prints the counts
    '''
    print("#####################")
    print(keyword)
    print("#####################")

    df = data[[keyword, "count"]]
    group = df.groupby(df[keyword]).sum()

    for i in range(0, len(group)):
        print(group.index.values[i] + " : " + str(group['count'][i]))
    print("\n")


def load_diversity_data(filename):
    '''
    Load Silicon Valley diversity data and print summary

    Inputs:
        filename: (string) the name pf the file with the data

    Variables:
        data: (pandas dataframe) holds the data in the .csv file given
        comps: (int) the number of unique companies in the data

    Returns: a pandas dataframe
    '''
    data = pd.read_csv(filename)

    comps = str(len(data.drop_duplicates('company')))
    print("Diversity data comes from the following " + comps + " companies:")
    
    companies_text = ""
    for c in data.drop_duplicates('company').company:
        companies_text += c + ", "
    print(companies_text)

    print("\nThis data includes " + str(data['count'].sum()) + " employees\n")

    print_data(data, 'gender')
    print_data(data, 'race')
    print_data(data, 'job_category')
    
    return data


def prune_tree(original_sub_tree, values_to_discard):
    '''
    Returns a tree with any node whose label is in the list values_to_discard
    (and thus all of its children) pruned. This function should return a copy
    of the original tree and should not destructively modify the original tree.
    The pruning step must be recursive.

    Inputs:
        original_sub_tree: (TreeNode) a tree of type TreeNode whose internal
                  counts have been computed. That is, compute_internal_counts()
                  must have been run on this tree.
        values_to_discard: (list of strings) A list of strings specifying the
                  labels of nodes to discard

    Variables:
        t: (TreeNode) variable representation of original_sub_tree
        child_array: (list of TreeNodes) holds the list of children for a given
                  node of the tree 

    Returns: a new TreeNode representing the pruned tree
    '''
    t = original_sub_tree
    if t.num_children() == 0:
        return treenode.TreeNode(t.label, count=t.count)
    child_array = []
    for child in t.children:
        if child.label not in values_to_discard:
            child_array.append(prune_tree(child, values_to_discard))
    return treenode.TreeNode(t.label, t.count, child_array)


#############################
#                           #
#  Our code: DO NOT MODIFY  #
#                           #
#############################

def data_to_tree(data, hierarchy):
    '''
    Converts a pandas DataFrame to a tree (using TreeNode) following a
    specified hierarchy

    Inputs:
        data: (pandas.DataFrame) the data to be represented as a tree
        hierarchy: (list of strings) a list of column names to be used as
                   the levels of the tree in the order given. Note that all
                   strings in the hierarchy must correspond to column names
                   in data

    Returns: a tree (using the TreeNode class) representation of data
    '''
    if hierarchy is None or len(hierarchy) == 0:
        raise ValueError("Hierarchy must be a non-empty list of column names")
    # create dictionary of possible values for each level of the hierarchy
    hierarchy_labels = {}
    for level in hierarchy:
        if level not in data.columns:
            raise ValueError("Column " + str(level) + " included in the \
                  hierarchy, but does not exist in data", data.columns)
        else:
            hierarchy_labels[level] = data[level].unique()
    return create_st(data, hierarchy, hierarchy_labels, "")


def create_st(relevant_rows, hierarchy, hierarchy_labels, level_label):
    '''
    Recursively creates subtrees

    '''
    if len(hierarchy) == 0:
        # Return leaf node with count of relevant rows
        return treenode.TreeNode(level_label,
                                 count=relevant_rows["count"].sum())
    else:
        curr_children = []
        curr_level = hierarchy[0]
        hierarchy = list(hierarchy[1:])
        for level_value in hierarchy_labels[curr_level]:
            curr_rows = relevant_rows[relevant_rows[curr_level] == level_value]
            curr_children.append(create_st(curr_rows, hierarchy,
                                 hierarchy_labels, level_value))
        return treenode.TreeNode(level_label, children=curr_children)


def parse_args(args):
    parser = argparse.ArgumentParser(description='Drawing treemaps.')
    parser.add_argument('-i', '--input_filename', nargs=1,
                        help="input filename", type=str,
                        default=["data/Reveal_EEO1_for_2016.csv"])
    parser.add_argument('-o', '--output_filename', nargs=1,
                        help="output filename", type=str, default=[None])
    parser.add_argument('-w', '--width', nargs=1,
                        help="initial bounding rectangle width", type=float,
                        default=[1.0])

    try:
        return parser.parse_args(args[1:])
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = parse_args(sys.argv)

        data = load_diversity_data(args.input_filename[0])

        # Subdivide by job category and then gender
        example_tree = data_to_tree(data, ["job_category", "gender"])
        treemap.compute_internal_counts(example_tree)
        treemap.compute_verbose_labels(example_tree)
        treemap.draw_treemap(example_tree,
                             bounding_rec_height=1.0,
                             bounding_rec_width=args.width[0],
                             output_filename=args.output_filename[0])

        # Subdivide by job category, gender, and race
        example_tree = data_to_tree(data, ["job_category", "gender", "race"])
        treemap.compute_internal_counts(example_tree)
        treemap.compute_verbose_labels(example_tree)
        treemap.draw_treemap(example_tree,
                             bounding_rec_height=1.0,
                             bounding_rec_width=args.width[0],
                             output_filename=args.output_filename[0])

        # Subdivide by company, gender, and race
        example_tree = data_to_tree(data, ["company", "gender", "race"])
        treemap.compute_internal_counts(example_tree)
        treemap.compute_verbose_labels(example_tree)
        treemap.draw_treemap(example_tree,
                             bounding_rec_height=1.0,
                             bounding_rec_width=args.width[0],
                             output_filename=args.output_filename[0])

        # Show gender and race filtering for only small companies
        original_tree = data_to_tree(data, ["company", "gender", "race"])
        treemap.compute_internal_counts(original_tree)
        example_tree = prune_tree(original_tree,
                                  ["Adobe", "Airbnb", "Apple", "Cisco", "eBay",
                                   "Facebook", "Google", "HP Inc.", "HPE",
                                   "Intel", "Intuit", "LinkedIn", "Lyft",
                                   "Nvidia", "Salesforce", "Square", "Twitter",
                                   "Uber"])
        treemap.compute_internal_counts(example_tree)
        treemap.compute_verbose_labels(example_tree)
        treemap.draw_treemap(example_tree,
                             bounding_rec_height=1.0,
                             bounding_rec_width=args.width[0],
                             output_filename=args.output_filename[0])

        # Show non-white and non-asian Silicon Valley workforce
        original_tree = data_to_tree(data, ["company", "race", "gender"])
        treemap.compute_internal_counts(original_tree)
        example_tree = prune_tree(original_tree, ["Asian", "White"])
        treemap.compute_internal_counts(example_tree)
        treemap.compute_verbose_labels(example_tree)
        treemap.draw_treemap(example_tree,
                             bounding_rec_height=1.0,
                             bounding_rec_width=args.width[0],
                             output_filename=args.output_filename[0])

    else:
        print("doing nothing besides loading the code...")