# Examples for lists and loops lab

l0 = []
l1 = [1, "abc", 5.7, [1, 3, 5]]
l2 = [10, 11, 12, 13, 14, 15, 16]
l3 = [7, -5, 6, 27, -3, 0, 14]
l4 = [0, 1, 1, 3, 2, 4, 6, 1, 7, 8]


new_list = [0] * (max(l4) + 1)

for element in l4:
	new_list[element] += 1

print(new_list)


