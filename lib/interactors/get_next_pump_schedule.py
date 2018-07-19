import datetime

from lib.repositories.pump_control_rule_repository import PumpControlRuleRepository
from lib.entities.pump_schedule import PumpSchedule


class GetNextPumpSchedule(object):

    def __init__(self, pump_control_rule_repo=PumpControlRuleRepository()):
        self.pump_control_rule_repo = pump_control_rule_repo

    def __call__(self, current_date_time, pump):
        self.current_date_time = current_date_time
        self.pump = pump
        self.control_rule = self.__get_control_rule_for_pump(self.pump)

        return self.__next_schedule()

    def __get_control_rule_for_pump(self, pump):
        return self.pump_control_rule_repo.find_for_pump_id(pump.id)

    def __next_schedule(self):
        current_time_control = self.__find_time_control(self.current_date_time)
        if(current_time_control is None):  # there is no time_control definition at the moment
            return None

        time_per_slot = current_time_control.check_interval / self.control_rule.time_slots
        increase_per_slot = (time_per_slot * self.control_rule.temperature_delta) / current_time_control.check_interval
        slots_to_run = (self.control_rule.nominal_temperature - self.current_temperature()) / increase_per_slot
        seconds_to_wait = (self.control_rule.time_slots - slots_to_run) * time_per_slot

        next_start = self.current_date_time + datetime.timedelta(seconds=seconds_to_wait)
        start_time_control = self.__find_time_control(next_start)
        if(current_time_control != start_time_control):  # next_start would be within subsequent time_control
            return None

        next_stop = self.current_date_time + \
            datetime.timedelta(seconds=current_time_control.check_interval)

        stop_time_control = self.__find_time_control(next_stop)

        if(current_time_control != stop_time_control):
            replace_units = {'hour': stop_time_control.start_at.hour,
                             'minute': stop_time_control.start_at.minute, 'second': 0}
            if(next_stop.time() <= stop_time_control.start_at):  # check if stop_time_control starts at previous day
                replace_units['day'] = next_start.day
            next_stop = next_stop.replace(**replace_units)

        return PumpSchedule(pump_id=self.pump.id, next_start=next_start, next_stop=next_stop)

    def __find_time_control(self, current_date_time):
        result = [time_control for time_control in self.control_rule.time_controls if self.__is_time_in_range(
            current_date_time.time(), time_control)]
        return result[0] if len(result) > 0 else None

    def __is_time_in_range(self, current_time, time_control):
        if time_control.start_at < time_control.end_at:
            return current_time >= time_control.start_at and current_time <= time_control.end_at
        else:  # over midnight
            return current_time >= time_control.start_at or current_time <= time_control.end_at

    def __time_delta(self):
        self.control_rule.nominal_temperature - self.control_rule.start_temperature

    def current_temperature(self):
        return 33