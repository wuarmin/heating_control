from lib.repositories.pump_schedule_repository import PumpScheduleRepository
from lib.interactors.get_next_pump_schedule import GetNextPumpSchedule


class ControlPump(object):

    def __init__(self, pump_schedule_repo=PumpScheduleRepository(), get_next_pump_schedule=GetNextPumpSchedule()):
        self.pump_schedule_repo = pump_schedule_repo
        self.get_next_pump_schedule = get_next_pump_schedule

    def __call__(self, pump, current_time):
        self.pump = pump
        self.current_time = current_time

        self._switch_on_off_pump(self._next_schedule())

    def _next_schedule(self):
        next_schedule = self._stored_next_schedule()

        if(next_schedule is None):
            next_schedule = self._get_next_schedule()
        return next_schedule

    def _stored_next_schedule(self):
        return self.pump_schedule_repo.find_by_pump_id(self.pump.id)

    def _get_next_schedule(self):
        next_schedule = self.get_next_pump_schedule(self.current_time, self.pump)
        if next_schedule is not None:
            self.pump_schedule_repo.create(next_schedule)
        return next_schedule

    def _switch_on_off_pump(self, next_schedule):
        if(next_schedule is None):
            self.pump.switch_off()
        
        elif(self.pump.off and self._current_time_is_between_next_start_and_stop(next_schedule)):
            self.pump.switch_on()

        elif(self.pump.off and self._current_time_is_before_next_start(next_schedule)):
            pass

        elif(self.pump.off and self._current_time_is_after_next_stop(next_schedule)):
            self.pump_schedule_repo.delete(next_schedule)

        elif(self.pump.on and self._current_time_is_between_next_start_and_stop(next_schedule)):
            pass
       
        elif(self.pump.on and self._current_time_is_before_next_start(next_schedule)):
            self.pump.switch_off()
        
        elif(self.pump.on and self._current_time_is_after_next_stop(next_schedule)):
            self.pump.switch_off()
            self.pump_schedule_repo.delete(next_schedule)
        
        else:
            pass

    def _current_time_is_between_next_start_and_stop(self, next_schedule):
        return next_schedule.next_start <= self.current_time and self.current_time <= next_schedule.next_stop

    def _current_time_is_before_next_start(self, next_schedule):
        return self.current_time < next_schedule.next_start

    def _current_time_is_after_next_stop(self, next_schedule):
        return self.current_time > next_schedule.next_start