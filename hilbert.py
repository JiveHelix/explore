#!/usr/bin/env python


import turtle
from color_wheel import ColorWheel


class HilbertCurve(object):
    def __init__(self, turtle, edge_length, depth):
        self.turtle = turtle
        self.edge_length = edge_length
        self.segment_length = edge_length / (2 ** (depth + 1) - 1)
        self.depth = depth
        self.segmentCount = 2 ** ((depth + 1) * 2) - 1
        self.colorWheel = ColorWheel(self.segmentCount)

    def draw_segment(self):
        self.turtle.color(self.colorWheel.get_next_color())
        self.turtle.forward(self.segment_length)

    def __call__(self, direction, depth=None):
        if depth is None:
            depth = self.depth

        if depth < 0:
            return

        self.turtle.left(direction)

        self(-direction, depth - 1)

        self.draw_segment()
        self.turtle.right(direction)

        self(direction, depth - 1)

        self.draw_segment()

        self(direction, depth - 1)

        self.turtle.right(direction)
        self.draw_segment()

        self(-direction, depth - 1)

        self.turtle.right(-direction)


def get_new_turtle(initial_position=(0, 0)):
    turtle.clearscreen()
    t = turtle.Turtle()
    t.shape("turtle")
    t.penup()
    t.setposition(*initial_position)
    t.pendown()
    return t


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        depth = int(sys.argv[1])
    else:
        depth = 5

    t = get_new_turtle((-400, -400))
    t.speed(10)
    t.getscreen().bgcolor('black')

    t.getscreen().tracer(50)

    hilbert = HilbertCurve(t, 800, depth)
    hilbert(90)

    t.getscreen().update()

    # Save your design
    t.screen.getcanvas().postscript(file="hilbert.eps")

    input("Press enter to close")
