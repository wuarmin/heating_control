from interface import implements

from lib.entities.sensor_interface import SensorInterface


class DualPinSensor(implements(SensorInterface)):

    def __init__(self, id, pin_one, pin_two):
        self.id = id
        self.pin_one = pin_one
        self.pin_two = pin_two

    def current_temperature(self):
        return ((self._temperature_one()+self._temperature_two())/2)+self._temperature_two()

    def _temperature_one(self):
        return 30

    def _temperature_two(self):
        return 12
