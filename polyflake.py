#!/usr/bin/env python


import turtle
import math
from color_wheel import ColorWheel


class RecursivePolySegment(object):
    def __init__(self, turtle, side_count, limit_count, rainbow=0):
        if side_count < 3:
            raise ValueError('Side count less than 3 is nonsensical')

        self.turtle = turtle
        exterior_angle = 360.0 / side_count
        interior_angle = 180 - exterior_angle

        self.turns = (0, -interior_angle) \
            + (side_count - 2) * (exterior_angle,) \
            + (-interior_angle,)

        self.limit_count = limit_count
        self.side_count = side_count
        self.segment_count = 0
        self.rainbow = rainbow

        if self.rainbow > 0:
            self.color_wheel = ColorWheel(
                self.get_predicted_segment_count() / self.rainbow)

    @staticmethod
    def get_smallest_segment(initial_segment_length, limit_count):
        return initial_segment_length / (3.0 ** limit_count)

    @staticmethod
    def get_pixel_based_limit_count(initial_segment_length):
        # smallest_segment = initial_segment_length / (3.0 ** limit_count)
        # smallest_segment * (3.0 ** limit_count) = initial_segment_length
        # 3.0 ** limit_count = initial_segment_length / smallest_segment
        # limit_count = math.log(initial_segment_length / smallest_segment, 3)
        # smallest segment desired is 1.0
        return math.log(initial_segment_length, 3)

    def __call__(self, direction, segment_length, count):
        if count < self.limit_count:
            for degrees in self.turns:
                direction += degrees
                self(direction, segment_length / 3.0, count + 1)
        else:
            self.turtle.setheading(direction)

            if self.rainbow:
                self.turtle.color(self.color_wheel.get_next_color())

            self.turtle.forward(segment_length)
            self.segment_count += 1

    def get_predicted_segment_count(self):
        return self.side_count * (self.side_count + 1) ** (self.limit_count)


def draw_poly_flake(
        instance,
        direction,
        length,
        side_count,
        iterations=None,
        rainbow=0):

    if iterations is None:
        # calculate the max visible for size length
        iterations = RecursivePolySegment.get_pixel_based_limit_count(length)

    instance.getscreen().tracer(0)
    recursive = RecursivePolySegment(instance, side_count, iterations, rainbow)

    for i in range(side_count):
        direction += (360.0 / side_count)
        recursive(direction, length, 0)

    instance.getscreen().update()


def draw_koch_snowflake():
    draw_poly_flake(0, 500, 3)


def erase(instance):
    instance.reset()
    instance.getscreen().bgcolor('black')
    instance.shape('turtle')
    instance.color('blue')
    instance.hideturtle()
    instance.penup()
    instance.setposition(200, -200)
    instance.pendown()


def simple_draw_flake(side_count, limit, rainbow=0):
    length = 1500.0 / side_count
    draw_poly_flake(0, length, side_count, limit, rainbow)


def demo(rainbow=0):
    instance = turtle.Turtle()

    for n in range(3, 5):
        length = 1500.0 / n

        maximum_iterations = \
            RecursivePolySegment.get_pixel_based_limit_count(length)

        for j in range(int(math.ceil(maximum_iterations))):
            erase(instance)
            draw_poly_flake(instance, 0, length, n, j, rainbow=rainbow)
            yield (n, j)


if __name__ == '__main__':
    for p in demo(1):
        input("Press enter to continue")
