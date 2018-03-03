import json
from lib.entities.pump_control_rule import PumpControlRule
from datetime import datetime
from simple_settings import settings

from lib.entities.time_control import TimeControl

class PumpControlRuleRepository(object):

  def find_for_pump_id(self, pump_id):
    return self.__deserialize_pump_control_rule(self.json()[pump_id])

  def json(self):
    return json.load(open(settings.HEATING_CONTROL_CONFIG))["pump_control_rules"]

  # private
  def __deserialize_pump_control_rule(self, json_dict):
    pump_control_rule_dict = {
      'start_temperature':   json_dict.get('start_temperature'),
      'nominal_temperature': json_dict.get('nominal_temperature'),
      'time_slots':          json_dict.get('time_slots'),
      'time_controls':       list(map(self.__deserialize_time_control, json_dict['time_controls']))
    }
    return PumpControlRule(**pump_control_rule_dict)

  def __deserialize_time_control(self, json_dict):
    time_control_dict = {
      'name':           json_dict.get('name'),
      'check_interval': json_dict.get('check_interval'),
      'outdoor_max':    json_dict.get('outdoor_max'),
      'start_at':       datetime.strptime(json_dict['start_at'], '%H:%M').time(),
      'end_at':         datetime.strptime(json_dict['end_at'], '%H:%M').time()
    }
    return TimeControl(**time_control_dict)
