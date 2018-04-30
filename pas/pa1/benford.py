# CS121: Benford's Law
#
# Yasoob Rasheed

# Functions for evaluating data using Benford's Law.

import math
import os.path
import pylab as plt
import sys
import util


def extract_amount(currency_symbol, amount_str):
	'''
	Extract currency_symbol from amount_str and return a float value
	extracted: variable that will hold the string value of the float
	return: the extracted variable casted to a float
	'''
	extracted = ""	
	if amount_str.startswith(currency_symbol):
		extracted = amount_str[len(currency_symbol):]
	return float(extracted)


def extract_leading_digits(amount, num_digits):
  	'''
	Use math methods and the formula provided to extract a specific num_digits from the beginning of an amount
	return: The first num_digits of the amount
	'''
    return math.trunc(10 ** (-1 * math.floor(math.log10(amount)) + num_digits - 1) * amount)


def get_leading_digits_range(num_digits):
	'''
	Find the distance between the upper and lower bounds of the range of numbers as a tuple (ex. (1, 10), (10, 100))
	lower_bound: ranges of numbers are powers of 10, so 10^(num_digits - 1)
	upper_bound: same as above, but upper bounds so 10^(num_digits)
	return: tuple with the lower_bound and the upper_bound
	'''	
	lower_bound = 10 ** (num_digits - 1)
	upper_bound = 10 ** num_digits	  
	return (lower_bound, upper_bound)


def compute_expected_benford_dist(num_digits):
	'''
	Create an array of the expected benford distributions between a lower and upper bound
	dist_array: holds the value of the benford formula applied to each "digit" in the range
	dist: benford formula applied to each leading digit
	return: the expected benford distribution
	'''
	dist_array = [] 
	num_range = get_leading_digits_range(num_digits)
	for digit in range(num_range[0], num_range[1]):
		dist = math.log10(1 + 1 / digit)
		dist_array.append(dist)		  
	return dist_array


def compute_benford_dist(currency_symbol, amount_strs, num_digits):
	'''
	Calculates the actual occurences of the leading digits in a given sample range
	num_range: the tuple returned from task 3 (lower_bound, upper_bound)
	benford_array: empty array of size (upper_bound - lower_bound) populated with 0.0 and which will hold the actual distribution
	increment: variable that holds the decimal amount that each occurrence should add to ints respective spot in the benford_array
	numeric_amount: task 1 applied
	trunc_amount: task 2 applied
	return: the benford_area of this sample set
	'''
	num_range = get_leading_digits_range(num_digits)
	benford_array = [0.0] * (num_range[1] - num_range[0])
	increment = 1.0 / len(amount_strs)
	for amount in amount_strs:
		numeric_amount = extract_amount(currency_symbol, amount)
		trunc_amount = extract_leading_digits(numeric_amount, num_digits)
		for benford_digit in range(num_range[0], num_range[1]):
			if trunc_amount == benford_digit:
				benford_array[benford_digit - num_range[0]] += increment
	return benford_array


def compute_benford_MAD(currency_symbol, amount_strs, num_digits):
	'''
	Calculate the mean absolute difference of the expected benford percentages of a given range and the sample benford percentages of the same range
	expected_benford_dist: function made in task 4
	benford_dist: function made in task 5
	sum_of_benfords: holds the summation portion of the MAD formula
	return: mean_abs_diff, which is the sum_of benfords divided by the amount of elements in both sets
	'''
	expected_benford_dist = compute_expected_benford_dist(num_digits)
	benford_dist = compute_benford_dist(currency_symbol, amount_strs, num_digits)
	sum_of_benfords = 0
	for i in range(0, len(benford_dist)):
		sum_of_benfords += abs(benford_dist[i] - expected_benford_dist[i])
	mean_abs_diff = sum_of_benfords / len(benford_dist)
	return mean_abs_diff


################ Do not change the code below this line ################

def plot_benford_dist(currency_symbol, amount_strs, num_digits, output_filename):
    '''
    Plot the actual and expected benford distributions

    Inputs:
        currency_symbol: (string) a currency symbol e.g. '$', 'C$', '\u00A3'
        amount_strs: (list of strings) a non-empty list of positive
            amounts as strings
        num_digits: (int) number of leading digits
    '''
    assert num_digits > 0, \
        "num_digits must be greater than zero {:d}".format(num_digits)

    n = len(amount_strs)
    assert n > 0, \
        "amount_strs must be a non-empty list"

    # compute range of leading digits
    (lb, ub) = get_leading_digits_range(num_digits)
    if lb == 0 and ub == 0:
        print("Skipping plot:invalid return value from get_leading_digits_range")
        return
    digits = range(lb,ub)

    # start a new figure
    f = plt.figure()

    # plot expected distribution
    expected = compute_expected_benford_dist(num_digits)
    plt.scatter(digits, expected, color="red", zorder=1)

    # plot actual distribution
    actual = compute_benford_dist(currency_symbol, amount_strs, num_digits)
    plt.bar(digits, actual, align="center", color="blue", zorder=0)

    # set hash marks for x axis.
    plt.xticks(range(lb, ub, lb))

    # compute limits for the y axis
    max_val = max(max(expected), max(actual))
    y_ub = max_val * 1.1
    plt.ylim(0,y_ub)

    # add labels
    plt.title("Actual (blue) and expected (red) Benford distributions")
    if num_digits ==1: 
        plt.xlabel("Leading digit")
    else:
        plt.xlabel("Leading digits")
    plt.ylabel("Proportion")

    if output_filename:
        # save the plot
        plt.savefig(output_filename)
    else:
        # show the plot
        plt.show()


def go():
    '''
    Process the arguments and do the work.
    '''
    usage = ("usage: python benford.py <input filename> <column number>"
             "<currency symbol> <num digits>")

    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print(usage)
        return

    input_filename = sys.argv[1]
    if not os.path.isfile(input_filename):
        print(usage)
        print("error: file not found: {}".format(input_filename))
        return

    # convert column number argument to an integer
    try:
        col_num = int(sys.argv[2])
    except ValueError:
        s = "error: column number must be an integer: {}"
        print(usage)
        print(s.format(sys.argv[2]))
        return

    data = util.read_column_from_csv(input_filename, col_num, True)
    currency_symbol = sys.argv[3]

    # convert number of digits argument to an integer
    try:
        num_digits = int(sys.argv[4])
    except ValueError:
        s = "error: number of digits must be an integer: {}".format(sys.argv[4])
        print(usage)
        print(s.format(sys.argv[4]))
        return

    # grab the name for the PNG file, if exists.
    if len(sys.argv) == 5:
        output_filename = None
    else:
        output_filename = sys.argv[5]

    plot_benford_dist(currency_symbol, data, num_digits, output_filename)

    # print only four digits after the decimal point
    print("MAD: {:.4}".format(compute_benford_MAD(currency_symbol, data, num_digits)))

if __name__=="__main__":
    go()

