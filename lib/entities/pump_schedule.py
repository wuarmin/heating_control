import datetime

class PumpSchedule(object):

  def __init__(self, pump_id, next_start, next_stop):
    self.pump_id    = pump_id
    self.next_start = next_start
    self.next_stop = next_stop

  def __str__(self):
    return str(self.__dict__)