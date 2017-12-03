from ..repositories.pump_schedule_repository import PumpScheduleRepository

class ControlPump(object):

  def __init__(self):
    self.pump_schedule_repo = PumpScheduleRepository()

  def __call__(self, pump, current_time):
    self.pump = pump
    self.current_time = current_time
    next_schedule = self.next_schedule()

    print("here next_schedule", next_schedule);

    # next_schedule = rule.next_schedule(pump, current_time)
    # print("next_schedule", next_schedule.next_start)

    # get the current temperature
    # what's the current time slice
    # when is next start and next stop

  def next_schedule(self):
    next_schedule = self.pump_schedule_repo.find_by_pump_id(self.pump.id)
    if(next_schedule is None):
      rule = self.pump.rule
      next_schedule = rule.next_schedule(self.pump, self.current_time)
      self.pump_schedule_repo.create(next_schedule)
    return next_schedule