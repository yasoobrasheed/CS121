def f(x):
    '''
    Real valued square function  f(x) == x^2
    '''

    return x*x


def integrate(N):
    # Your code here
    # decide on the number of rectangles
    # compute the width of the rectangles
    # use a loop to compute the total area
    # return the value of totalArea
    # remove the next line

    x_dist = 1
    dx = x_dist / N
    totalArea = 0

    for i in range(0, N):
        height = f(i * dx)
        width = dx
        totalArea += (height * width)

    return totalArea

print(integrate(1000))
