from datetime import timedelta

from lib.repositories.pump_control_rule_repository import PumpControlRuleRepository
from lib.repositories.sensor_repository import SensorRepository
from lib.entities.pump_schedule import PumpSchedule


class GetNextPumpSchedule(object):

    def __init__(self, pump_control_rule_repo=PumpControlRuleRepository(), sensor_repo=SensorRepository()):
        self._pump_control_rule_repo = pump_control_rule_repo
        self._sensor_repo = sensor_repo

    def __call__(self, current_date_time, pump):
        self._current_date_time = current_date_time
        self._pump = pump
        self._control_rule = self._get_control_rule_for_pump(self._pump)

        return self._next_schedule()

    def _get_control_rule_for_pump(self, pump):
        return self._pump_control_rule_repo.find_for_pump_id(pump.id)

    def _next_schedule(self):
        current_time_control = self._find_time_control(self._current_date_time)
        if(current_time_control is None):
            return None

        if(self._current_temperatur_is_too_high()):
            return None

        if(self._outsite_temperature_too_high(current_time_control)):
            return None

        next_start = self._compute_next_start(current_time_control)
        if(current_time_control != self._find_time_control(next_start)):
            return None

        next_stop = self._compute_next_stop(next_start, current_time_control)
        return PumpSchedule(pump_id=self._pump.id, next_start=next_start, next_stop=next_stop)

    def _find_time_control(self, current_date_time):
        result = [time_control for time_control in self._control_rule.time_controls if self._is_time_in_range(
            current_date_time.time(), time_control)]
        return result[0] if len(result) > 0 else None

    def _current_temperatur_is_too_high(self):
        return self._current_temperature() >= self._control_rule.nominal_temperature

    def _outsite_temperature_too_high(self, current_time_control):
        return self._sensor_repo.find('OUTSIDE').current_temperature() >= current_time_control.outdoor_max

    def _is_time_in_range(self, current_time, time_control):
        if time_control.start_at < time_control.end_at:
            return current_time >= time_control.start_at and current_time <= time_control.end_at
        else:  # over midnight
            return current_time >= time_control.start_at or current_time <= time_control.end_at

    def _compute_next_start(self, current_time_control):
        time_per_slot = current_time_control.check_interval / self._control_rule.time_slots
        increase_per_slot = (time_per_slot * self._control_rule.temperature_delta) / current_time_control.check_interval
        slots_to_run = (self._control_rule.nominal_temperature - self._current_temperature()) / increase_per_slot
        seconds_to_wait = (self._control_rule.time_slots - slots_to_run) * time_per_slot

        return self._current_date_time + timedelta(seconds=seconds_to_wait)

    def _compute_next_stop(self, next_start, current_time_control):
        next_stop = self._current_date_time + timedelta(seconds=current_time_control.check_interval)
        stop_time_control = self._find_time_control(next_stop)

        if(current_time_control != stop_time_control):
            replace_units = {'hour': stop_time_control.start_at.hour, 'minute': stop_time_control.start_at.minute, 'second': 0}
            if(next_stop.time() <= stop_time_control.start_at):  # check if stop_time_control starts at previous day
                replace_units['day'] = next_start.day
            next_stop = next_stop.replace(**replace_units)
        return next_stop

    def _current_temperature(self):
        current_sensor = self._sensor_repo.find(self._control_rule.temperature_sensor_id)
        return current_sensor.current_temperature()