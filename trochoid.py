#!/usr/bin/env python

import turtle_tools as tt
import turtle
import math
from color_wheel import ColorWheel


class Trochoid:
    def __init__(self, center=(0, 0)):
        self.turtle = turtle.Turtle()
        self.screen = self.turtle.getscreen()
        self.center = turtle.Vec2D(center[0], center[1])

        self._steps_per_turn = 720
        self._pen_sign = -1
        self._turns = 1
        self._steps = 360
        self.set_radii(200, 70)
        self._color_wheel = ColorWheel(self._steps)

        self.screen.bgcolor('black')
        self.turtle.shape('turtle')
        self.turtle.color('red')
        self.turtle.speed(0)
        self.screen.tracer(5)

    @property
    def is_epitrochoid(self) -> bool:
        return self._pen_sign == 1

    @is_epitrochoid.setter
    def is_epitrochoid(self, value: bool) -> None:
        if value:
            self._pen_sign = 1
        else:
            self._pen_sign = -1

        self.set_radii(self._arm_radius, self.pen_radius)

    @property
    def is_hypotrochoid(self) -> bool:
        return self._pen_sign == -1

    @is_hypotrochoid.setter
    def is_hypotrochoid(self, value: bool) -> None:
        if value:
            self._pen_sign = -1
        else:
            self._pen_sign = 1

        self.set_radii(self._arm_radius, self.pen_radius)

    @property
    def arm_radius(self):
        return self._arm_radius

    @arm_radius.setter
    def arm_radius(self, value):
        self.set_radii(value, self._pen_radius)

    @property
    def pen_radius(self):
        return self._pen_radius

    @pen_radius.setter
    def pen_radius(self, value):
        self.set_radii(self._arm_radius, value)

    def set_pen_radius(self, pen_radius) -> None:
        self.set_radii(self._arm_radius, pen_radius)

    def set_radii(self, arm_radius, pen_radius, minimum_arc=2.0):
        self._rolling_radius = arm_radius + self._pen_sign * pen_radius
        self._pen_radius = pen_radius
        self._arm_radius = arm_radius

        self._arm_rate = 1.0
        self._pen_rate = \
            self._pen_sign * self._arm_rate * arm_radius / self._pen_radius

        # Calculate number of _turns required to complete pattern
        self._turns = self._pen_radius / math.gcd(arm_radius, self._pen_radius)

        # Calculate _steps_per_turn to ensure smoothness
        self._angle_delta = tt.get_smooth_angle_delta(
            self._rolling_radius + self._pen_radius,
            minimum_arc)

        self._steps_per_turn = int(math.ceil(2 * math.pi / self._angle_delta))
        self._steps = int(math.ceil(self._turns * self._steps_per_turn))

    def erase(self):
        bgcolor = self.screen.bgcolor()
        shape = self.turtle.shape()
        color = self.turtle.color()
        speed = self.turtle.speed()
        tracer = self.screen.tracer()
        self.turtle.reset()
        self.screen = self.turtle.getscreen()
        self.screen.bgcolor(bgcolor)
        self.turtle.shape(shape)
        self.turtle.color(*color)
        self.turtle.speed(speed)
        self.screen.tracer(tracer)

    def calculate_orthogonal_position(self, trigfunc, angle):
        arm = self._rolling_radius * trigfunc(self._arm_rate * angle)
        pen = self._pen_radius * trigfunc(self._pen_rate * angle)

        return arm + pen

    def calculate_position(self, angle):
        return turtle.Vec2D(
            self.calculate_orthogonal_position(math.cos, angle),
            self.calculate_orthogonal_position(math.sin, angle))

    def draw(self, rainbow_count=1):
        self._color_wheel.set_period(self._steps / rainbow_count)
        self.turtle.penup()
        last_point = self.center + self.calculate_position(0)
        self.turtle.setpos(last_point)
        self.turtle.pendown()
        speed = self.turtle.speed()

        if speed > 0 and speed < 11:
            # The turtle icon will be animated as it draws.
            # When speed is 0 or greater than 10, the turtle jumps to the next
            # position.
            for i in range(self._steps):
                current_point = self.center \
                    + self.calculate_position(i * self._angle_delta)

                self.turtle.setheading(
                    tt.get_heading(current_point, last_point))

                last_point = current_point
                self.turtle.setpos(current_point)
                self.turtle.color(self._color_wheel.get_next_color())

                if i % (2 * speed) == 0:
                    self.screen.update()
        else:
            for i in range(self._steps):
                current_point = \
                    self.center \
                    + self.calculate_position(i * self._angle_delta)

                self.turtle.setheading(
                    tt.get_heading(current_point, last_point))

                last_point = current_point
                self.turtle.setpos(current_point)
                self.turtle.color(self._color_wheel.get_next_color())


if __name__ == '__main__':
    trochoid = Trochoid()
    trochoid.turtle.speed(10)
    trochoid.screen.tracer(200)

    print(f"{trochoid.is_hypotrochoid=}")
    print(f"{trochoid.is_epitrochoid=}")
    trochoid.draw()

    trochoid.is_epitrochoid = True
    print(f"{trochoid.is_hypotrochoid=}")
    print(f"{trochoid.is_epitrochoid=}")
    trochoid.pen_radius = trochoid.pen_radius - 5
    trochoid.draw()

    # Hide the turtle
    trochoid.turtle.hideturtle()
    trochoid.screen.update()

    # Save your design
    trochoid.screen.getcanvas().postscript(file="trochoid.eps")

    input("Press enter to close")
