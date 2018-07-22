import json
from datetime import datetime
from simple_settings import settings

from lib.entities.pump_control_rule import PumpControlRule
from lib.entities.time_control import TimeControl


class PumpControlRuleRepository(object):

    def find_for_pump_id(self, pump_id):
        pump_control_rule_json = self._json().get(pump_id, None)
        if pump_control_rule_json is None:
            return None
        return self._deserialize_pump_control_rule(pump_control_rule_json)

    def _json(self):
        return json.load(open(settings.HEATING_CONTROL_CONFIG)).get("pump_control_rules", {})

    # private
    def _deserialize_pump_control_rule(self, json_dict):
        pump_control_rule_dict = {
            'start_temperature': json_dict.get('start_temperature'),
            'nominal_temperature': json_dict.get('nominal_temperature'),
            'temperature_sensor_id': json_dict.get('temperature_sensor_id'),
            'time_slots': json_dict.get('time_slots'),
            'time_controls': list(map(self._deserialize_time_control, json_dict['time_controls']))
        }
        return PumpControlRule(**pump_control_rule_dict)

    def _deserialize_time_control(self, json_dict):
        time_control_dict = {
            'name': json_dict.get('name'),
            'check_interval': json_dict.get('check_interval'),
            'outdoor_max': json_dict.get('outdoor_max'),
            'start_at': datetime.strptime(json_dict['start_at'], '%H:%M').time(),
            'end_at': datetime.strptime(json_dict['end_at'], '%H:%M').time()
        }
        return TimeControl(**time_control_dict)
