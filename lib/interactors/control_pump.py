from lib.repositories.pump_schedule_repository import PumpScheduleRepository


class ControlPump(object):

    def __init__(self):
        self.pump_schedule_repo = PumpScheduleRepository()

    def __call__(self, pump, current_time):
        self.pump = pump
        self.current_time = current_time
        next_schedule = self.next_schedule()

        if(not self.pump.on and self.current_time >= next_schedule.next_start):
            self.pump.switch_on()

        if(self.pump.on and self.current_time >= next_schedule.next_stop):
            self.pump.switch_off()
            self.pump_schedule_repo.delete(next_schedule)

    def next_schedule(self):
        next_schedule = self.pump_schedule_repo.find_by_pump_id(self.pump.id)
        if(next_schedule is None):
            rule = self.pump.rule
            next_schedule = rule.next_schedule(self.pump, self.current_time)
            self.pump_schedule_repo.create(next_schedule)
        return next_schedule
