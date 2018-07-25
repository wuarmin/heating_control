import pytest
from datetime import datetime
from collections import namedtuple
from doubles import expect, InstanceDouble

from lib.interactors.control_pump import ControlPump
from lib.interactors.get_next_pump_schedule import GetNextPumpSchedule
from lib.repositories.pump_schedule_repository import PumpScheduleRepository
from lib.entities.pump_schedule import PumpSchedule
from lib.entities.pump import Pump

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
    control_pump(current_time=datetime(1989, 12, 24, 23, 30, 59, 000000), pump=pump)

    pump_schedule = pump_schedule_repo.find_by_pump_id(pump.id)
    assert isinstance(pump_schedule, PumpSchedule)
    assert pump_schedule.pump_id == pump.id
    assert pump_schedule.next_start == datetime(1989, 12, 24, 23, 34, 19, 000000)
    assert pump_schedule.next_stop == datetime(1989, 12, 24, 23, 47, 39, 000000)
    assert pump.on == False


def test_subsequent_runs_of_control_pump(pump, pump_schedule_repo):
    ControlPump()(current_time=datetime(1990, 12, 24, 23, 30, 59, 000000), pump=pump)
    assert isinstance(pump_schedule_repo.find_by_pump_id('OG'), PumpSchedule)
    assert pump.on == False
    ControlPump()(current_time=datetime(1990, 12, 24, 23, 34, 19, 000000), pump=pump)
    assert isinstance(pump_schedule_repo.find_by_pump_id('OG'), PumpSchedule)
    assert pump.on == True
    ControlPump()(current_time=datetime(1990, 12, 24, 23, 40, 19, 000000), pump=pump)
    assert isinstance(pump_schedule_repo.find_by_pump_id('OG'), PumpSchedule)
    assert pump.on == True
    ControlPump()(current_time=datetime(1990, 12, 24, 23, 48, 19, 000000), pump=pump)
    assert PumpScheduleRepository().find_by_pump_id('OG') is None
    assert pump.on == False
    ControlPump()(current_time=datetime(1990, 12, 24, 23, 48, 50, 000000), pump=pump)
    pump_schedule = PumpScheduleRepository().find_by_pump_id('OG')
    assert pump_schedule.pump_id == pump.id
    assert pump_schedule.next_start == datetime(1990, 12, 24, 23, 52, 10, 000000)
    assert pump_schedule.next_stop == datetime(1990, 12, 25, 0, 0, 0, 000000)

def test_switch_off_pump_if_next_schedule_is_none(pump):
    current_time = datetime(1990, 12, 24, 23, 30, 59, 000000)

    doubles = doubles_switch_off_pump_if_next_schedule_is_none(current_time, pump)

    control_pump = ControlPump(
        pump_schedule_repo=doubles.pump_schedule_repo,
        get_next_pump_schedule=doubles.get_next_pump_schedule
    )
    control_pump(current_time=current_time, pump=pump)
    
    assert pump.off == True

def doubles_switch_off_pump_if_next_schedule_is_none(current_time, pump):
    pump_schedule_repo = InstanceDouble('lib.repositories.pump_schedule_repository.PumpScheduleRepository')
    expect(pump_schedule_repo).find_by_pump_id('OG').and_return(None)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')
    expect(get_next_pump_schedule).__call__(current_time, pump).and_return(None)

    Doubles = namedtuple('Doubles' , 'pump_schedule_repo get_next_pump_schedule')
    return Doubles(pump_schedule_repo, get_next_pump_schedule)

def test_switch_off_pump_if_current_time_is_after_next_stop(pump):
    current_time = datetime(1990, 12, 24, 23, 30, 59, 000000)

    doubles = doubles_switch_off_pump_current_time_is_after_next_stop(current_time, pump)

    control_pump = ControlPump(
        pump_schedule_repo=doubles.pump_schedule_repo,
        get_next_pump_schedule=doubles.get_next_pump_schedule
    )
    control_pump(current_time=current_time, pump=pump)
    
    assert pump.off == True

def doubles_switch_off_pump_current_time_is_after_next_stop(current_time, pump):
    pump_schedule_repo = InstanceDouble('lib.repositories.pump_schedule_repository.PumpScheduleRepository')
    next_schedule = PumpSchedule(
        pump_id=pump.id,
        next_start=datetime(1990, 12, 24, 23, 00, 59, 000000),
        next_stop=datetime(1990, 12, 24, 23, 30, 58, 000000)
    )
    expect(pump_schedule_repo).find_by_pump_id('OG').and_return(next_schedule)
    expect(pump_schedule_repo).delete(next_schedule)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')

    Doubles = namedtuple('Doubles' , 'pump_schedule_repo get_next_pump_schedule')
    return Doubles(pump_schedule_repo, get_next_pump_schedule)