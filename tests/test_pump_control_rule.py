import sys
import pytest
import datetime
import collections
from datetime import datetime, time

from lib.entities.pump_control_rule import PumpControlRule
from lib.entities.pump_schedule import PumpSchedule
from lib.entities.time_control import TimeControl

# fixtures


@pytest.fixture()
def pump():
    return collections.namedtuple('Pump', ['id'])

# tests


def test_init():
    rule = PumpControlRule(nominal_temperature=45, start_temperature=30, time_slots=4, time_controls=[
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
    assert isinstance(rule, PumpControlRule)
    assert rule.start_temperature == 30
    assert rule.nominal_temperature == 45
    assert rule.time_slots == 4
    assert len(rule.time_controls) == 2
    for time_control in rule.time_controls:
        assert isinstance(time_control, TimeControl)


def test_next_schedule_returns_none_because_subsequent_schedule_will_start_before_current_will_be_applied(
        pump):
    rule = PumpControlRule(nominal_temperature=45, start_temperature=30, time_slots=4, time_controls=[
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
    next_schedule = rule.next_schedule(
        pump=pump('OG'), current_date_time=datetime(
            1989, 12, 24, 3, 55, 59, 000000))
    assert next_schedule is None


def test_next_schedule_returns_a_schedule_which_is_in_current_time_control(pump):
    rule = PumpControlRule(nominal_temperature=45, start_temperature=30, time_slots=4, time_controls=[
        TimeControl(
            name="Night",
            check_interval=8800,
            outdoor_max=15,
            start_at=time(22),
            end_at=time(
                21,
                59)),
    ])
    next_schedule = rule.next_schedule(
        pump=pump('OG'), current_date_time=datetime(
            1989, 12, 24, 23, 30, 59, 000000))
    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 25, 0, 0, 19)
    assert next_schedule.next_stop == datetime(1989, 12, 25, 1, 57, 39)


def test_next_schedule_returns_a_schedule_which_is_in_current_time_control_but_overnight(pump):
    rule = PumpControlRule(nominal_temperature=45, start_temperature=30, time_slots=4, time_controls=[
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
    next_schedule = rule.next_schedule(
        pump=pump('OG'), current_date_time=datetime(
            1989, 12, 24, 23, 30, 59, 000000))
    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 24, 23, 42, 59)
    assert next_schedule.next_stop == datetime(1989, 12, 25, 0, 30, 59)


def test_starts_at_current_time_control_but_ends_with_start_of_subsequent_control_same_day(pump):
    rule = PumpControlRule(nominal_temperature=45, start_temperature=30, time_slots=4, time_controls=[
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

    next_schedule = rule.next_schedule(
        pump=pump('OG'), current_date_time=datetime(
            1989, 12, 24, 23, 30, 59, 000000))
    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 24, 23, 42, 59)
    assert next_schedule.next_stop == datetime(1989, 12, 24, 23, 51, 0)


def test_starts_at_current_time_control_but_ends_with_start_of_subsequent_control_next_day(pump):
    rule = PumpControlRule(nominal_temperature=45, start_temperature=30, time_slots=4, time_controls=[
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

    next_schedule = rule.next_schedule(
        pump=pump('OG'), current_date_time=datetime(
            1989, 12, 24, 23, 30, 59, 000000))
    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 24, 23, 42, 59)
    assert next_schedule.next_stop == datetime(1989, 12, 25, 0, 6, 0)


def test_returns_none_if_no_time_control_is_set(pump):
    rule = PumpControlRule(nominal_temperature=45, start_temperature=30, time_slots=4, time_controls=[
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(
                0,
                6),
            end_at=time(8)),
    ])
    next_schedule = rule.next_schedule(
        pump=pump('OG'), current_date_time=datetime(
            1989, 12, 24, 23, 30, 59, 000000))
    assert next_schedule is None
