import datetime

from lib.entities.time_control import TimeControl
from lib.entities.pump_schedule import PumpSchedule


def is_time_in_range(start_at_time, current_time, end_at_time):
    if start_at_time < end_at_time:
        return current_time >= start_at_time and current_time <= end_at_time
    else:  # over midnight
        return current_time >= start_at_time or current_time <= end_at_time


class PumpControlRule(object):

    def __init__(self, start_temperature, nominal_temperature, time_slots, time_controls):
        self.start_temperature = start_temperature
        self.nominal_temperature = nominal_temperature
        self.time_slots = time_slots
        self.time_controls = time_controls

    def next_schedule(self, pump, current_date_time):
        current_time_control = self.__find_time_control(current_date_time)
        if(current_time_control is None):  # there is no time_control definition at the moment
            return None

        temp_delta = self.nominal_temperature - self.start_temperature
        time_per_slot = current_time_control.check_interval / self.time_slots
        increase_per_slot = (time_per_slot * temp_delta) / current_time_control.check_interval
        slots_to_run = (self.nominal_temperature - self.current_temperature()) / increase_per_slot
        seconds_to_wait = (self.time_slots - slots_to_run) * time_per_slot

        next_start = current_date_time + datetime.timedelta(seconds=seconds_to_wait)
        start_time_control = self.__find_time_control(next_start)
        if(current_time_control != start_time_control):  # next_start would be within subsequent time_control
            return None

        next_stop = current_date_time + \
            datetime.timedelta(seconds=current_time_control.check_interval)

        stop_time_control = self.__find_time_control(next_stop)

        if(current_time_control != stop_time_control):
            replace_units = {'hour': stop_time_control.start_at.hour,
                             'minute': stop_time_control.start_at.minute, 'second': 0}
            if(next_stop.time() <= stop_time_control.start_at):  # check if stop_time_control starts at previous day
                replace_units['day'] = next_start.day
            next_stop = next_stop.replace(**replace_units)

        return PumpSchedule(pump_id=pump.id, next_start=next_start, next_stop=next_stop)

    def current_temperature(self):
        return 33

    # private
    def __find_time_control(self, current_date_time):
        result = [time_control for time_control in self.time_controls if is_time_in_range(
            time_control.start_at, current_date_time.time(), time_control.end_at)]
        return result[0] if len(result) > 0 else None

    def __next_start(self, current_date_time, seconds_to_wait):
        next_start = current_date_time + datetime.timedelta(seconds=seconds_to_wait)
        self.__find_time_control(next_start)
