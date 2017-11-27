import sys
import pytest
import datetime

from ..lib.entities.time_control import TimeControl

# fixtures
@pytest.fixture()
def time_control():
  return TimeControl(name='Night', check_interval=2400, outdoor_max=4, start_at="23:59", end_at="02:45")

@pytest.fixture()
def another_time_control():
  return TimeControl(name='Morning', check_interval=2400, outdoor_max=3, start_at="02:45", end_at="08:00")

# tests
def test_init(time_control):
  assert isinstance(time_control, TimeControl)
  assert time_control.name   == 'Night'
  assert time_control.check_interval == 2400
  assert time_control.outdoor_max == 4
  assert time_control.start_at == datetime.datetime(2017, 11, 18, 23, 59, 00, 000000).time()
  assert time_control.end_at == datetime.datetime(2017, 11, 19, 2, 45, 00, 000000).time()

def test_comparison(time_control, another_time_control):
  assert time_control == time_control
  assert time_control != another_time_control
  assert another_time_control == another_time_control
