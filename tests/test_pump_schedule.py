import sys
import pytest
from datetime import datetime

from lib.entities.pump_schedule import PumpSchedule


def test_init():
    schedule = PumpSchedule(
        pump_id='OG', next_start=datetime(
            2015, 1, 1, 23, 59, 59, 000000), next_stop=datetime(
            2015, 1, 2, 3, 59, 59, 000000))
    assert isinstance(schedule, PumpSchedule)
    assert schedule.pump_id == 'OG'
    assert schedule.next_start == datetime(2015, 1, 1, 23, 59, 59, 000000)
    assert schedule.next_stop == datetime(2015, 1, 2, 3, 59, 59, 000000)
