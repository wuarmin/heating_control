import sys
import pytest
import datetime

from ..lib.entities.pump_schedule import PumpSchedule

def test_init():
  schedule = PumpSchedule(pump_id='OG', next_start='2015-01-01T23:59:59.000000', next_stop='2015-01-02T03:59:59.000000')
  assert isinstance(schedule, PumpSchedule)
  assert schedule.pump_id     == 'OG'
  assert schedule.next_start  == datetime.datetime(2015, 1, 1, 23, 59, 59, 000000)
  assert schedule.next_stop   == datetime.datetime(2015, 1, 2, 3, 59, 59, 000000)