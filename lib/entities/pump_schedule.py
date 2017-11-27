import datetime

class PumpSchedule(object):

  def __init__(self, pump_id, next_start, next_stop):
    self.pump_id    = pump_id
    if(isinstance(next_start, datetime.datetime)):
      self.next_start = next_start
    else:
      self.next_start = datetime.datetime.strptime(next_start, '%Y-%m-%dT%H:%M:%S.%f')
    if(isinstance(next_stop, datetime.datetime)):
      self.next_stop = next_stop
    else:
      self.next_stop = datetime.datetime.strptime(next_stop, '%Y-%m-%dT%H:%M:%S.%f')

  def __str__(self):
    return str(self.__dict__)