# CS121: Treemaps
# Sample use of ColorKey
#
# This code is not explicitly part of the assignment, but rather a demo to
# provide familiarity with the use of ColorKey

from drawing import ChiCanvas, ColorKey


def go():
    # create a canvas
    c = ChiCanvas(10, 10)

    # create a color key
    ck = ColorKey(set(["SR", "W", "A"]))

    # draw the color key
    ck.draw_color_key(c, .8, 0, 1.0, .30,
                      code_to_label={"SR": "Streets/Roads", "W": "Water",
                                     "A": "Airports"})

    # show it
    c.show()

if __name__ == "__main__":
    go()
