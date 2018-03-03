from datetime import datetime
from tinydb import TinyDB, Query, where
from lib.entities.pump_schedule import PumpSchedule

class PumpScheduleRepository:

  def __init__(self):
    self.db = TinyDB('heating_control_db.json')
    self.table = self.db.table('pump_schedules')

  def find_by_pump_id(self, pump_id):
    result = self.table.search(Query().pump_id == pump_id)
    return self.__deserialize_pump_schedule(result[0]) if len(result) > 0 else None

  def create(self, pump_schedule):
    self.table.insert(self.__serialize_pump_schedule(pump_schedule))

  def delete(self, pump_schedule):
    self.table.remove(where('pump_id') == pump_schedule.pump_id)

  def clear(self):
    self.table.purge()

  # private
  def __deserialize_pump_schedule(self, tdb_dict):
    pump_schedule_dict = {
      'pump_id':    tdb_dict.get('pump_id'),
      'next_start': datetime.strptime(tdb_dict.get('next_start'), '%Y-%m-%dT%H:%M:%S.%f'),
      'next_stop':  datetime.strptime(tdb_dict.get('next_stop'), '%Y-%m-%dT%H:%M:%S.%f'),
    }
    return PumpSchedule(**pump_schedule_dict)

  # private
  def __serialize_pump_schedule(self, pump_schedule):
    return {
      'pump_id':    pump_schedule.pump_id, 
      'next_start': pump_schedule.next_start.strftime('%Y-%m-%dT%H:%M:%S.%f'),
      'next_stop':  pump_schedule.next_stop.strftime('%Y-%m-%dT%H:%M:%S.%f')
    }
