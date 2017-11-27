import json
from ..entities.pump_control_rule import PumpControlRule

class SensorRepository:

  def find(self, id):
    return PumpControlRule(**json.loads(self.json())[pump_id])

  def json(self):
    return """{ 
                "OG": {
                  "start_temperature": 30, 
                  "nominal_temperature": 45,
                  "time_slots": 4,
                  "time_controls": [{
                    "name": "Night",
                    "check_interval": 2400,
                    "outdoor_max": 15,
                    "start_at": "22:00",
                    "end_at": "03:59"
                  },
                  {
                    "name": "Day",
                    "check_interval": 1000,
                    "outdoor_max": 15,
                    "start_at": "04:00",
                    "end_at": "23:59"
                  }]
                },
                "EG": {
                  "start_temperature": 30,
                  "nominal_temperature": 60
                }
              }"""