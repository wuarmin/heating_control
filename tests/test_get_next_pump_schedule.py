import sys
import pytest
import datetime
from collections import namedtuple
from datetime import datetime, time

from lib.entities.pump_control_rule import PumpControlRule
from lib.entities.pump_schedule import PumpSchedule
from lib.entities.time_control import TimeControl
from lib.interactors.get_next_pump_schedule import GetNextPumpSchedule

# fixtures


def fake_pump_repository(rule):
    class FakePumpControlRuleRepository(object):
        def find_for_pump_id(self, pump_id):
            return rule

    return FakePumpControlRuleRepository()

def fake_sensor_repository(temperature):
    class FakeSensor(object):
        def current_temperature(self):
            return temperature

    class FakeSensorRepository(object):
        def find(self, id):
            return FakeSensor()

    return FakeSensorRepository()


@pytest.fixture()
def pump():
    return namedtuple('Pump', ['id'])

# tests


def test_next_schedule_returns_none_because_subsequent_schedule_will_start_before_current_will_be_applied(pump):
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Night",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(22),
            end_at=time(
                3,
                59)),
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(4),
            end_at=time(8)),
    ])

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=fake_pump_repository(rule_for_test),
        sensor_repo=fake_sensor_repository(33)
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 3, 55, 59, 000000))

    assert next_schedule is None


def test_next_schedule_returns_a_schedule_which_is_in_current_time_control(pump):
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Night",
            check_interval=8800,
            outdoor_max=15,
            start_at=time(22),
            end_at=time(
                21,
                59)),
    ])

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=fake_pump_repository(rule_for_test),
        sensor_repo=fake_sensor_repository(33)
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 23, 30, 59, 000000))

    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 25, 0, 0, 19)
    assert next_schedule.next_stop == datetime(1989, 12, 25, 1, 57, 39)


def test_next_schedule_returns_a_schedule_which_is_in_current_time_control_but_overnight(pump):
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Night",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(22),
            end_at=time(
                3,
                59)),
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(4),
            end_at=time(8)),
    ])

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=fake_pump_repository(rule_for_test),
        sensor_repo=fake_sensor_repository(33)
    )

    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 23, 30, 59, 000000))
    
    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 24, 23, 42, 59)
    assert next_schedule.next_stop == datetime(1989, 12, 25, 0, 30, 59)


def test_starts_at_current_time_control_but_ends_with_start_of_subsequent_control_same_day(pump):
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Night",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(23),
            end_at=time(
                23,
                50)),
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(
                23,
                51),
            end_at=time(8)),
    ])

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=fake_pump_repository(rule_for_test),
        sensor_repo=fake_sensor_repository(33)
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 23, 30, 59, 000000))
    
    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 24, 23, 42, 59)
    assert next_schedule.next_stop == datetime(1989, 12, 24, 23, 51, 0)


def test_starts_at_current_time_control_but_ends_with_start_of_subsequent_control_next_day(pump):
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Night",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(23),
            end_at=time(
                0,
                5)),
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(
                0,
                6),
            end_at=time(8)),
    ])
    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=fake_pump_repository(rule_for_test),
        sensor_repo=fake_sensor_repository(33)
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 23, 30, 59, 000000))
    
    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 24, 23, 42, 59)
    assert next_schedule.next_stop == datetime(1989, 12, 25, 0, 6, 0)


def test_returns_none_if_no_time_control_is_set(pump):
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(
                0,
                6),
            end_at=time(8)),
    ])

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=fake_pump_repository(rule_for_test),
        sensor_repo=fake_sensor_repository(33)
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 23, 30, 59, 000000))
    
    assert next_schedule is None
