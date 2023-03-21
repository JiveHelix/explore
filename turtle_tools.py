
import turtle
import math
from contextlib import contextmanager


def get_heading(first: turtle.Vec2D, second: turtle.Vec2D) -> float:
    x, y = first - second
    return math.degrees(math.atan2(y, x))


def get_smooth_angle_delta(radius, minimum_arc_pixels: float = 2.0) -> float:
    return abs(math.atan(minimum_arc_pixels / radius))
