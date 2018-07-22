from interface import implements

from lib.entities.sensor_interface import SensorInterface


class SinglePinSensor(implements(SensorInterface)):

    def __init__(self, id, pin):
        self.id = id
        self.pin = pin

    def current_temperature(self):
        return 33
