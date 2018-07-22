import json
from simple_settings import settings

from lib.entities.single_pin_sensor import SinglePinSensor
from lib.entities.dual_pin_sensor import DualPinSensor

class SensorRepository(object):

    def find(self, id):
        sensor_json = self._json().get(id, None)
        if sensor_json is None:
            return None
        return self._deserialize_sensor(id, sensor_json)

    def _json(self):
        return json.load(open(settings.HEATING_CONTROL_CONFIG)).get('sensors', {})

    def _deserialize_sensor(self, id, json_dict):
        if('pin_two' in json_dict):
            dual_pin_sensor_dict = {
                'id': id,
                'pin_one': json_dict.get('pin_one'),
                'pin_two': json_dict.get('pin_two')
            }
            return DualPinSensor(**dual_pin_sensor_dict)
        else:
            single_pin_sensor_dict = {
                'id': id,
                'pin': json_dict.get('pin_one'),
            }
            return SinglePinSensor(**single_pin_sensor_dict)
