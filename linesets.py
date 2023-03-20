#!/usr/bin/env python


import turtle
import colorsys
import math


class LineTurtle(turtle.Turtle):
    def __init__(self, *args, **kwargs):
        super(LineTurtle, self).__init__(*args, **kwargs)

        self._center = (0, 0)
        self._radius = 200
        self._point_count = 180
        self.set_point_count(self._point_count)

        self.speed(10)

    def _create_points(self):
        angle_delta = 2 * math.pi / self._point_count
        sub_angles = [0.0] * self._point_count
        for i in range(self._point_count):
            sub_angles[i] = angle_delta * i
        self._points = [(
            self._center[0] + self._radius * math.cos(q * angle_delta),
            self._center[1] + self._radius * math.sin(q * angle_delta))
            for q in range(self._point_count)]

    def set_center(self, x, y):
        self._center = (x, y)
        self._create_points()

    def set_point_count(self, point_count):
        self._point_count = point_count
        self._create_points()

    def set_radius(self, radius):
        self._radius = radius
        self._create_points()

    def _set_heading(self, start, end):
        # Point the turtle in the right direction
        opposite = end[1] - start[1]
        adjacent = end[0] - start[0]

        try:
            heading_radians = math.atan(opposite / adjacent)
        except ZeroDivisionError:
            return

        heading_degrees = 180 * heading_radians / math.pi
        self.setheading(heading_degrees)

    def draw_circle(self, skip=10):
        for index, point in enumerate(self._points):
            starting_point = point
            target_point_index = \
                (index + int(self._point_count / 2) + skip + 1)

            # The points are on a circle, so values higher than
            # self._point_count wrap around to the front of the point list
            target_point_index = target_point_index % (self._point_count)
            target_point = self._points[target_point_index]
            self.penup()
            self.setpos(starting_point[0], starting_point[1])
            self.pendown()
            self.setpos(target_point[0], target_point[1])

    def draw_oid(self, skip=2):
        for index, point in enumerate(self._points):
            target_index = (index + 2 + index * skip) % self._point_count
            target = self._points[target_index]
            self.penup()
            self.setpos(point[0], point[1])
            self.pendown()
            self.setpos(target[0], target[1])

    def draw_points(self, point_size=2):
        self.setheading(90)
        save_the_pen_size = self.pensize()
        self.pensize(point_size)
        for point in self._points:
            self.penup()
            self.setpos(point[0], point[1] - point_size / 2)
            self.pendown()
            self.forward(0)

        self.pensize(save_the_pen_size)


if __name__ == '__main__':
    line_turtle = LineTurtle()
    screen = line_turtle.getscreen()
    screen.bgcolor('black')
    screen.tracer(10)
    width = screen.window_width()
    height = screen.window_height()
    line_turtle.set_radius(0.9 * min(width, height) / 4)
    skip = 1

    line_turtle.shape('turtle')

    for i in (1, -1):
        for j in (1, -1):
            line_turtle.color(
                colorsys.hsv_to_rgb(
                    1.0 + (math.atan2(i, j) / (2 * math.pi)) % 1.0,
                    1.0,
                    1.0))

            line_turtle.set_center(j * width / 4., i * height / 4)
            line_turtle.draw_points()
            line_turtle.draw_oid(skip)
            skip += 1

    input("Press enter to quit")
