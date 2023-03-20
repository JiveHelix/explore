import colorsys


class ColorWheel(object):
    def __init__(self, period=360):
        self._set_period(period)
        self._set_saturation(1.0)
        self.reset()

    def _set_period(self, period):
        self.period = int(period)
        # self.angle_delta = 2 * math.pi / self.period
        self.angle_delta = 1.0 / self.period

    def set_period(self, period):
        self._set_period(period)
        self.reset()

    def _set_saturation(self, saturation):
        """saturation is a positive float """
        self.saturation = max(saturation, 0.0)
        self.cos_power = 0.0 + saturation

    def set_saturation(self, saturation):
        self._set_saturation(saturation)
        self.reset()

    def reset(self):
        self._color_index = 0

        self.color_values = [
            colorsys.hsv_to_rgb(i * self.angle_delta, 1.0, 1.0)
            for i in range(self.period)]

    def get_next_color(self):
        if self._color_index >= self.period:
            self._color_index = 0
            return self.get_next_color()

        color = self.color_values[self._color_index]
        self._color_index += 1

        return color
