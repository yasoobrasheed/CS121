# CS 121: Drawing TreeMaps
#
# Code for constructing a treemap.
#
# YOUR NAME: Yasoob Rasheed

import sys
import csv
import json

from drawing import ChiCanvas, ColorKey


MIN_RECT_SIDE_FOR_TEXT = 0.03
X_SCALE_FACTOR = 12
Y_SCALE_FACTOR = 10


def compute_internal_counts(t):
    '''
    Assign a count to the interior nodes.  The count of the leaves
    should already be set.  The count of an internal node is the sum
    of the counts of its children.

    Inputs:
        t: a tree

    Variables:
        value: holds the count of the children of each node

    Returns:
        The count at that node. This is count for leaf nodes, and the sum of
            the counts of the children of internal nodes. The input tree t
            should be modified so that every internal node's count is set
            to be the sum of the counts of its children.
    '''
    if t.num_children() == 0:
        return t.count

    value = 0
    for child in t.children:
        value += compute_internal_counts(child)
    t.count = value

    return value


def compute_verbose_labels(t, prefix=None):
    '''
    Assign a verbose label to non-root nodes. Verbose labels contain the
    full path to that node through the tree. For example, following the
    path "Google" --> "female" --> "white" should create the verbose label
    "Google: female: white"

    Inputs:
        t: a tree

    Variables:
        pref: holds the verbose label of the node

    Outputs:
        No explicit output. The input tree t should be modified to contain
            verbose labels for all non-root nodes
    '''
    if t.num_children() == 0:
        t.verbose_label = prefix + t.label
        return t.label

    pref = ""
    if prefix != None:
        pref = prefix + t.label + ": "
    else:
        pref = t.label

    # Remove the colon from the end of the verbose label
    t.verbose_label = pref[:-2]

    for child in t.children:
        compute_verbose_labels(child, pref)


def draw_treemap(t,
                 bounding_rec_height=1.0,
                 bounding_rec_width=1.0,
                 output_filename=None):

    '''
    Draw a treemap and the associated color key

    Inputs:
        t: a tree
        bounding_rec_height: the height of the bounding rectangle.
        bounding_rec_width: the width of the bounding rectangle.
        output_filename: (string or None) the name of a file for
        storing the image or None, if the image should be shown.

    Variables:
        c: ChiCanvas object with given x and y scale factors
        ck: ColorKey object given the tree and the ChiCanvas

    Returns:
        No specific return, draws the tree
    '''
    c = ChiCanvas(X_SCALE_FACTOR, Y_SCALE_FACTOR)
    ck = assign_color(t, c)
    x0 = 0.0
    y0 = 0.0
    weight(c, ck, t, x0, y0, bounding_rec_width, bounding_rec_height)
    if output_filename == None:
        c.show()
    else:
        c.savefig(output_filename)


def weight(c, ck, t, x0, y0, w, h, flag=True):
    '''
    Draw the treemap (All the rectangles and labels)

    Inputs:
        c: ChiCanvas object
        ck: ColorKey object with colors already assigned
        t: a tree
        x0: hardcoded 0.0, the top left of the screen
        y0: hardcoded 0.0, the top left of the screen
        w: width of the bounding rectangle
        h: height of the bounding rectangle
        flag: set to True, changes based on the depth of the tree

    Variables:
        color: holds the color of that label in the color key
        percentage: holds the weight of a given rectangle in
                    comparison with the previous node
        width: modified w based on the value of flag
        height: modified h based on the value of flag

    Return:
        No explicit return, meant to draw the rectangles and text
    '''
    if t.num_children() == 0:
        color = ck.get_color(t.label)
        c.draw_rectangle(x0, y0, 1.0, 1.0, fill=color)
        l = t.verbose_label
        if w >= MIN_RECT_SIDE_FOR_TEXT and h >= MIN_RECT_SIDE_FOR_TEXT:
            if h > w:
                c.draw_text_vertical(x0 + w / 2, y0 + h / 2, h, l)
            else:
                c.draw_text(x0 + w / 2, y0 + h / 2, w, l)
        return

    for child in t.children:
        percentage = child.count
        if t.count != 0:
            percentage = child.count / t.count
        width = w
        height = h
        if flag:
            width = percentage * w
        else:
            height = percentage * h
        weight(c, ck, child, x0, y0, width, height, not flag)
        if flag:
            x0 += width
        else:
            y0 += height 


def assign_color(t, c):
    '''
    Creates the color key

    Inputs:
        t: a tree
        c: ChiCanvas object

    Variables:
        color_list: holds the verbose_labels of the leaves of the tree
        color_set: a set of lists for the Color key

    Returns:
        ck: a color key given a mapping of unique verbose_labels
    '''
    color_list = []
    color_list = make_color_list(t, color_list)
    color_set = set(color_list)
    ck = ColorKey(color_set)
    return ck


def make_color_list(t, color_list):
    '''
    Creates a list of colors from the verbose_labels of the leaves of t

    Inputs:
        t: a tree
        color_list: an empty list

    Returns:
        color_list: the inputted empty list, populated with unique 
                    verbose_labels
    '''
    if t.num_children() == 0:
        color_list.append(t.label)
        return

    for child in t.children:
        make_color_list(child, color_list)

    return color_list