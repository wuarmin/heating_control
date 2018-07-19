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
def rule():
    return PumpControlRule(nominal_temperature=45, start_temperature=30, time_slots=4, time_controls=[
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

# tests


def test_init(rule):
    assert isinstance(rule, PumpControlRule)
    assert rule.start_temperature == 30
    assert rule.nominal_temperature == 45
    assert rule.time_slots == 4
    assert len(rule.time_controls) == 2
    for time_control in rule.time_controls:
        assert isinstance(time_control, TimeControl)

def test_returns_its_temperature_delta(rule):
    assert rule.temperature_delta == 15
