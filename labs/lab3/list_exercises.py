# CS121 Lab 3: Function

<<<<<<< HEAD
test_list = [True, True, False, True, True]
one = [1, 1, 1, 1]
two = [2, 2, 2, 2]


# Write functions: are_any_true, add_lists, and add_one
def are_any_true(bool_list):
	for i in bool_list:
		if i:
			return True
	return False


def add_lists(list_1, list_2):
	summed_list = []
	for i in range(0, len(list_1)):
		summed_list.append(list_1[i] + list_2[i])
	return summed_list


def add_one(array):
	for i in range(0, len(array)):
		array[i] += 1


def go():
	print(are_any_true(test_list))
	print(add_lists(one, two))
	a = [1, 2, 3, 4, 5]
	add_one(a)
	print(a)


go()
=======

# Write functions: are_any_true, add_lists, and add_one


def go():
    '''
    Write code to verify that your functions work as expected here.
    Try to think of a few good examples to test your work.
    '''

    # replace the pass with test code for your functions
    pass


if __name__ == "__main__":
    go()

>>>>>>> 5948107c6aa4a0fae598e416d34f75c6afb0e3b7
