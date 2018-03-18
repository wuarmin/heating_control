import sys
import pytest
import collections
from datetime import datetime

from lib.repositories.pump_schedule_repository import PumpScheduleRepository
from lib.entities.pump_schedule import PumpSchedule

# fixtures


@pytest.fixture()
def repo():
    repo = PumpScheduleRepository()
    yield repo
    repo.clear()


@pytest.fixture()
def new_schedule():
    return PumpSchedule(pump_id='OG', next_start=datetime(2017, 1, 1, 15, 15,
                                                          15, 1), next_stop=datetime(2017, 1, 1, 15, 15, 16, 1100))

# tests


def test_create_and_find_by_pump_id(repo, new_schedule):
    repo.create(new_schedule)
    schedule = repo.find_by_pump_id('OG')
    assert isinstance(schedule, PumpSchedule)
    assert schedule.pump_id == new_schedule.pump_id
    assert schedule.next_start == datetime(2017, 1, 1, 15, 15, 15, 1)
    assert schedule.next_stop == datetime(2017, 1, 1, 15, 15, 16, 1100)


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
