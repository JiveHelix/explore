#!/usr/bin/env python

import turtle
import numpy as np
from color_wheel import ColorWheel


class ComplexTurtle(turtle.Turtle):
    def __init__(self, pixels_per_unit):
        super(ComplexTurtle, self).__init__()
        self._pixels_per_unit = pixels_per_unit
        self._value = complex(0, 0)
        self.getscreen().bgcolor('black')
        self.shape('turtle')
        self.color('red')
        self.speed(0)
        self.getscreen().tracer(100)

    def update_position(self):
        self.set_position_complex(self._value * self._pixels_per_unit)

    def assign(self, value):
        is_down = self.isdown()
        self.penup()
        self._value = value
        self.update_position()

        if is_down:
            self.pendown()

    def set_position_complex(self, z):
        self.setpos(np.real(z), np.imag(z))

    def get_position_complex(self):
        position = self.pos()
        return complex(position[0], position[1])

    def set_heading_complex(self, z):
        self.setheading(np.angle(z, True))

    def __imul__(self, other):
        self._value *= other

        delta = \
            self._value * self._pixels_per_unit - self.get_position_complex()

        mag = np.absolute(delta)
        if (mag > 0.5):
            # change is large enough to be visible
            self.set_heading_complex(delta)
            self.forward(mag)

        return self

    def __idiv__(self, other):
        starting_value = self._value
        self._value = starting_value / other

        delta = \
            self._value * self._pixels_per_unit - self.get_position_complex()

        mag = np.absolute(delta)

        if (mag > 0.5):
            # change is large enough to be visible
            self.set_heading_complex(delta)
            self.forward(mag)

        return self

    def apply_rotation(self, divisions, count):
        self.assign(complex(1, 0))
        speed = self.speed()
        step = complex(1, np.pi / divisions)

        if speed:
            # This is a value between 1 and 10.
            for i in range(count):
                self *= step
                if i % (speed * 10) == 0:
                    self.getscreen().update()
        else:
            for i in range(count):
                self *= step

        self.getscreen().update()

    def draw_circle(self, divisions):
        self.apply_rotation(divisions, 2 * divisions)


if __name__ == '__main__':
    complex_turtle = ComplexTurtle(100)
    colors = ColorWheel(10)

    for i in range(10):
        complex_turtle.color(colors.get_next_color())
        complex_turtle.draw_circle(2 ** (i + 2))

    complex_turtle.getscreen().getcanvas().postscript(file="exp.eps")
    input("Press enter to close")
