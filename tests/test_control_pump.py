import sys
import pytest
import datetime
import collections

from ..lib.interactors.control_pump import ControlPump
from ..lib.repositories.pump_schedule_repository import PumpScheduleRepository
from ..lib.entities.pump_schedule import PumpSchedule
from ..lib.entities.pump import Pump

# fixtures
@pytest.fixture()
def pump():
  return Pump(id='OG', control_pin=14)

@pytest.fixture()
def pump_schedule_repo():
  pump_schedule_repo = PumpScheduleRepository()
  yield pump_schedule_repo
  pump_schedule_repo.clear()

# tests
def test_initial_run_of_control_pump(pump, pump_schedule_repo):
  control_pump = ControlPump()
  control_pump(current_time=datetime.datetime(1989, 12, 24, 23, 30, 59, 000000), pump=pump)

  pump_schedule = pump_schedule_repo.find_by_pump_id(pump.id)
  assert isinstance(pump_schedule, PumpSchedule)
  assert pump_schedule.pump_id == pump.id
  assert pump_schedule.next_start == datetime.datetime(1989, 12, 24, 23, 34, 19, 000000)
  assert pump_schedule.next_stop == datetime.datetime(1989, 12, 24, 23, 47, 39, 000000)
  assert pump.on == False

def test_subsequent_runs_of_control_pump(pump, pump_schedule_repo):
  ControlPump()(current_time=datetime.datetime(1990, 12, 24, 23, 30, 59, 000000), pump=pump)
  assert isinstance(pump_schedule_repo.find_by_pump_id('OG'), PumpSchedule)
  assert pump.on == False
  ControlPump()(current_time=datetime.datetime(1990, 12, 24, 23, 34, 19, 000000), pump=pump)
  assert isinstance(pump_schedule_repo.find_by_pump_id('OG'), PumpSchedule)
  assert pump.on == True
  ControlPump()(current_time=datetime.datetime(1990, 12, 24, 23, 40, 19, 000000), pump=pump)
  assert isinstance(pump_schedule_repo.find_by_pump_id('OG'), PumpSchedule)
  assert pump.on == True
  ControlPump()(current_time=datetime.datetime(1990, 12, 24, 23, 48, 19, 000000), pump=pump)
  assert PumpScheduleRepository().find_by_pump_id('OG') is None
  assert pump.on == False
  ControlPump()(current_time=datetime.datetime(1990, 12, 24, 23, 48, 50, 000000), pump=pump)
  pump_schedule = PumpScheduleRepository().find_by_pump_id('OG')
  assert pump_schedule.pump_id == pump.id
  assert pump_schedule.next_start == datetime.datetime(1990, 12, 24, 23, 52, 10, 000000)
  assert pump_schedule.next_stop == datetime.datetime(1990, 12, 25, 0, 0, 0, 000000)

