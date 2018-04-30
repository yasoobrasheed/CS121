# CS121: Analyzing Election Tweets
# Part 1: Task 0
# By: Yasoob Rasheed

from util import sort_count_pairs


def find_top_k(items, k):
    '''
    Find the K most frequently occuring items

    Inputs:
        items: a list of items
        k: integer 

	Variables:
		item_dict: a dictionary with the number of occurrence 
		of each unique value

    Returns: sorted list of K tuples
    '''

    # Use a dictionary to count the number of times each unique 
	# value occurs
	# Extract list of (key, count) pairs from the dictionary
	# Sort the pairs using the supplied function
	# Pick off the first K pairs
	
    item_dict = {}

    for item in items:
	    if item in item_dict:
    		item_dict[item] += 1
	    else:
		    item_dict[item] = 1

    return sort_count_pairs(item_dict.items())[:k]


def find_min_count(items, min_count):
    '''
    Find the items that occur at least min_count times
	
    Inputs:
        items: a list of items    
        min_count: integer

	Variables:
		item_dict: a dictionary with the number of occurrence 
		of each unique value
		min_count_array: an array with each tuple containing 
		an item and its occurrences
        
    Returns: sorted list of tuples
    '''

    # Compute the counts
    # Build a list of the items and associated counts that meet 
	# the threshold
    # Sort it using the supplied function

    item_dict = {}

    for item in items:
        if item in item_dict:
            item_dict[item] += 1
        else:
            item_dict[item] = 1
  
    min_count_array = []

    for key, value in item_dict.items():
        if value >= min_count:
            min_count_array.append((key, value))
        
    return sort_count_pairs(min_count_array)


def find_frequent(items, k):
    '''
    Find items where the number of times the item occurs is at least
    1/k * len(items).

    Input: 
        items: list of items
        k: integer

	Variables:
		item_dict: a dictionary with the number of occurrence 
		of each unique value

    Returns: sorted list of tuples
    '''

    # N = Total number of items
    # D = Data structure with K - 1 counters
    # I = Given list item

    # If I occurs in D, increment I counter by one
    # If I doesn't occur in D, and there are fewer than K - 1 items in D,
	# add I with a value of one to D
    # If I does not occur in D and there are K - 1 items in D, decrement all 
	# the counters by one and remove any with a count of 0 from D
 
    item_dict = {}

    for item in items:
        if item not in item_dict and len(item_dict) < k - 1:
            item_dict[item] = 1
        elif item not in item_dict and len(item_dict) == k - 1:
            item_dict_subtracted = {}
            for key in item_dict:
                value = item_dict[key] - 1
                if value > 0:
                    item_dict_subtracted[key] = value
            item_dict = item_dict_subtracted
        elif item in item_dict:
            item_dict[item] += 1     
     
    return sort_count_pairs(item_dict.items())
