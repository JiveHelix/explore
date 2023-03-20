#!/usr/bin/env python


import turtle_tools as tt
import turtle
import math
from color_wheel import ColorWheel


def get_circle_points(radius, steps=None):
    if steps is None:
        # determine arc that will ensure smooth rendering for any sized circle
        angle_delta = tt.get_smooth_angle_delta(radius)
        steps = int(math.ceil(2 * math.pi / angle_delta))
    else:
        angle_delta = 2 * math.pi / steps

    angles = [i * angle_delta for i in range(steps)]

    points = [
        turtle.Vec2D(radius * math.cos(theta), radius * math.sin(theta))
        for theta in angles]

    return points


class Shapes:
    def __init__(self, center=(0, 0)):
        self.turtle = turtle.Turtle()
        self.screen = self.turtle.getscreen()
        self.color_wheel = ColorWheel(256)
        self.screen.bgcolor('black')
        self.turtle.shape('turtle')
        self.turtle.color('red')
        self.turtle.speed(10)
        self.screen.tracer(50)

    def draw_square(self, size):
        for i in range(4):
            self.turtle.forward(size)
            self.turtle.left(90)

    def draw_partial_square(self, size, segments=(True, True, True, True)):
        for segment in segments:
            if segment:
                self.turtle.pendown()
            else:
                self.turtle.penup()

            self.turtle.forward(size)
            self.turtle.left(90)

        self.turtle.pendown()

    def draw_partial_squares(
            self,
            size,
            count,
            segments=(True, True, True, True)):

        self.color_wheel.set_period(count)
        angle_delta = 360. / count

        for i in range(count):
            self.draw_partial_square(size, segments)
            self.turtle.left(angle_delta)
            self.turtle.color(self.color_wheel.get_next_color())

    def draw_circle(self, radius, center=(0, 0), animate=True):
        center = turtle.Vec2D(*center)
        points = get_circle_points(radius)
        self.turtle.penup()

        try:
            self.turtle.setpos(center + points[0])
        except IndexError:
            breakpoint()

        self.turtle.pendown()

        speed = self.turtle.speed()
        last_p = points[0]
        for idx, p in enumerate(points[1:]):
            self.turtle.setheading(tt.get_heading(p, last_p))
            self.turtle.setpos(p + center)
            last_p = p

    def draw_circles_on_path(
            self,
            path_radius,
            circle_radius,
            steps,
            path_center=(0, 0),
            use_rainbow=False,
            animate=True):

        points = get_circle_points(path_radius, steps)
        center = turtle.Vec2D(*path_center)

        if use_rainbow:
            self.color_wheel.set_period(steps)

            for p in points:
                self.turtle.color(self.color_wheel.get_next_color())
                self.draw_circle(circle_radius, p + center, animate)
        else:
            for p in points:
                self.draw_circle(circle_radius, p + center, animate)


if __name__ == '__main__':
    shapes = Shapes()
    shapes.turtle.pensize(2)
    width = shapes.screen.window_width()
    height = shapes.screen.window_height()

    diameter = min(width, height) * 0.9
    radius = diameter / 2.0
    path_diameter = diameter * 0.8
    path_radius = path_diameter / 2.0
    circles_radius = radius - path_radius

    square_size = math.sqrt(0.5 * ((path_radius - circles_radius) * 0.95) ** 2)
    count = 42

    shapes.draw_partial_squares(square_size, count, (False, True, True, False))

    shapes.draw_circles_on_path(
        path_radius,
        circles_radius,
        count,
        use_rainbow=True)

    # Hide the turtle
    shapes.turtle.hideturtle()
    shapes.screen.update()

    # Save your design
    shapes.screen.getcanvas().postscript(file="shapes.eps")

    input("Press enter to close")
