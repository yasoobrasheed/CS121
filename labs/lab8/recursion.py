from math import sin

def is_power_of_two(n):
    if n == 2:
      return True
    if n % 2 != 0:
      return False
    return is_power_of_two(n / 2)


def fib(n):
    if n == 0:
      return 1
    if n == 1:
      return 1
    return fib(n - 1) + fib(n - 2)


def find_root_sqrt2(epsilon, a, b):
    f_a = (a ** 2) - 2
    f_b = (b ** 2) - 2
    c = (a + b) / 2
    f_c = (c ** 2) - 2
    if abs(f_c) < epsilon:
        return c
    else:
        if f_c < 0:
            return find_root_sqrt2(epsilon, c, b)
        else:
            return find_root_sqrt2(epsilon, a, c)


def find_root(f, epsilon, a, b):
    c = (a + b) / 2
    if abs(f(c)) < epsilon:
        return c
    else:
        if f(c) < 0:
            return find_root(f, epsilon, c, b)
        else:
            return find_root(f, epsilon, a, c)


def root2(x):
    return (x ** 2) - 2


def sinPoint5(x):
    return sin(x) - 0.5


t0 = {"key":"node0",
      "val":27,
      "children":[]}

t1 = {"key":"node0",
      "val":1,
      "children":[{"key":"node0",
                   "val":2,
                   "children":[{"key":"node0",
                                "val":3,
                                "children":[]}]},
                  {"key":"node0",
                   "val":4,
                   "children":[]},
                  {"key":"node0",
                   "val":5,
                   "children":[]}]}


def count_leaves(t):
    '''
    Count the number of leaves in the tree rooted at t
    
    Inputs: (dictionary) a tree
    
    Returns: (integer) number of leaves in t
    '''
    assert t is not None

    if not t["children"]:
        return 1

    num_leaves = 0
    for kid in t["children"]:
        num_leaves += count_leaves(kid)

    return num_leaves


def add_values(t):
    assert t is not None

    values = t['val']

    if not t['children']:
        return values
    
    for child in t['children']:
        values += add_values(child)

    return values