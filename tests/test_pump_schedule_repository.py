import sys
import pytest
import datetime
import collections

from ..lib.repositories.pump_schedule_repository import PumpScheduleRepository
from ..lib.entities.pump_schedule import PumpSchedule

# fixtures
@pytest.fixture()
def repo():
  repo = PumpScheduleRepository()
  yield repo
  repo.clear()

@pytest.fixture()
def new_schedule():
  return PumpSchedule(pump_id='OG', next_start='2017-01-01T15:15:15.000000', next_stop='2017-01-01T15:15:16.000000')

# tests
def test_create_and_find_by_pump_id(repo, new_schedule):
  repo.create(new_schedule)
  schedule = repo.find_by_pump_id('OG')
  assert isinstance(schedule, PumpSchedule)
  assert schedule.pump_id == new_schedule.pump_id
  assert schedule.next_start == datetime.datetime(2017, 1, 1, 15, 15, 15, 000000)
  assert schedule.next_stop == datetime.datetime(2017, 1, 1, 15, 15, 16, 000000)

def test_delete(repo, new_schedule):
  repo.create(new_schedule)
  schedule = repo.find_by_pump_id('OG')
  assert isinstance(schedule, PumpSchedule)

  repo.delete(schedule)
  schedule = repo.find_by_pump_id('OG')
  assert schedule is None

def test_clear(repo, new_schedule):
  repo.create(new_schedule)
  repo.clear()
  schedule = repo.find_by_pump_id('OG')
  assert schedule is None

